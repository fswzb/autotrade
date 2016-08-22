# coding: utf-8

import numpy as np
import pandas as pd
import math
import talib

#此例子采用Talib提供的MACD指标作为买入/卖出信号。
#当MACD信号小于0卖出。
#当MACD信号大于0买入。
import talib
import numpy as np
import pandas as pd

# 定义一个全局变量, 保存要操作的证券
stocks = ['000001.XSHE', '000002.XSHE', '000004.XSHE', '000005.XSHE']
# 设置我们要操作的股票池
set_universe(stocks)


# 初始化此策略
def handle_data(context, data):
    # 取得当前的现金
    cash = context.portfolio.cash
    # 循环股票列表
    for stock in stocks:
        # 获取股票的收盘价数据
        prices = attribute_history(stock, 40, '1d', ('close'))
        # 创建MACD买卖信号，包括三个参数fast period, slow period, and the signal
        # 注意：MACD使用的price必须是narray
        macd = MACD(
            prices['close'].values,
            fastperiod=12,
            slowperiod=26,
            signalperiod=9)
        # 获取当前股票的数据
        current_position = context.portfolio.positions[stock].amount
        # 获取当前股票价格
        current_price = data[stock].price
        # 当MACD信号小于0，且拥有的股票数量大于0时，卖出所有股票
        if macd < 0 and current_position > 0:
            order_target(stock, 0)
        # 当MACD信号大于0, 且拥有的股票数量为0时，则全仓买入
        elif macd > 0 and current_position == 0:
            number_of_shares = int(cash / current_price)
            # 购买量大于0时，下单
            if number_of_shares > 0:
                # 买入股票
                order(stock, +number_of_shares)
                # 记录这次买入
                log.info("Buying %s" % (stock))


# 定义MACD函数
def MACD(prices, fastperiod=12, slowperiod=26, signalperiod=9):
    '''
    参数设置:
        fastperiod = 12
        slowperiod = 26
        signalperiod = 9

    返回: macd - signal
    '''
    macd, signal, hist = talib.MACD(
        prices,
        fastperiod=fastperiod,
        slowperiod=slowperiod,
        signalperiod=signalperiod)
    return macd[-1] - signal[-1]


def initialize(context):
    # 定义一个全局变量, 保存要操作的证券
    context.stocks = ['601328.XSHG', '600036.XSHG', '600196.XSHG',
                      '600010.XSHG']
    context.LOW_RSI = 30
    context.HIGH_RSI = 70
    # 设置我们要操作的股票池
    set_universe(context.stocks)


# 初始化此策略
def handle_data(context, data):
    # 取得当前的现金
    cash = context.portfolio.cash
    # 循环股票列表
    for stock in context.stocks:
        # 获取股票的收盘价数据,talib参数取14，前14天的rsi无法计算，所以取15天的数据
        prices = attribute_history(stock, 15, '1d', ('close'))
        # 创建RSI买卖信号，包括参数timeperiod
        # 注意：RSI函数使用的price必须是narray
        rsi = talib.RSI(prices['close'].values, timeperiod=14)[-1]
        # 获取当前股票的数据
        current_position = context.portfolio.positions[stock].amount
        # 获取当前股票价格
        current_price = data[stock].price
        # 当RSI信号小于30，且拥有的股票数量大于0时，卖出所有股票
        if rsi < context.LOW_RSI and current_position > 0:
            order_target(stock, 0)
        # 当RSI信号大于70, 且拥有的股票数量为0时，则全仓买入
        elif rsi > context.HIGH_RSI and current_position == 0:
            number_of_shares = int(cash / current_price)
            # 购买量大于0时，下单
            if number_of_shares > 0:
                # 买入股票
                order(stock, +number_of_shares)
                # 记录这次买入
                log.info("Buying %s" % (stock))


def initialize(context):
    # 定义一个全局变量, 保存要操作的证券
    context.stocks = ['601328.XSHG', '600036.XSHG', '600196.XSHG',
                      '600010.XSHG']
    # 设置我们要操作的股票池
    set_universe(context.stocks)


