# coding: utf-8
import pandas as pd
import numpy as np
import tushare as ts
from operator import methodcaller
import datetime

g = {
    'indexList': ['A01', 'B06', 'C19', 'E47', 'G58', 'J68', 'I64', 'P82'],
    'pastDay': 5,
    'topK': 8,
    'gainThre': 0.05,
    'herdSign': np.zeros((len(g.indexList), 1))
}


def initialize():
    # 定义行业指数list以便去股票
    # g.indexList = ['A01','A02','A03','A04','A05','B06',\
    # 'B07','B08','B09','B11','C13','C14','C15','C17','C18',\
    # 'C19','C20','C21','C22','C23','C24','C25','C26','C27',\
    # 'C28','C29','C30','C31','C32','C33','C34','C35','C36',\
    # 'C37','C38','C39','C40','C41','C42','D44','D45','D46',\
    # 'E47','E48','E50','F51','F52','G53','G54','G55','G56',\
    # 'G58','G59','H61','H62','I63','I64','I65','J66','J67',\
    # 'J68','J69','K70','L71','L72','M73','M74','N77','N78',\
    # 'P82','Q83','R85','R86','R87','S90']
    g.indexList = ['A01', 'B06', 'C19', 'E47', 'G58', 'J68', 'I64', 'P82']
    # 定义全局参数值
    g.pastDay = 5  # 过去pastDay日参数
    g.topK = 8  # topK只股票
    g.gainThre = 0.05  # 涨幅阈值
    g.herdSign = np.zeros((len(g.indexList), 1))

    # 每周判断一次羊群效应
    #run_weekly(mainHerd, 1, time='open')


    # 计算相对强弱RPS值
def calRPS(stocks, preDate, curDate):
    # 初始化
    rankValue = []
    topK = g.topK

    # 计算涨跌幅
    for code in stocks:
        stocksPrice = ts.get_hist_data(
            code=code, start=preDate, end=curDate, ktype='D')
        stocksPrice.sort(columns='close')
        errCloseOpen = [float((stocksPrice.iloc[-1] - stocksPrice.iloc[0]) /
                              stocksPrice.iloc[0])]
        rankValue += errCloseOpen

    # 根据周涨跌幅排名
    rpsStocks = {'code': stocks, 'rankValue': rankValue}
    rpsStocks = pd.DataFrame(rpsStocks)
    rpsStocks = rpsStocks.sort('rankValue', ascending=False)
    rpsStocks = rpsStocks.head(topK)
    rpsStocks = list(rpsStocks['code'])

    return rpsStocks


# 计算行业收益率
def calRmt(index, preDate, curDate):
    Rmt = 0
    sign = 0
    stocks = get_industry_stocks(index)

    for code in stocks:
        stocksPrice = ts.get_hist_data(
            code=code, start=preDate, end=curDate, ktype='D')
        stocksPrice.sort(columns='close')
        stocksPrice = stocksPrice.dropna(how='any')
        if len(stocksPrice) != 0:
            registRmt = (
                float(stocksPrice.iloc[-1]) - float(stocksPrice.iloc[0])
            ) / float(stocksPrice.iloc[0])
            Rmt += registRmt
        else:
            Rmt += 0

    return Rmt / (len(stocks) - sign)


# 判断：是否存在羊群效应
def calHerdSign(index, pastDay):
    #初始化存储数组[CSAD,Rmt,Rmt2]
    stockRInfo = history(pastDay, '1d', 'close', ['000300.XSHG'])
    dateInfo = (stockRInfo.T).columns
    stockRInfo = pd.DataFrame(
        {index: [0] * pastDay,
         'Rmt': [0] * pastDay,
         'Rmt2': [0] * pastDay},
        index=list(dateInfo))

    #计算CSAD
    CSADt = 0
    RitIndex = 0
    dateInfo = dateInfo.map(methodcaller('date'))
    for days in dateInfo:
        # 初始化日期参数
        inCurDate = days + datetime.timedelta(days=-1)
        inPreDate = inCurDate + datetime.timedelta(days=-pastDay)
        inCurDate = str(inCurDate)
        preDate = str(inPreDate)
        #计算当期市场收益率Rmt
        Rmt = calRmt(index, inPreDate, inCurDate)
        stockRInfo.loc[days, 'Rmt'] = Rmt
        stockRInfo.loc[days, 'Rmt2'] = Rmt**2
        #获取指数内的股票
        stocks = get_industry_stocks(index)
        numStocks = len(stocks)
        for code in stocks:
            # 计算Rit
            Rit = ts.get_hist_data(
                code=code, start=inPreDate, end=inCurDate, ktype='D')
            Rit.sort(columns='close')

            # print(Rmt,Rit)
            Rit = Rit.dropna(how='any')
            if len(Rit) != 0:
                Rit = (float(Rit.iloc[-1]) - float(Rit.iloc[0])
                       ) / float(Rit.iloc[0])
                errRmi = abs(Rmt - Rit)
                CSADt += errRmi
            else:
                continue
        stockRInfo.loc[days, index] = float(CSADt / numStocks)
        #重置参数
        CSADt = 0
        RitIndex = 0
    # print(stockRInfo)
    olsResult = pd.stats.api.ols(y=stockRInfo[index],
                                 x=stockRInfo[['Rmt', 'Rmt2']])
    coef = olsResult.beta.loc['Rmt2']
    pvalues = olsResult.p_value.loc['Rmt2']
    if pvalues < 0.5 and coef < 0:
        return 1
    else:
        return 0
        # except:
        # print('Turn to modify code in function "calHerdSign"')


        # 根据涨幅筛选股票
