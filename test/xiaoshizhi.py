# coding: utf-8
'''
小市值择时买卖

配置指定频率的调仓日，在调仓日每日指定时间，计算沪深300指数和中证500指数当前的20日涨
幅，如果2个指数的20日涨幅有一个为正，则进行选股调仓，之后如此循环往复。

止损策略：每日指定时间，计算沪深300指数和中证500指数当前的20日涨幅，如果2个指数涨幅
都为负，则清仓，重置调仓计数，待下次调仓条件满足再操作

版本：v1.2.7
日期：2016.08.13
作者：Morningstar
'''

import tradestat

#from blacklist import *

# blacklist.py
# 建议在研究里建立文件blacklist.py，然后将这段代码拷贝进blacklist.py
# 模拟运行的时候只需要更新研究里的数据即可，这样可在不修改模拟运行代码的情况下
# 修改黑名单


# 配置股票黑名单
# 列出当且极不适宜购买的股票
# 注：1. 黑名单有时效性，回测的时候最好不使用，模拟交易建议使用
#     2. 用一模块或者大数据分析收集这类股票，定时更新
def get_blacklist():
    # 黑名单一览表，更新时间 2016.7.10 by 沙米
    # 科恒股份、太空板业，一旦2016年继续亏损，直接面临暂停上市风险
    blacklist = ["600656.XSHG", "300372.XSHE", "600403.XSHG", "600421.XSHG",
                 "600733.XSHG", "300399.XSHE", "600145.XSHG", "002679.XSHE",
                 "000020.XSHE", "002330.XSHE", "300117.XSHE", "300135.XSHE",
                 "002566.XSHE", "002119.XSHE", "300208.XSHE", "002237.XSHE",
                 "002608.XSHE", "000691.XSHE", "002694.XSHE", "002715.XSHE",
                 "002211.XSHE", "000788.XSHE", "300380.XSHE", "300028.XSHE",
                 "000668.XSHE", "300033.XSHE", "300126.XSHE", "300340.XSHE",
                 "300344.XSHE", "002473.XSHE"]
    return blacklist


def before_trading_start(context):
    log.info("---------------------------------------------")
    #log.info("==> before trading start @ %s", str(context.current_dt))
    pass


def after_trading_end(context):
    #log.info("==> after trading end @ %s", str(context.current_dt))
    g.trade_stat.report(context)

    # 得到当前未完成订单
    orders = get_open_orders()
    for _order in orders.values():
        log.info("canceled uncompleted order: %s" % (_order.order_id))
    pass


def initialize(context):
    log.info("==> initialize @ %s", str(context.current_dt))

    # 设置手续费率
    set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0013, min_cost=5))
    # 设置基准指数：沪深300指数 '000300.XSHG'
    set_benchmark('000300.XSHG')
    # 使用真实价格回测(模拟盘推荐如此，回测请注释)
    set_option('use_real_price', True)

    g.period = 10  # 调仓频率，单位：日
    g.day_count = 0  # 调仓日计数器，单位：日

    # 配置选股参数
    g.selected_stock_count = 100  # 备选股票数目
    g.buy_stock_count = 5  # 买入股票数目

    # 配置是否根据市盈率选股
    # 此回测如果不按pe选股，收益更高，回撤也稍大，个人取舍
    g.select_by_pe = True
    if g.select_by_pe:
        g.max_pe = 200
        g.min_pe = 2

    g.filter_gem = True  # 配置是否过滤创业板股票
    g.filter_blacklist = False  # 配置是否过滤黑名单股票，回测建议关闭，模拟运行时开启

    # 输出各类参数
    log.info("调仓日频率: %d 日" % (g.period))
    log.info("备选股票数目: %d" % (g.selected_stock_count))
    log.info("购买股票数目: %d" % (g.buy_stock_count))
    log.info("是否根据PE选股: %s" % (g.select_by_pe))
    if g.select_by_pe:
        log.info("最大PE: %s" % (g.max_pe))
        log.info("最小PE: %s" % (g.min_pe))

    log.info("是否过滤创业板股票: %s" % (g.filter_gem))
    log.info("是否过滤黑名单股票: %s" % (g.filter_blacklist))
    if g.filter_blacklist:
        log.info("当前股票黑名单：%s" % str(get_blacklist()))

    # 加载统计模块
    g.trade_stat = tradestat.trade_stat()

    # 每天下午14:52执行
    run_daily(do_handle_data, '14:52')


