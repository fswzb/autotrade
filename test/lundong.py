# coding: utf-8

#行业龙头股均线
#股票池需要如下：
#沪深300池，
#当前不停牌的股票池，
#有历史数据的股票池,
#两者的交集得到可用股票池
#持仓股票池
#可用股票池中剔除持仓股票得到的股票池（可以进行买入操作的股票池）
#将要买入的股票池：即上述股票池中发出买入信号得到的股票池
#将要卖出的股票池：持仓股票池中，没有停牌的，发出卖出信号的股票池
enable_profile()
import random
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import scipy.stats as stats
import math


def initialize(context):
    #初始化沪深300
    #g.stocks_ttl = get_index_stocks('000300.XSHE')
    g.stocks_ttl = ['000651.XSHE', '601318.XSHG', '000012.XSHE', '002299.XSHE',
                    '600150.XSHG', '600027.XSHG', '600900.XSHG', '600406.XSHG',
                    '600151.XSHG', '002241.XSHE', '000563.XSHE', '000002.XSHE',
                    '601668.XSHG', '002269.XSHE', '600019.XSHG', '600089.XSHG',
                    '600362.XSHG', '002005.XSHE', '600115.XSHG', '601866.XSHG',
                    '600352.XSHG', '600004.XSHG', '601186.XSHG', '002415.XSHE',
                    '002489.XSHE', '002340.XSHE', '601088.XSHG', '000581.XSHE',
                    '000625.XSHE', '600917.XSHG', '600415.XSHG', '600196.XSHG',
                    '600256.XSHG', '600887.XSHG', '600585.XSHG', '601006.XSHG',
                    '000063.XSHE', '300027.XSHE', '600456.XSHG', '600511.XSHG',
                    '600036.XSHG', '600519.XSHG', '600663.XSHG', '600030.XSHG',
                    '000538.XSHE', '600108.XSHG', '600655.XSHG']
    set_universe(g.stocks_ttl)
    set_commission(PerTrade(buy_cost=0.0005, sell_cost=0.0013, min_cost=5))
    #初始化可用股票池(不停牌的股票池)
    g.stocks_trading = []
    #初始化有历史数据的股票池
    g.stocks_hist = []
    #初始化持仓股票池
    g.stocks_hold = []
    #初始化备选股票池
    g.stocks_toChoose = []
    #将要买入的股票池
    g.stocks_toBuy = []
    #将要卖出的股票池
    g.stocks_toSell = []
    #长短均线的间隔
    g.shortMA = 1
    g.longMA = 60
    #持仓持有股票数量的最大上限
    g.numHoldmax = 10
    # 坑满时每次调仓量
    g.num_of_change = 2
    #设置计算几日收益率
    g.period = 10


def before_trading_start(context):
    #得到当前的可用的股票池
    #g.stocks_ttl = get_index_stocks('000300.XSHE')
    #set_universe(g.stocks_ttl)
    current_data = get_current_data(g.stocks_ttl)
    g.stocks_trading = []
    length = len(g.stocks_ttl)
    #得到有历史数据的股票池，并且得到有历史数据
    operate_buy = {}
    g.stocks_hist = []
    for i in range(0, length):
        #得到当前的不停牌股票
        if not current_data[g.stocks_ttl[i]].paused:
            hdict = attribute_history(
                g.stocks_ttl[i],
                g.longMA + 1,
                '1d', ('close'),
                skip_paused=True,
                df=False)
            #取出有历史数据的股票，如果历史数据能够支撑运算，顺便也把买入的信号一做
            temp_hist = hdict['close']
            temp_hist = np.array([x for x in temp_hist if str(x) != 'nan'])
            if len(temp_hist) >= g.longMA:
                g.stocks_hist.append(g.stocks_ttl[i])
                signal = cal_signal(temp_hist)
                operate_buy.update({g.stocks_ttl[i]: signal})

    #得到最后的备选池
    g.stocks_toChoose = list(set(g.stocks_hist).difference(set(g.stocks_hold)))

    #得到最终的可执行池：即发出信号的买入池
    g.stocks_toBuy = []
    length = len(g.stocks_toChoose)
    for i in range(0, length):
        if operate_buy[g.stocks_toChoose[i]] == 1:
            g.stocks_toBuy.append(g.stocks_toChoose[i])

    #得到发出信号的卖出池
    g.stocks_toSell = []
    length = len(g.stocks_hold)
    if length > 0:
        current_hold = get_current_data(g.stocks_hold)
        for i in range(0, length):
            #如果当天股票不停牌，则进行下一步计算
            if not current_hold[g.stocks_hold[i]].paused:
                temp_hist = attribute_history(
                    g.stocks_hold[i],
                    g.longMA + 1,
                    '1d', ('close'),
                    skip_paused=True,
                    df=False)
                signal = cal_signal(temp_hist['close'])
                if signal == -1:
                    g.stocks_toSell.append(g.stocks_hold[i])