# 初始化此策略
def handle_data(context, data):
    # 取得当前的现金
    cash = context.portfolio.cash
    # 循环股票列表
    for stock in context.stocks:
        # 获取股票的数据
        h = attribute_history(stock, 30, '1d', ('high', 'low', 'close'))
        # 创建STOCH买卖信号，包括最高价，最低价，收盘价和快速线（一般取为9），慢速线
        # 注意：STOCH函数使用的price必须是narray
        slowk, slowd = talib.STOCH(
            h['high'].values,
            h['low'].values,
            h['close'].values,
            fastk_period=9,
            slowk_period=3,
            slowk_matype=0,
            slowd_period=3,
            slowd_matype=0)
        # 获得最近的kd值
        slowk = slowk[-1]
        slowd = slowd[-1]
        # 获取当前股票的数据
        current_position = context.portfolio.positions[stock].amount
        # 获取当前股票价格
        current_price = data[stock].price
        # 当slowk > 90 or slowd > 90，且拥有的股票数量>=0时，卖出所有股票
        if slowk > 90 or slowd > 90 and current_position >= 0:
            order_target(stock, 0)
        # 当slowk < 10 or slowd < 10, 且拥有的股票数量<=0时，则全仓买入
        elif slowk < 10 or slowd < 10 and current_position <= 0:
            number_of_shares = int(cash / current_price)
            # 购买量大于0时，下单
            if number_of_shares > 0:
                # 买入股票
                order(stock, +number_of_shares)
                # 记录这次买入
                log.info("Buying %s" % (stock))

#此例子采用Talib提供的BBANDS( Bollinger Bands )
#布林线（Boll）指标是通过计算股价的“标准差”，再求股价的“信赖。
#该指标在图形上画出三条线，其中上下两条线可以分别看成是股价的阻力线和支撑线，
#而在两条线之间还有一条股价平均线，布林线指标的参数最好设为20。
#一般来说，股价会运行在压力线和支撑线所形成的通道中。


def initialize(context):
    # 定义一个全局变量, 保存要操作的证券
    context.stocks = ['600036.XSHG'
                      ]  #,'601328.XSHG','600196.XSHG','600010.XSHG']
    # 设置我们要操作的股票池
    set_universe(context.stocks)


# 初始化此策略
def handle_data(context, data):
    # 取得当前的现金
    cash = context.portfolio.cash
    # 循环股票列表
    for stock in context.stocks:
        # 获取股票的数据
        h = attribute_history(stock, 25, '1d', ('high', 'low', 'close'))
        # 创建布林线买卖信号，包括价格和参数
        # 注意：函数使用的price必须是narray
        upper, middle, lower = talib.BBANDS(
            h['close'].values,
            timeperiod=20,
            # number of non-biased standard deviations from the mean
            nbdevup=2,
            nbdevdn=2,
            # Moving average type: simple moving average here
            matype=0)
        # 获取当前股票的数据
        current_position = context.portfolio.positions[stock].amount
        # 获取当前股票价格
        current_price = data[stock].price
        # 当价格突破阻力线upper时，且拥有的股票数量>=0时，卖出所有股票
        if current_price >= upper[-1] and current_position >= 0:
            order_target(stock, 0)
        # 当价格跌破支撑线lower时, 且拥有的股票数量<=0时，则全仓买入
        elif current_price <= lower[-1] and current_position <= 0:
            number_of_shares = int(cash / current_price)
            # 购买量大于0时，下单
            if number_of_shares > 0:
                # 买入股票
                order(stock, +number_of_shares)
                # 记录这次买入
                log.info("Buying %s" % (stock))
        record(
            upper=upper[-1],
            lower=lower[-1],
            mean=middle[-1],
            price=current_price,
            position_size=current_position)

#此例子采用Talib提供的平均真实波幅ATR指标作为买入/卖出信号。
#如果当前价格比之前的价格高一个ATR的涨幅，买入股票
#如果之前的价格比当前价格高一个ATR的涨幅，卖出股票


