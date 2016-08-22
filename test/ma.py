# coding: utf-8
import talib
import math
import numpy as np
import pandas as pd


def initialize(context):
    # 定义一个全局变量, 保存要操作的证券
    g.index = '000001.XSHG'
    g.stocks = ['600196.XSHG']

    # 设定全局参数
    g.pastDay = 90  # 初始基准日期
    g.topK = 3  # 只操作topK只股票
    g.gainThre = g.pastDay * 0.02  # 涨幅限制
    g.refreshSign = 0  # 持仓条件更新参数
    g.selectStockMethod = 3  # 选股方法参数(可选：0,1,2,3)
    g.closePositionMethod = 0  # 清仓方式参数(可选：0,1)
    g.stopLossMethod = 1  # 止损方式参数(可选：0,1,2)

    # 按周期选股
    run_monthly(mainSelectStocks, 1, time='before_open')


# 根据涨幅筛选股票
def filtGain(stocks, pastDay):
    # 初始化参数信息
    numStocks = len(stocks)
    rankValue = []

    # 计算涨跌幅
    for security in stocks:
        # 获取过去pastDay的指数值
        stocksPrice = history(pastDay, '1d', 'close', [security])
        if len(stocksPrice) != 0:
            # 计算涨跌幅
            errCloseOpen = [
                (float(stocksPrice.iloc[-1]) - float(stocksPrice.iloc[0])) /
                float(stocksPrice.iloc[0])
            ]
            rankValue += errCloseOpen
        else:
            rankValue += [0]

    # 根据周涨跌幅排名
    filtStocks = {'code': stocks, 'rankValue': rankValue}
    filtStocks = pd.DataFrame(filtStocks)
    filtStocks = filtStocks.sort('rankValue', ascending=False)
    # 根据涨跌幅筛选
    filtStocks = filtStocks.head(g.topK)
    filtStocks = list(filtStocks['code'])

    return filtStocks


# 根据成交量筛选股票
def filtVol(stocks):
    # 初始化返回数组
    returnStocks = []

    # 筛选
    for security in stocks:
        stockVol = history(60, '1d', 'volume', [security])
        if float(mean(stockVol.iloc[-5:])) > float(mean(stockVol.iloc[-30:])):
            returnStocks += [security]
        else:
            continue
    return returnStocks


# 根据流通市值筛选股票
def filtMarketCap(context, stocks, index):
    # 初始化返回数组
    returnStocks = []

    # 计算指数的总流通市值
    oriStocks = get_index_stocks(index)
    indexMarketCap = get_fundamentals(
        query(valuation.circulating_market_cap).filter(
            valuation.code.in_(oriStocks)),
        date=context.current_dt)
    totalMarketCap = float(sum(indexMarketCap['circulating_market_cap']))

    # 计算个股流通市值占总市值百分比阈值：以四分位为阈值
    indexMarketCap = indexMarketCap.div(totalMarketCap, axis=0)
    porThre = indexMarketCap.describe()
    porThre = float(porThre.loc['25%'])

    # 筛选
    for security in stocks:
        stockMarketCap = get_fundamentals(
            query(valuation.circulating_market_cap).filter(
                valuation.code.in_([security])),
            date=context.current_dt)
        if float(stockMarketCap.iloc[0]) > totalMarketCap * porThre:
            returnStocks += [security]
        else:
            continue
    return returnStocks


# 寻找指数的龙头股
def findLeadStock(context, index, pastDay, method=0):
    # 初始化参数
    topK = g.topK
    # 规则
    # 1.涨幅大于阈值的topK只股票；
    # 3.过去一周成交量大于过去两周成交量；
    # 4.个股流通市值占总市值百分比达到阈值
    # 取出该指数的股票:
    oriStocks = get_index_stocks(index)
    # 根据个股涨幅筛选
    filtStocks = filtGain(oriStocks, pastDay)

    # 根据规则筛选绩优股
    if method == 0:
        # 基本限制
        return filtStocks
    elif method == 1:
        # 基本限制+成交量限制
        filtStocks = filtVol(filtStocks)
        return filtStocks
    elif method == 2:
        # 基本限制+流通市值限制
        filtStocks = filtMarketCap(context, filtStocks, index)
        return filtStocks
    elif method == 3:
        # 基本限制+流通市值限制+成交量限制
        filtStocks = filtVol(filtStocks)
        if len(filtStocks) != 0:
            filtStocks = filtMarketCap(context, filtStocks, index)
        else:
            pass
        return filtStocks
    else:
        return 'Error method order'


