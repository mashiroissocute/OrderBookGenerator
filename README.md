# Order Book Generator

README : https://github.com/mashiroissocute/OrderBookGenerator


## 1. 环境配置
pip install -r requirements.txt

## 2. 运行
```shell
cd prject
python myborker.py
```
结果如下:
![result]](result.png)

`注： 交易所一般在订单簿中不展示详细的orders信息。本程序处于方便可视化和验证的目的，展示了orders(idx,volume)信息`

## 3. 源码说明

### `orderbook.py`：订单簿类，负责管理订单簿中的订单
订单薄设计大量的删除、插入、按price查找订单的操作。因此采用二叉搜索树来管理订单薄，以实现O(logn)的查找、插入、删除操作。

- Order类用于记录一个订单
- Orders类用于从本地获取订单流并对数据流异常数据进行处理
- OrderBookNode 是订单薄类，通过二叉搜索树组织，每个节点包含price、volume、orderlist(Order类组成的列表)，以及指向左右子节点的指针。

### `myborker.py`：主程序，负责生成订单簿并展示订单博

订单流处理：按照订单的quote_type 和 order_type执行不同的操作，更新订单薄OrderBookNode。

- ASK LIMIT 订单 : 通过process_ask_limit_order处理
- ASK MARKET 订单 : 通过process_ask_market_order处理
- BID LIMIT 订单 : 通过process_bid_limit_order处理
- BID MARKET 订单 : 通过process_bid_market_order处理

每个函数的处理流程都在代码中进行了详细注释。

`注: 常见的交易所会对LIMIT订单进行交易，查看是否超出价格笼子，如果超出则拒绝交易。本程序对此进行了简化，例如大于卖1价的 BID LIMIT 订单将进行成交，直到不满足大于卖1价。`