def initialize(context):
    # 定义一个全局变量, 保存要操作的证券
    context.stocks = ['601328.XSHG', '600036.XSHG', '600196.XSHG',
                      '600010.XSHG']
    # 设置我们要操作的股票池
    set_universe(context.stocks)


# 初始化此策略
def handle_data(context, data):
    # 取得当前的现金
    cash = context.portfolio.cash
    # 循环股票列表
    for stock in context.stocks:
        # 获取股票的数据
        h = attribute_history(stock, 30, '1d', ('high', 'low', 'close'))
        # 创建ATR买卖信号，包括最高价，最低价，收盘价和参数timeperiod
        # 注意：ATR函数使用的price必须是narray
        atr = talib.ATR(h['high'].values,
                        h['low'].values,
                        h['close'].values,
                        timeperiod=14)[-1]
        # 获取当前股票的数据
        current_position = context.portfolio.positions[stock].amount
        # 获取当前股票价格
        current_price = data[stock].price
        #获取四天前的收盘价
        prev_close = h['close'].values[-5]
        #如果当前价格比之前的价格高一个ATR的涨幅，买入股票
        upside_signal = current_price - (prev_close + atr)
        #如果之前的价格比当前价格高一个ATR的涨幅，卖出股票
        downside_signal = prev_close - (current_price + atr)
        # 当downside_signal大于0，且拥有的股票数量大于0时，卖出所有股票
        if downside_signal > 0 and current_position > 0:
            order_target(stock, 0)
        # 当upside_signal大于0, 且拥有的股票数量为0时，则全仓买入
        elif upside_signal > 0 and current_position == 0:
            number_of_shares = int(cash / current_price)
            # 购买量大于0时，下单
            if number_of_shares > 0:
                # 买入股票
                order(stock, +number_of_shares)
                # 记录这次买入
                log.info("Buying %s" % (stock))

###多股票轮动
init_money = 1000000
start_date = '2009-01-01'
end_date = '2015-10-26'
#每笔交易时的手续费是, 买入时万分之三，卖出时万分之三加千分之一印花税, 每笔交易最低扣0块钱
buy_cost = 0.0003
sell_cost = 0.0013
min_cost = 0
cangweip = 25 / 100.0  #设定持股仓位
moneyp = 0  #现金占比
threshold = 5 / 100.0  #设置阈值
pricec = 'open'  #用pricec计算仓位价格,是否符合买入卖出条件
price = 'close'  #买入卖出价格
stocklist = ['600000.XSHG', '600036.XSHG', '601166.XSHG',
             '600016.XSHG']  #浦发，招商，兴业，民生
get_price(
    stocklist[0], start_date, end_date, frequency='daily')['close'].plot(
        label='pufa', figsize=[18, 10])
get_price(
    stocklist[1], start_date, end_date,
    frequency='daily')['close'].plot(label='zhaoshang')
get_price(
    stocklist[2], start_date, end_date,
    frequency='daily')['close'].plot(label='xingye')
get_price(
    stocklist[3], start_date, end_date,
    frequency='daily')['close'].plot(label='minsheng')
plt.legend(loc='best')


def dataprocess(stocklist, start_date, end_date):  #输入stocklist列表
    stocks = []
    for stock in stocklist:
        df_stock = get_price(stock, start_date, end_date, frequency='daily')
        df_stock[df_stock['volume'] == 0] = np.nan
        df_stock = df_stock[['open', 'close']]
        stocks.append(df_stock)
    return stocks