# 按周期选股
def mainSelectStocks(context):
    index = g.index
    pastDay = g.pastDay
    topK = g.topK

    # 获取候选股票池
    stocks = findLeadStock(context, index, pastDay, method=g.selectStockMethod)

    # 重置参数
    g.stocks = stocks


# 均线筛股
def stopLoss(security, method=0):
    stocksPrice = history(10, '1d', 'avg', [security])
    if method == 0:
        errPrice = float(
            (stocksPrice.iloc[-1] - stocksPrice.iloc[0]) / stocksPrice.iloc[0])
        if errPrice < 0.02:
            return True
        else:
            return False
    elif method == 1:
        stocksPrice = list(stocksPrice[security])
        gainSign = [
            1 for i in range(1, len(stocksPrice))
            if (stocksPrice[i] - stocksPrice[i - 1]) / stocksPrice[i] > 0
        ]
        if float(len(gainSign)) / float(len(stocksPrice)) > 0.5:
            return False
        else:
            return True
    elif method == 2:
        return False
    else:
        return 'Error method order'


# 买卖股票函数
def mainHandle(context, data, method=0):
    # 获取全局参数值
    pastDay = g.pastDay
    stocks = g.stocks

    # 买卖操作
    if len(stocks) != 0:
        # 等权分配资金
        cash = context.portfolio.cash
        cash = cash / len(stocks)

        for i, security in enumerate(stocks):
            # 获取股票基本信息：是否停牌、是否ST,持股头寸、股价等
            currentData = get_current_data()
            pauseSign = currentData[security].paused
            STInfo = get_extras(
                'is_st',
                security,
                start_date=context.current_dt,
                end_date=context.current_dt)
            STSign = STInfo.iloc[-1]
            if not pauseSign and not STSign.bool():
                stockPrice = history(pastDay, '1d', 'close', [security])
                if not math.isnan(stockPrice[security][0]):
                    # 计算KDJ
                    macd, signal, hist = talib.MACD(
                        stockPrice[security].values,
                        fastperiod=5,
                        slowperiod=30,
                        signalperiod=5)

                    macdSign = macd[-1] - signal[-1]

                    # 获取持仓成本
                    avgCost = context.portfolio.positions[security].avg_cost
                    price = context.portfolio.positions[security].price

                    # 判断&交易
                    if macdSign > 0:
                        # 金叉信号
                        if method == 0:
                            # 根据持仓成本更新标记符更新持仓成本
                            if g.refreshSign == 1:
                                context.portfolio.positions[
                                    security].avg_cost = price
                                g.refreshSign = 0
                                continue
                            else:
                                pass
                            # 判断凸组合条件
                            if price >= avgCost and stopLoss(
                                    security, g.stopLossMethod) == False:
                                order(security, int(cash / data[security].avg))
                                # order_target_value(security,cash)
                                print("Buying %s" % (security))
                            else:
                                order_target(security, 0)
                                print("Selling %s" % (security))
                        elif method == 1:
                            order(security, int(cash / data[security].avg))
                            # order_target_value(security,cash)
                            print("Buying %s" % (security))
                        else:
                            print("Error method order")

                    elif macdSign < 0 and context.portfolio.positions[
                            security].sellable_amount > 0:
                        # 死叉信号
                        if method == 0:
                            if price >= avgCost and stopLoss(
                                    security, g.stopLossMethod) == False:
                                # 更新持仓成本标记符
                                g.refreshSign = 1
                            else:
                                order_target(security, 0)
                                print("Selling %s" % (security))
                        elif method == 1:
                            order_target(security, 0)
                            print("Selling %s" % (security))
                        else:
                            print("Error method order")

                    else:
                        continue
                else:
                    continue
            else:
                continue
    else:
        for security in context.portfolio.positions.keys():
            order_target(security, 0)
            print("Selling %s" % (security))


def handle_data(context, data):
    # 买卖股票
    mainHandle(context, data, g.closePositionMethod)