def filtGain(stocks, preDate, curDate):
    # 初始化参数信息
    numStocks = len(stocks)
    rankValue = []

    # 计算涨跌幅
    for code in stocks:
        # 获取过去pastDay的指数值
        stocksPrice = ts.get_hist_data(
            code=code, start=preDate, end=curDate, ktype='D')
        stocksPrice.sort(columns='close')
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
    for i in range(numStocks):
        if filtStocks['rankValue'].iloc[i] > g.gainThre:
            continue
        else:
            break
    filtStocks = filtStocks.head(i)
    filtStocks = list(filtStocks['code'])

    return filtStocks


# 根据成交量筛选股票
def filtVol(stocks):
    # 初始化返回数组
    returnStocks = []

    # 筛选
    for security in stocks:
        stockVol = history(20, '1d', 'volume', [security])
        if float(np.mean(stockVol.iloc[-5:])) > float(
                np.mean(stockVol.iloc[-10:])):
            returnStocks += [security]
        else:
            continue
    return returnStocks


# 根据流通市值筛选股票
def filtMarketCap(context, stocks, index):
    # 初始化返回数组
    returnStocks = []

    # 计算行业流通市值
    oriStocks = get_industry_stocks(index)
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


# 计算行业涨幅
def calIndustryGain(stocks, preDate, curDate):
    gainIndex = 0
    for security in stocks:
        stocksPrice = ts.get_hist_data(
            code=code, start=preDate, end=curDate, ktype='D')
        stocksPrice.sort(columns='close')
        if len(stocksPrice) != 0:
            gainIndex += (
                float(stocksPrice.iloc[-1]) - float(stocksPrice.iloc[0])
            ) / float(stocksPrice.iloc[0])
        else:
            continue
    return gainIndex / len(stocks)


# 寻找指数的龙头股
def findLeadStock(context, index, preDate, curDate, method=0):
    # 初始化参数
    topK = g.topK
    # 规则
    # 1.涨幅大于阈值的topK只股票；
    # 2.指数涨幅在阈值的四分之一以上；
    # 3.过去一周成交量大于过去两周成交量；
    # 4.个股流通市值占总市值百分比达到阈值
    # 取出该指数的股票:
    oriStocks = get_industry_stocks(index)
    # 根据个股涨幅筛选
    filtStocks = filtGain(oriStocks, preDate, curDate)
    # 计算指数涨幅
    gainIndex = calIndustryGain(oriStocks, preDate, curDate)

    # 根据规则筛选龙头股
    if float(gainIndex) / g.gainThre > 0.5:
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
    else:
        return []


# 买卖股票的主函数
def mainHandle(context, stocks, cash, preDate, curDate):
    # 初始化
    numStocks = len(stocks)

    # 买卖操作
    if numStocks > 0:
        # 卖出操作
        # 判断当前是否持有目前股票,若已持有股票在新的候选池里则继续持有，否则卖出
        for security in context.portfolio.positions.keys():
            if security in stocks:
                continue
            else:
                order_target(security, 0)
                print("Selling %s" % (security))
        # 买入操作
        # 获取可操作资金,并等权分配
        if cash != 0:
            for security in stocks:
                # 买入该股票
                # 获取股票基本信息：是否停牌、是否ST,持股头寸、股价等
                currentData = get_current_data()
                pauseSign = currentData[security].paused
                STInfo = get_extras(
                    'is_st',
                    security,
                    start_date=context.current_dt,
                    end_date=context.current_dt)
                STSign = STInfo.iloc[-1]
                # 买入操作
                if not pauseSign and not STSign.bool():
                    # 购买该股票
                    order_value(security, cash / numStocks)
                    print("Buying %s" % (security))
                else:
                    continue
        else:
            pass

    else:
        # 没有股票池，清仓操作
        for security in context.portfolio.positions.keys():
            order_target(security, 0)
            # print("Selling %s" %(security))


            # 每周（月）计算一次羊群效应，并执行买卖操作
def mainHerd(context):
    # 初始化参数
    indexList = g.indexList
    topK = g.topK
    herdSign = g.herdSign
    indexList = g.indexList
    herdStocks = []
    rationalStocks = []

    # 获取全局参数
    pastDay = g.pastDay
    # 初始化日期参数
    # curDate = context.current_dt
    curDate = context.current_dt + datetime.timedelta(days=-1)
    preDate = curDate + datetime.timedelta(days=-pastDay)
    curDate = str(curDate)
    preDate = str(preDate)

    # 判断羊群效应
    returnArr = g.herdSign
    for i, eachIndex in enumerate(indexList):
        herdSign = calHerdSign(eachIndex, pastDay)
        if herdSign == 1:
            herdStocks += findLeadStock(
                context, eachIndex, preDate, curDate, method=1)
        else:
            pass

    # 分配资金
    cash = context.portfolio.cash
    # 执行买卖操作
    if len(herdStocks) > topK:
        herdStocks = calRPS(herdStocks, preDate, curDate)
    else:
        pass
    mainHandle(context, herdStocks, cash, preDate, curDate)


# 回测
def handle_data(context, data):
    day = context.current_dt.day
    if day > 24:
        for security in context.portfolio.positions.keys():
            order_target(security, 0)
            print("Selling %s" % (security))
    else:
        pass