#输入某只股票的hist数据，然后判断是否发出买入卖出信号，输入为dataframe，输出为
#数字1:买入，-1卖出，0表示不变
def cal_signal(data_withHist):
    MA_shortYesterday = calMA(data_withHist, g.shortMA)
    MA_shortBeforeYesterday = calMA(data_withHist[:-1], g.shortMA)
    MA_longYesterday = calMA(data_withHist, g.longMA)
    MA_longBeforeYesterday = calMA(data_withHist[:-1], g.longMA)
    signal = 0
    if MA_shortBeforeYesterday < MA_longBeforeYesterday and MA_shortYesterday > MA_longYesterday:
        signal = 1
    elif MA_shortYesterday < MA_longYesterday:
        signal = -1
    return signal


#输入某只股票的hist数据,计算MA，返回一个数
def calMA(data_withHist, num):
    ma = data_withHist[-1 * num:].mean()
    return ma


#构成一个列索引为股票名，收益率一行的索引为
#'return'的dataframe，并返回这个dataframe
def calreturn(stocklist):
    #取出每只股票period天的收盘价格
    stocks_info = history(g.period, '1d', 'close', security_list=stocklist)
    #去除信息不全的数据
    stocks_info.dropna(axis=0, how='any', thresh=None)
    #取出昨天和period天之前的收盘价，计算收益率
    a1 = list(stocks_info.iloc[0])
    a2 = list(stocks_info.iloc[g.period - 1])
    a1 = np.array(a1)
    a2 = np.array(a2)
    #用一个dataframe来保存所有股票的收益率信息
    stocks_return = DataFrame(
        a2 / a1, columns=['return'], index=stocks_info.columns)
    stocks_info = stocks_info.T
    #把收益率的数据加到相应的列
    stocks_info = pd.concat([stocks_info, stocks_return], axis=1)
    #将股票信息按照收益率从小到大来存储
    stocks_info = stocks_info.sort(columns=['return'], ascending=[True])
    #返回处理好的dataframe
    return stocks_info


def handle_data(context, data):
    #首先卖出持仓中该卖出的股票
    for i in range(0, len(g.stocks_toSell)):
        order_target(g.stocks_toSell[i], 0, LimitOrderStyle(0.01))
    g.stocks_hold = list(set(g.stocks_hold).difference(set(g.stocks_toSell)))
    # 计算还剩下的坑位
    num_canBuy = g.numHoldmax - len(g.stocks_hold)

    # 如果坑满了，剔除坑中持有的一部分收益不好的股票，买入备选池中收益率较好的股票
    if num_canBuy == 0 and len(g.stocks_toBuy) > 0:
        stocks_holdreturnup = calreturn(g.stocks_hold)
        stocks_tobuyreturnup = calreturn(g.stocks_toBuy)
        for i in range(0, min(len(g.stocks_toBuy), g.num_of_change)):
            order_target(stocks_holdreturnup.index[i], 0,
                         LimitOrderStyle(0.01))
            g.stocks_hold.remove(stocks_holdreturnup.index[i])
        num_canBuy = g.numHoldmax - len(g.stocks_hold)
        cash_ttl = context.portfolio.cash
        cash_perShare = cash_ttl / num_canBuy
        for i in range(0, num_canBuy):
            order_target_value(
                stocks_tobuyreturnup.index[len(stocks_tobuyreturnup) - i - 1],
                cash_perShare, LimitOrderStyle(9999))

    # 如果坑没满
    elif num_canBuy > 0:
        cash_ttl = context.portfolio.cash
        cash_perShare = cash_ttl / num_canBuy
        #如果备选股票池中的股票数量小于可买的股票，则全部买入
        if len(g.stocks_toBuy) <= num_canBuy:
            for i in range(0, len(g.stocks_toBuy)):
                order_target_value(g.stocks_toBuy[i], cash_perShare,
                                   LimitOrderStyle(9999))

        #如果备选池的股票大于可买数量，则按照收益率买入
        elif len(g.stocks_toBuy) > num_canBuy:
            stocks_tobuyreturnup = calreturn(g.stocks_toBuy)
            for i in range(0, num_canBuy):
                order_target_value(stocks_tobuyreturnup.index[len(
                    stocks_tobuyreturnup) - i - 1], cash_perShare,
                                   LimitOrderStyle(9999))
                #成功下单完了以后更新g.stocks_hold


                #记录一下实际持仓：
def after_trading_end(context):
    g.stocks_hold = context.portfolio.positions.keys()
