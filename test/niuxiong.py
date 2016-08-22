# coding: utf-8
import tushare as ts
import pandas as pd
import datetime

g = {}
# 定义行业类别
g.index = 'industry'
# 定义全局参数值
g.indexThre = 0.2  #站上pastDay日均线的行业比重
g.pastDay = 30  # 过去pastDay日参数
g.topK = 6  #

if g.index == 'index':
    # 定义行业指数list以便去股票
    g.indexList = ['000928.XSHG', '000929.XSHG', '000930.XSHG', '000931.XSHG',
                   '000932.XSHG', '000933.XSHG', '000934.XSHG', '000935.XSHG',
                   '000936.XSHG', '000937.XSHG', '000938.XSHG']
elif g.index == 'industry':
    # 定义行业list以便取股票
    g.indexList = ['A01','A02','A03','A04','A05','B06', \
                   'B07','B08','B09','B11','C13','C14','C15','C17','C18', \
                   'C19','C20','C21','C22','C23','C24','C25','C26','C27', \
                   'C28','C29','C30','C31','C32','C33','C34','C35','C36', \
                   'C37','C38','C39','C40','C41','C42','D44','D45','D46', \
                   'E47','E48','E50','F51','F52','G53','G54','G55','G56', \
                   'G58','G59','H61','H62','I63','I64','I65','J66','J67', \
                   'J68','J69','K70','L71','L72','M73','M74','N77','N78', \
                   'P82','Q83','R85','R86','R87','S90']


# 计算相对强弱RPS值
def calRPS(stocks, curDate, preDate):
    # 初始化参数信息
    numStocks = len(stocks)
    rankValue = []

    # 计算涨跌幅
    for code in stocks:
        # 获取过去pastDay的指数值
        lastDf = ts.get_hist_data(
            code=code, start=preDate, end=curDate, ktype='D')
        lastDf.sort(columns='close')
        lastClosePrice = float(lastDf.iloc[0])
        firstClosePrice = float(lastDf.iloc[-1])
        # 计算涨跌幅
        errCloseOpen = [lastClosePrice - firstClosePrice]
        rankValue += errCloseOpen

    # 根据周涨跌幅排名
    rpsStocks = {'code': stocks, 'rankValue': rankValue}
    rpsStocks = pd.DataFrame(rpsStocks)
    rpsStocks = rpsStocks.sort('rankValue', ascending=False)
    stocks = list(rpsStocks['code'])

    # 计算RPS值
    rpsValue = [99 - (100 * i / numStocks) for i in range(numStocks)]
    rpsStocks = {'code': stocks, 'rpsValue': rpsValue}
    rpsStocks = pd.DataFrame(rpsStocks)

    return rpsStocks


# 股票池：取强舍弱
def findStockPool(indexList, curDate, preDate, index='index'):
    topK = g.topK
    stocks = []
    rpsValue = []
    industryCode = []
    # 从每个行业中选取RPS值最高的topK只股票
    # for eachIndustry in industryList:
    for eachIndex in indexList:
        # 取出该行业的股票
        if index == 'index':
            stocks = get_index_stocks(eachIndex)
        elif index == 'industry':
            stocks = get_industry_stocks(eachIndex)
        else:
            return 'Error index order'

        # 计算股票的相对强弱RPS值
        rpsStocks = calRPS(stocks, curDate, preDate)
        stocks.append(rpsStocks[:topK]['code'])
        # rpsValue += list(rpsStocks[:topK]['rpsValue'])
    return stocks


# 选股：单均线动量策略
def selectStocks(stocks, curDate, data):
    # 初始化
    returnStocks = []

    # 筛选当且仅当当日收盘价在5日均线以上的股票
    for code in stocks:
        closePrice = ts.get_hist_data(
            code=code, start=curDate, end=curDate, ktype='D')
        closePrice.sort(columns='close')
        closePrice = float(closePrice.iloc[-1])
        ma5 = data[code].mavg(5, 'close')
        ma15 = data[code].mavg(15, 'close')
        # if closePrice > ma5:
        if closePrice > ma5 and ma5 > ma15:
            returnStocks.append(code)
        else:
            continue

    return returnStocks


