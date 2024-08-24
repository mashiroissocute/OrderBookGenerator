from projcet.base import BaseBroker
from projcet.orderbook import Order,Orders,OrderBook,OrderBookNode
import os 
from functools import reduce

from typing import Any

class MyBroker(BaseBroker):
    def __init__(self):
        self.bids = OrderBook() # 买单orderbook
        self.asks = OrderBook() # 卖单orderbook
        
    # 处理 卖单 市价单
    def process_ask_market_order(self, order:Order):
        while order.volume > 0:
            # 不断获取当前最大买单
            max_bid = self.bids.find_max() 
            
            # 已经没有买单了，则加入卖方订单簿，退出
            if max_bid is None: 
                self.asks.insert(order.price,order)
                return
            
            # 有买单，则按照时间 订单ID依次成交
            if max_bid.volume > order.volume: # 当前价格买单充足，一定可以全部成交，退出
                max_bid.process_part_del(order.volume)
                return 
            else: # 当前价格买单不足，部分成交，到下一个价格，不能退出
                order.volume -= max_bid.volume
                self.bids.delete(max_bid.price)
                
                
    # 处理 买单 市价单          
    def process_bid_market_order(self, order:Order):
        while order.volume > 0:
            # 不断获取当前最低卖单
            min_ask = self.asks.find_min() 
            
            # 没有卖单，则加入买方订单簿，退出
            if min_ask is None:  
                self.bids.insert(order.price,order)
                return
            
            # 有卖单，则按照时间 订单ID依次成交
            if min_ask.volume > order.volume: # 当前价格卖单充足，一定可以全部成交，退出
               min_ask.process_part_del(order.volume)
            else:  #当前价格卖单不足，部分成交，到下一个价格，不能退出
                order.volume -= min_ask.volume
                self.asks.delete(min_ask.price)

         
    # 处理 卖单 限价单
    def process_ask_limit_order(self, order:Order):
        while order.volume > 0:
            # 不断获取当前最高买单
            max_bid = self.bids.find_max()
            
            # 已经没有买单 或者 卖单高于最高买单价格 则插入卖单orderbook，退出
            if max_bid is None or order.price > max_bid.price:
                self.asks.insert(order.price,order)
                return
            
            # 存在买单 并且 卖单低于最高买单价格 则开始成交
            if max_bid.volume > order.volume:  #当前价格买单充足，一定可以全部成交，退出
                max_bid.process_part_del(order.volume)
                return
            else: # 当前价格买单不足，部分成交，到下一个价格，不能退出
                order.volume -= max_bid.volume
                self.bids.delete(max_bid.price)

        
    # 处理 买单 限价单
    def process_bid_limit_order(self, order:Order):
        while order.volume > 0:
            # 不断获取当前最低卖单
            min_ask = self.asks.find_min()
            
            # 已经没有卖单 或者  买单低于最低卖单价格 则插入买单orderbook，退出
            if min_ask is None or order.price < min_ask.price:
                self.bids.insert(order.price,order)
                return
            
            # 存在卖单 并且 买单高于orderbook中最低卖单价格 则开始成交
            if min_ask.volume > order.volume:  #当前价格买单充足，一定可以全部成交，退出
                min_ask.process_part_del(order.volume)
                return
            else: # 当前价格买单不足，部分成交，到下一个价格，不能退出
                order.volume -= min_ask.volume
                self.asks.delete(min_ask.price)
        
    def transact(self, order: Any, **kwargs):
        """
        处理订单
        """
        print('start transact, wait a moment')
        for _,row in order.iterrows():
            order = Order(row['idx'],row['time'],row['price'],row['volume'],row['quote_type'],row['order_type'])
            if row['quote_type'] == 'ASK':
                if row['order_type'] == 'LIMIT':
                    self.process_ask_limit_order(order)
                elif row['order_type'] == 'MARKET':
                    self.process_ask_market_order(order)
                else:
                    raise Exception(f'error: unknow order_type {row}')
            elif row['quote_type'] == 'BID':
                if row['order_type'] == 'LIMIT':
                    self.process_bid_limit_order(order)
                elif row['order_type'] == 'MARKET':
                    self.process_bid_market_order(order)
                else:
                    raise Exception(f'error: unknow order_type {row}')
            else:
                raise Exception(f'error: unknow quote_type {row}')

    def order_book(self, level: int = 5, **kwargs):
        """
        根据level返回订单薄
        """        
        asks_list:list[OrderBookNode] =self.asks.inorder_traversal()
        bids_list:list[OrderBookNode] =self.bids.inorder_traversal()
        
        print(f'price\tvolume\torders(idx volume)')
        for ask in list(reversed(asks_list))[-level:]:
            print(f'{ask.price}\t{ask.volume}\t{[(order.idx,order.volume) for order in ask.orderlist]}')
        print("------------------------------------------")
        for bid in list(reversed(bids_list))[0:level]:
            print(f'{bid.price}\t{bid.volume}\t{[(order.idx,order.volume) for order in bid.orderlist]}')
            
        return asks_list,bids_list

# 示例
if __name__ == "__main__":
    orders = Orders(os.getcwd()+'/order.csv')
    orders.load_data_from_file()
    orders.process_data()
    # orders.show_data()
    
    broker = MyBroker()
    broker.transact(orders.df)
    asks,bids = broker.order_book()

    
