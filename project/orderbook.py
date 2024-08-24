from pandas.core.frame import DataFrame
import pandas as pd
import time
import os


# 单个订单
class Order():
    def __init__(self,idx,time,price,volume,quote_tyep,order_type):
        self.idx = idx
        self.time = time
        self.price = price
        self.volume = volume
        self.quote_type = quote_tyep
        self.order_type = order_type
        
# 订单数据流
class Orders():
    def __init__(self,path):
        self.df = DataFrame()
        self.data_path = path
        
    def load_data_from_file(self):
        self.df = pd.read_csv(self.data_path)
        
    # 排序、处理none值、处理异常值
    def process_data(self):
        if self.df.isnull().any().any():
            raise Exception("data has null")
        
    def show_data(self):
        print(self.df)
        
        
# order book 中的每一项都是一个OrderBookNode
class OrderBookNode:
    def __init__(self, price, order):
        self.price = price
        self.volume = order.volume
        self.orderlist:list[Order] = [order]
        self.left = None
        self.right = None
    
    # 处理当前价格，部分成交的情况
    def process_part_del(self, volume):
        while self.orderlist: # order已经按照时间 订单ID 排好序
            if self.orderlist[0].volume > volume:
                self.orderlist[0].volume -= volume
                self.volume -= volume
                volume = 0
                break
            else:
                volume -= self.orderlist[0].volume
                self.volume -= self.orderlist.pop(0).volume
# OrderBook
class OrderBook:
    def __init__(self):
        self.root = None

    def insert(self, price, order:Order):
        if not self.root:
            self.root = OrderBookNode(price, order)
        else:
            self._insert(self.root, price, order)

    def _insert(self, node, price, order:Order):
        if price < node.price:
            if node.left is None:
                node.left = OrderBookNode(price, order)
            else:
                self._insert(node.left, price, order)
        elif price > node.price:
            if node.right is None:
                node.right = OrderBookNode(price, order)
            else:
                self._insert(node.right, price, order)
        else:
            node.volume += order.volume
            node.orderlist.append(order)
            node.orderlist = sorted(node.orderlist, key=lambda x: (x.time, x.idx))

    def delete(self, price):
        self.root = self._delete(self.root, price)

    def _delete(self, node, price):
        if node is None:
            return node

        if price < node.price:
            node.left = self._delete(node.left, price)
        elif price > node.price:
            node.right = self._delete(node.right, price)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            temp = self._find_min(node.right)
            node.price = temp.price
            node.volume = temp.volume
            node.right = self._delete(node.right, temp.price)
        return node

    def _find_min(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current
    
    def _find_max(self, node):
        current = node
        while current.right is not None:
            current = current.right
        return current
    
    def find_min(self): 
        return self._find_min(self.root) if self.root else None

    def find_max(self):
        return self._find_max(self.root) if self.root else None


    def inorder_traversal(self):
        result = []
        self._inorder_traversal(self.root, result)
        return result

    def _inorder_traversal(self, node, result):
        if node is not None:
            self._inorder_traversal(node.left, result)
            result.append(node)
            self._inorder_traversal(node.right, result)

