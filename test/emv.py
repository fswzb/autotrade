# coding: utf-8

#此例子采用EMV指标作为买入/卖出信号。
#当EMV信号从上方穿越0时卖出。
#当EMV信号从下方穿越0时买入。
import talib
import numpy as np
import pandas as pd


def initialize(context):
    #定义全局变量，保存EM，EMV序列
    g.EM1 = []
    g.EMV1 = []
    # 定义一个全局变量, 保存要操作的证券
    context.stocks = '600016.XSHG'
    # 设置我们要操作的股票池
    set_universe(context.stocks)


    # 初始化此策略
def handle_data(context, data):
    #获取股票
    stock = context.stocks
    #获取EMV序列
    EMV(g.EM1, stock)
    # 取得当前的现金
    cash = context.portfolio.cash
    #获取股票当前价格
    current_price = data[stock].price
    #判断指标，进行买入卖出操作
    #如果昨天EMV<0而前天EMV>0,并且当天开盘,卖出。
    #如果前天EMV>0而昨天EMV<0,并且当天开盘，买入。
    #记录买入卖出操作
    if g.EMV1[len(g.EMV1) - 1] > 0 and g.EMV1[len(g.EMV1) - 2] < 0 and data[
            stock].money > 0:
        number_of_share = int(cash / current_price)
        if number_of_share > 0:
            order(stock, +number_of_share)
            log.info('Buying %s' % (stock))
    elif g.EMV1[len(g.EMV1) - 1] < 0 and g.EMV1[len(g.EMV1) - 2] > 0 and data[
            stock].money > 0 and context.portfolio.positions[stock].amount > 0:
        order_target(stock, 0)
        log.info('sellng %s' % (stock))


        #获取EM指标函数
def EM(high_today, low_today, money, high_yesterday, low_yesterday):
    A = 0.5 * (high_today + low_today)
    B = 0.5 * (high_yesterday + low_yesterday)
    C = high_today - low_today
    EM = (A - B) * C / money
    return EM


    #获取EMV序列函数
def EMV(EM1, stock):
    #第一天应该获取前三日的数据才能得到前两日的EMV，进而判断进行何种操作
    #后面每天只需获取前两日可得到前一日的EMV
    #high/low/money后缀today yesterday before_yesterday代表昨天，前天，大前天。
    #em后缀的yesterday和before_yesterday代表昨天，前天
    #判断是否是回测第一天，分别进行操作
    if len(g.EM1) == 0:
        #如果是回测第一天
        # 获取股票的价格数据（最高价格，最低价格，成交额）
        h = attribute_history(stock, 3, '1d', ('high', 'low', 'money'))
        high_today = h['high'][-1]
        low_today = h['low'][-1]
        high_yesterday = h['high'][-2]
        low_yesterday = h['low'][-2]
        high_before_yesterday = h['high'][-3]
        low_before_yesterday = h['low'][-3]
        money_today = h['money'][-1]
        money_yesterday = h['money'][-2]
        #通过EM函数获取EM指标，并添加到序列EM1中
        em_yesterday = EM(high_today, low_today, money_today, high_yesterday,
                          low_yesterday)
        em_before_yesterday = EM(high_yesterday, low_yesterday,
                                 money_yesterday, high_before_yesterday,
                                 low_before_yesterday)
        g.EM1.append(em_before_yesterday)
        g.EM1.append(em_yesterday)
        #EMV序列的前两个数据是回测前两天的EMV指标
        g.EMV1.append(em_before_yesterday)
        emv2 = sum(g.EM1[0:2])
        g.EMV1.append(emv2)
    elif len(g.EM1) > 0:
        #如果不是回测第一天
        # 获取股票的价格数据（最高价格，最低价格，成交额）
        h = attribute_history(stock, 2, '1d', ('high', 'low', 'money'))
        high_today = h['high'][-1]
        low_today = h['low'][-1]
        high_yesterday = h['high'][-2]
        low_yesterday = h['low'][-2]
        money = h['money'][-1]
        if money > 0:
            em = EM(high_today, low_today, money, high_yesterday,
                    low_yesterday)
            g.EM1.append(em)
        emv = sum(EM1[0:len(EM1)])
        g.EMV1.append(emv)