def balance(stocks, pricec, price, buy_cost, sell_cost, min_cost, cangweip,
            threshold, init_money):
    df_stock1 = stocks[0]
    df_stock2 = stocks[1]
    df_stock3 = stocks[2]
    df_stock4 = stocks[3]  #每只股票的dataframe
    num_stock1 = []
    num_stock2 = []
    num_stock3 = []
    num_stock4 = []  #股票持有数
    cangwei1 = []
    cangwei2 = []
    cangwei3 = []
    cangwei4 = []  #仓位
    n = len(stocks[0])
    money = []  #剩余现金
    portfolio_value = []  #总价值
    portfolio_valuebudong = []
    p1 = []
    p2 = []
    p3 = []
    p4 = []  #仓位占比
    k = 0
    num_tiaozheng = 0
    index1 = []
    #开始第一天股票就有停盘数据，顺延直到都没停盘。只要有一只股票停盘就不进行操作
    for i in range(0, n):
        #print i
        numnan = 0
        for stock in stocks:
            if math.isnan(stock['open'][i]):
                numnan = numnan + 1
        if numnan == 0:
            index1.append(stocks[0].index[i])
            if k == 0:  #初始买入，以开盘价买入
                cost = init_money * buy_cost
                if cost < min_cost:
                    cost = min_cost
                init_money1 = init_money - cost
                #计算可以购买的股票数
                num_stock1.append(
                    int(cangweip * init_money1 / df_stock1[pricec][i]))
                num_stock2.append(
                    int(cangweip * init_money1 / df_stock2[pricec][i]))
                num_stock3.append(
                    int(cangweip * init_money1 / df_stock3[pricec][i]))
                num_stock4.append(
                    int(cangweip * init_money1 / df_stock4[pricec][i]))
                #每只股票可购买的股票数存到一个list中
                num_stocks = [num_stock1, num_stock2, num_stock3, num_stock4]
                #计算仓位
                cangwei1.append(num_stock1[-1] * df_stock1[pricec][i])
                cangwei2.append(num_stock2[-1] * df_stock2[pricec][i])
                cangwei3.append(num_stock3[-1] * df_stock3[pricec][i])
                cangwei4.append(num_stock4[-1] * df_stock4[pricec][i])
                money.append(init_money1 - cangwei1[-1] - cangwei2[-1] -
                             cangwei3[-1] - cangwei4[-1])  #计算持有的现金量
                portfolio_value.append(init_money)  #初始化总价值
                #计算仓位比例
                p1.append(cangwei1[-1] / (init_money))
                p2.append(cangwei2[-1] / (init_money))
                p3.append(cangwei3[-1] / (init_money))
                p4.append(cangwei4[-1] / (init_money))
                k = k + 1
            else:
                #计算仓位
                cangwei1.append(num_stock1[-1] * df_stock1[pricec][i])
                cangwei2.append(num_stock2[-1] * df_stock2[pricec][i])
                cangwei3.append(num_stock3[-1] * df_stock3[pricec][i])
                cangwei4.append(num_stock4[-1] * df_stock4[pricec][i])
                #计算总价值
                total_value = money[-1] + cangwei1[-1] + cangwei2[
                    -1] + cangwei3[-1] + cangwei4[-1]
                #计算各股票所占的仓位比例
                p1.append(cangwei1[-1] / total_value)
                p2.append(cangwei2[-1] / total_value)
                p3.append(cangwei3[-1] / total_value)
                p4.append(cangwei4[-1] / total_value)
                #如果每只股票的仓位占比都在（仓位-阈值）到（仓位+阈值）之间，则不进行操作
                if p1[-1] > (cangweip - threshold) and p1[-1] < (
                        cangweip + threshold
                ) and p2[-1] > (cangweip - threshold) and p2[-1] < (
                        cangweip + threshold) and p3[-1] > (
                            cangweip - threshold) and p3[-1] < (
                                cangweip + threshold) and p4[-1] > (
                                    cangweip - threshold) and p4[-1] < (
                                        cangweip + threshold):
                    num_stock1.append(num_stock1[-1])
                    num_stock2.append(num_stock2[-1])
                    num_stock3.append(num_stock3[-1])
                    num_stock4.append(num_stock4[-1])
                    num_stocks = [num_stock1, num_stock2, num_stock3,
                                  num_stock4]
                    money.append(money[-1])
                    portfolio_value.append(money[-1] + num_stock1[
                        -1] * df_stock1[price][i] + num_stock2[-1] * df_stock2[
                            price][i] + num_stock3[-1] * df_stock3[price][
                                i] + num_stock4[-1] * df_stock4[price][i])
                #只要有一只股票触发调仓标准就进行买卖
                else:
                    #计算总价值
                    total_value = money[-1] + num_stock1[-1] * df_stock1[
                        price][i] + num_stock2[-1] * df_stock2[price][
                            i] + num_stock3[-1] * df_stock3[price][
                                i] + num_stock4[-1] * df_stock4[price][i]
                    #计算买卖成本
                    for j in range(0, len(stocklist)):  #循环四只股票
                        num_stock = int(
                            cangweip * total_value /
                            stocks[j][price][i])  #计算得到目前总价值25%的仓位占比应该有的股票数
                        if num_stock - num_stocks[j][
                                -1] > 0:  #应该有的-已有的股票数，>0需要买入股票，<0需要卖出股票
                            buy_money = (num_stock - num_stocks[j][-1]
                                         ) * stocks[j][price][i]
                            buycost = buy_money * buy_cost  #计算买入手续费
                            total_value = total_value - buycost
                        else:
                            sell_money = abs(num_stock - num_stocks[j][
                                -1]) * stocks[j][price][i]
                            sellcost = sell_money * sell_cost  #计算卖出手续费
                            total_value = total_value - sellcost
                    #计算除去手续费后可以购买的股票数量
                    num_stock1.append(
                        int(cangweip * total_value / df_stock1[price][i]))
                    num_stock2.append(
                        int(cangweip * total_value / df_stock2[price][i]))
                    num_stock3.append(
                        int(cangweip * total_value / df_stock3[price][i]))
                    num_stock4.append(
                        int(cangweip * total_value / df_stock4[price][i]))
                    #计算现金持有量
                    money.append(total_value - num_stock1[-1] * df_stock1[
                        price][i] - num_stock2[-1] * df_stock2[price][
                            i] - num_stock3[-1] * df_stock3[price][i] -
                                 num_stock4[-1] * df_stock4[price][i])
                    #计算现金股票的总价值
                    portfolio_value.append(money[-1] + num_stock1[
                        -1] * df_stock1[price][i] + num_stock2[-1] * df_stock2[
                            price][i] + num_stock3[-1] * df_stock3[price][
                                i] + num_stock4[-1] * df_stock4[price][i])
                    #进行调整一次，调整次数加1
                    num_tiaozheng = num_tiaozheng + 1
            #计算持股不动时，组合的总价值
            portfolio_valuebudong.append(money[0] + num_stock1[0] * df_stock1[
                price][i] + num_stock2[0] * df_stock2[price][i] + num_stock3[
                    0] * df_stock3[price][i] + num_stock4[0] * df_stock4[price]
                                         [i])
    df2 = pd.DataFrame(index=index1)
    df2['num_stock1'] = num_stock1
    df2['num_stock2'] = num_stock2
    df2['num_stock3'] = num_stock3
    df2['num_stock4'] = num_stock4
    df2['caiwei1'] = cangwei1
    df2['caiwei2'] = cangwei2
    df2['caiwei3'] = cangwei3
    df2['caiwei4'] = cangwei4
    df2['portfolio_value'] = portfolio_value
    return portfolio_value, portfolio_valuebudong, num_tiaozheng, df2


stocks = dataprocess(stocklist, start_date, end_date)  #list中是dataframe
canshu = [0.25 / 100.0, 0.5 / 100.0, 0.75 / 100.0, 1 / 100.0, 2 / 100.0,
          3 / 100.0, 4 / 100.0, 5 / 100.0, 6 / 100.0, 7 / 100.0, 8 / 100.0, 9 /
          100.0, 10 / 100.0, 11 / 100.0, 12 / 100.0, 13 / 100.0, 14 / 100.0, 15
          / 100.0, 16 / 100.0, 17 / 100.0, 18 / 100.0, 19 / 100.0, 20 / 100.0]
list1 = []
for threshold in canshu:
    portfolio_value, portfolio_valuebudong, num_tiaozheng, df2 = balance(
        stocks, pricec, price, buy_cost, sell_cost, min_cost, cangweip,
        threshold, init_money)
    list1.append(df2)
    print portfolio_value[-1], portfolio_valuebudong[-1], num_tiaozheng