'''
# 按分钟回测
def handle_data(context, data):
    # 获得当前时间
    hour = context.current_dt.hour
    minute = context.current_dt.minute

    # 每天下午14:53调仓
    if hour == 14 and minute == 53:
    '''


def do_handle_data(context):
    log.info("调仓日计数 [%d]" % (g.day_count))

    # 回看指数前20天的涨幅
    hs300 = '000300.XSHG'  # 沪深300指数，表示二，大盘股
    zz500 = '000905.XSHG'  # 中证500指数，表示八，小盘股
    gr_hs300 = get_growth_rate(hs300)
    gr_zz500 = get_growth_rate(zz500)
    log.info("当前沪深300指数的20日涨幅 [%.2f%%]" % (gr_hs300 * 100))
    log.info("当前中证500指数的20日涨幅 [%.2f%%]" % (gr_zz500 * 100))

    # 前20日两指数涨幅均小于0，卖出所有持仓股票
    #
    # 如果跌停没有卖出，则第二天策略执行时继续根据大盘判定该卖则卖，如果第二天继
    # 续跌，还是多吃了一个跌
    #
    # 前20日若有一个指数涨幅大于0，买入靠前的小市值股票
    if gr_hs300 <= 0 and gr_zz500 <= 0:
        if context.portfolio.positions:
            clear_position(context)
        g.day_count = 0
    else:  #if  ret_hs300 > 0 or ret_zz500 > 0:
        if g.day_count % g.period == 0:
            log.info("==> 满足条件进行调仓")
            buy_stocks = select_stocks(context)
            log.info("选股后可买股票: %s" % (buy_stocks))
            adjust_position(context, buy_stocks)
        g.day_count += 1


# 获取股票n日以来涨幅，根据当前价计算
# n 默认20日
def get_growth_rate(security, n=20):
    lc = get_close_price(security, n)
    #c = data[security].close
    c = get_close_price(security, 1, '1m')
    return (c - lc) / lc


# 获取前n个单位时间当时的收盘价
def get_close_price(security, n, unit='1d'):
    return attribute_history(security, n, unit, ('close'), True)['close'][0]


# 自定义下单
# 根据Joinquant文档，当前报单函数都是阻塞执行，报单函数（如order_target_value）返回即表示报单完成
# 报单成功并全部成交，返回True
# 报单失败或者报单成功但被取消，返回False
def order_target_value_(security, value):
    if value == 0:
        log.debug("Selling out %s" % (security))
    else:
        log.debug("Order %s to value %f" % (security, value))

    # 如果股票停牌，创建报单会失败，order_target_value 返回False
    # 如果股票涨跌停，创建报单会成功，order_target_value 返回True，但是报单会取消
    order = order_target_value(security, value)
    if order != None and order.status == OrderStatus.held:
        return True
    else:
        return False


# 开仓，买入指定价值的证券
def open_position(security, value):
    return order_target_value_(security, value)


# 平仓，卖出指定持仓
def close_position(position):
    # 平仓成功后立即统计更新盈亏
    security = position.security
    if order_target_value_(security, 0):  # 可能会因停牌失败
        g.trade_stat.watch(security, position)
        return True
    return False


# 清空卖出所有持仓
def clear_position(context):
    log.info("==> 清仓，卖出所有股票")
    for stock in context.portfolio.positions.keys():
        position = context.portfolio.positions[stock]
        close_position(position)