# 止损：牛熊分界线
def calBuySign(indexList, pastDay, data, index='index'):
    # 初始化
    indexThre = g.indexThre

    # 计算过去几天的指数均值,判断是否满足牛熊分界值
    count = 0
    if index == 'index':
        for eachIndex in indexList:
            avgPrice = data[eachIndex].mavg(pastDay, 'close')
            if data[eachIndex].mavg(1, 'close') > avgPrice:
                count += 1
            else:
                continue
    elif index == 'industry':
        for eachIndustry in indexList:
            stocks = get_industry_stocks(eachIndustry)
            pastValue = 0
            curValue = 0
            for eachStocks in stocks:
                # pastValue += data[eachStocks].mavg(pastDay,'close')
                # curValue += data[eachStocks].mavg(1,'close')
                stocksPastPrice = data[eachStocks].mavg(pastDay, 'close')
                stocksCurrPrice = data[eachStocks].price
                if stocksPastPrice is None or stocksCurrPrice is None:
                    continue
                else:
                    pastValue += stocksPastPrice
                    curValue += stocksCurrPrice
            if curValue > pastValue:
                count += 1
            else:
                continue

    else:
        return 'Error index order.'

    # 根据行业比重发出牛熊市场信号
    if float(count) / len(indexList) > indexThre:
        return True
    else:
        return False


# 每个单位时间(如果按天回测,则每天调用一次,如果按分钟,则每分钟调用一次)调用一次
def handle_data(context, data):
    # 初始化参数
    index = g.index
    indexList = g.indexList
    indexThre = g.indexThre
    pastDay = g.pastDay
    curDate = datetime.date.today()
    preDate = curDate + datetime.timedelta(days=-pastDay)
    curDate = str(curDate)
    preDate = str(preDate)
    # 获取资金余额
    cash = context.portfolio.cash
    topK = g.topK
    numSell = 0
    numBuy = 0

    # 牛熊分界线发布止损信号
    buySign = calBuySign(indexList, pastDay, data, index)
    # buySign = True
    if buySign == True:
        # 取强舍弱选股：根据相对RPS指标选取各个行业中最强势的股票形成股票池
        candidateStocks = findStockPool(indexList, curDate, preDate, index)
        # 根据均线策略从股票池中选股买卖
        stocks = selectStocks(candidateStocks, curDate, preDate, data)
        countStocks = len(stocks)
        if countStocks > topK:
            rpsStocks = calRPS(stocks, curDate, preDate)
            stocks = list(rpsStocks[:topK]['code'])
        else:
            pass
        countStocks = len(stocks)

        # 判断当前是否持有目前股票,若已持有股票在新的候选池里则继续持有，否则卖出
        for security in context.portfolio.positions.keys():
            if security in stocks:
                continue
            else:
                order_target(security, 0)
                numSell += 1
                # print("Selling %s" %(security))

                # 根据股票池买入股票
        for security in stocks:
            # 获取股票基本信息：是否停牌、是否ST,持股头寸、股价等
            currentData = get_current_data()
            pauseSign = currentData[security].paused
            STInfo = get_extras(
                'is_st', security, start_date=preDate, end_date=curDate)
            STSign = STInfo.iloc[-1]
            stocksAmount = context.portfolio.positions[security].amount
            stocksPrice = data[security].price

            if not pauseSign and not STSign.bool():
                # 购买该股票，获得可购买的股票数量
                buyAmount = int((cash / countStocks) / stocksPrice)
                order(security, buyAmount)
                numBuy += 1
                # print("Buying %s" % (security))
            else:
                continue
    else:
        # 将目前所有的股票卖出
        for security in context.portfolio.positions:
            # 全部卖出
            order_target(security, 0)
            numSell += 1
            # 记录这次卖出
            # print("Selling %s" % (security))