# 过滤停牌、ST类股票及其他具有退市标签的股票
def filter_paused_and_st_stock(stock_list):
    current_data = get_current_data()
    return [stock for stock in stock_list
            if not current_data[stock].paused and not current_data[stock].is_st
            and 'ST' not in current_data[stock].name and '*' not in
            current_data[stock].name and '退' not in current_data[stock].name]


# 过滤涨停的股票
def filter_limitup_stock(context, stock_list):
    last_prices = history(
        1, unit='1m', field='close', security_list=stock_list)
    current_data = get_current_data()

    # 已存在于持仓的股票即使涨停也不过滤，避免此股票再次可买，但因被过滤而导致选择别的股票
    return [stock for stock in stock_list
            if stock in context.portfolio.positions.keys() or last_prices[
                stock][-1] < current_data[stock].high_limit]


# 过滤跌停的股票
def filter_limitdown_stock(context, stock_list):
    last_prices = history(
        1, unit='1m', field='close', security_list=stock_list)
    current_data = get_current_data()

    return [stock for stock in stock_list
            if stock in context.portfolio.positions.keys() or last_prices[
                stock][-1] > current_data[stock].low_limit]
    #return [stock for stock in stock_list if last_prices[stock][-1] > current_data[stock].low_limit]


    # 过滤黑名单股票
def filter_blacklist_stock(context, stock_list):
    blacklist = get_blacklist()
    return [stock for stock in stock_list if stock not in blacklist]


# 过滤创业版股票
def filter_gem_stock(context, stock_list):
    return [stock for stock in stock_list if stock[0:3] != '300']


# 过滤20日增长率为负的股票
def filter_by_growth_rate(stock_list, n):
    return [stock for stock in stock_list if get_growth_rate(stock, n) > 0]


# 选股
# 选取指定数目的小市值股票，再进行过滤，最终挑选指定可买数目的股票
def select_stocks(context):
    q = None
    if g.select_by_pe:
        q = query(valuation.code).filter(
            valuation.pe_ratio > g.min_pe,
            valuation.pe_ratio < g.max_pe).order_by(valuation.market_cap.asc(
            )).limit(g.selected_stock_count)
    else:
        q = query(valuation.code).order_by(valuation.market_cap.asc()).limit(
            g.selected_stock_count)

    df = get_fundamentals(q)
    stock_list = list(df['code'])

    if g.filter_gem:
        stock_list = filter_gem_stock(context, stock_list)

    if g.filter_blacklist:
        stock_list = filter_blacklist_stock(context, stock_list)

    stock_list = filter_paused_and_st_stock(stock_list)
    stock_list = filter_limitup_stock(context, stock_list)
    stock_list = filter_limitdown_stock(context, stock_list)

    # 根据20日股票涨幅过滤效果不好，故注释
    #stock_list = filter_by_growth_rate(stock_list, 15)

    # 选取指定可买数目的股票
    stock_list = stock_list[:g.buy_stock_count]
    return stock_list


# 根据待买股票创建或调整仓位
# 对于因停牌等原因没有卖出的股票则继续持有
# 始终保持持仓数目为g.buy_stock_count
def adjust_position(context, buy_stocks):
    for stock in context.portfolio.positions.keys():
        if stock not in buy_stocks:
            log.info("stock [%s] in position is not buyable" % (stock))
            position = context.portfolio.positions[stock]
            close_position(position)
        else:
            log.info("stock [%s] is already in position" % (stock))

    # 根据股票数量分仓
    # 此处只根据可用金额平均分配购买，不能保证每个仓位平均分配
    position_count = len(context.portfolio.positions)
    if g.buy_stock_count > position_count:
        value = context.portfolio.cash / (g.buy_stock_count - position_count)

        for stock in buy_stocks:
            if context.portfolio.positions[stock].total_amount == 0:
                if open_position(stock, value):
                    if len(context.portfolio.positions) == g.buy_stock_count:
                        break
