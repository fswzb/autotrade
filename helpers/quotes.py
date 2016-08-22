#!/usr/bin/python
# coding: utf-8
import MySQLdb
import datetime
from configs import common_mysql_config
import tushare as ts
import datetime as dt
import gevent
from gevent.threadpool import ThreadPool
import requests
thread_pool = ThreadPool(maxsize=50)
engine = MySQLdb.connect(**common_mysql_config)


def get_code_list():
    stock_basic = ts.get_stock_basics()
    stock_basic.to_sql(
        'stock_basics', engine, flavor='mysql', if_exists='replace')

    stock_timetomarket = stock_basic['timeToMarket']
    stock_timetomarket = stock_timetomarket.map(
        lambda x: x != 0 and dt.datetime.strptime(str(x), '%Y%m%d').strftime('%Y-%m-%d'))
    stock_timetomarket.sort_values(ascending=False, inplace=True)
    if stock_timetomarket is None:
        return
    max = len(stock_timetomarket.index)
    code_list = []
    for item in xrange(max):
        code_list.append(stock_timetomarket.index[item])
    return code_list


def get_data(code, start=None):
    if start is None:
        start = datetime.datetime.today().strftime('%Y-%m-%d')
    try:
        gevent.sleep(0.2)
        dayhistory = ts.get_h_data(
            code=code, start=start, retry_count=8, pause=3)
        if dayhistory is None:
            return
        dayhistory['code'] = code
        dayhistory.to_sql('h_data', engine, flavor='mysql', if_exists='append')
    except Exception as e:
        pass


def get_his_data(code, start=None):
    try:
        gevent.sleep(0.1)
        if start is None:
            dayhistory = ts.get_hist_data(
                code=code, retry_count=8, pause=3, ktype='D')
        else:
            dayhistory = ts.get_hist_data(
                code=code, start=start, retry_count=8, pause=3, ktype='D')
        if dayhistory is None:
            return
        dayhistory['code'] = code
        dayhistory.to_sql(
            'hist_data', engine, flavor='mysql', if_exists='append')
    except Exception as e:
        pass


def get_hist_data_all():
    code_list = get_code_list()
    thread_pool.map(get_his_data, code_list)
    thread_pool.join()


def get_data_all():
    code_list = get_code_list()
    thread_pool.map(get_data, code_list)
    thread_pool.join()


def classification_type(class_types):
    if class_types == 'classification_industry':
        industry_classified = ts.get_industry_classified('sw')
        industry_classified.to_sql(
            'classification_industry',
            engine,
            flavor='mysql',
            if_exists='replace')
    elif class_types == 'concept':
        concept_classified = ts.get_concept_classified()
        concept_classified.to_sql(
            'classification_concept',
            engine,
            flavor='mysql',
            if_exists='replace')
    elif class_types == 'area':
        area_classified = ts.get_area_classified()
        area_classified.to_sql(
            'classification_area', engine, flavor='mysql', if_exists='replace')
    elif class_types == 'sme':
        sme_classified = ts.get_sme_classified()
        sme_classified.to_sql(
            'classification_sme', engine, flavor='mysql', if_exists='replace')
    elif class_types == 'gem':
        gem_classified = ts.get_gem_classified()
        gem_classified.to_sql(
            'classification_gem', engine, flavor='mysql', if_exists='replace')
    elif class_types == 'st':
        st_classified = ts.get_st_classified()
        st_classified.to_sql(
            'classification_st', engine, flavor='mysql', if_exists='replace')
    elif class_types == 'hs300':
        hs300s = ts.get_hs300s()
        hs300s.to_sql(
            'classification_hs300s',
            engine,
            flavor='mysql',
            if_exists='replace')
    elif class_types == 'sz50':
        sz50s = ts.get_sz50s()
        sz50s.to_sql(
            'classification_sz50s',
            engine,
            flavor='mysql',
            if_exists='replace')
    elif class_types == 'zz500':
        zz500s = ts.get_zz500s()
        zz500s.to_sql(
            'classification_zz500s',
            engine,
            flavor='mysql',
            if_exists='replace')
    elif class_types == 'terminated':
        terminated = ts.get_terminated()
        terminated.to_sql(
            'classification_terminated',
            engine,
            flavor='mysql',
            if_exists='replace')
    elif class_types == 'suspended':
        suspended = ts.get_suspended()
        suspended.to_sql(
            'classification_suspended',
            engine,
            flavor='mysql',
            if_exists='replace')


def classification():
    class_types = ['industry', 'concept', 'area', 'sme', 'gem', 'st', 'hs300',
                   'sz50', 'zz500', 'terminated', 'suspended']

    thread_pool.map(classification_type, class_types)
    thread_pool.join()


def macro_type(macros_type):
    if macros_type == 'deposit_rate':
        deposit_rate = ts.get_deposit_rate()
        if deposit_rate is not None:
            deposit_rate.to_sql(
                'macros_deposit_rate',
                engine,
                flavor='mysql',
                if_exists='replace')
    elif macros_type == 'loan_rate':
        loan_rate = ts.get_loan_rate()
        if loan_rate is not None:
            loan_rate.to_sql(
                'macros_loan_rate',
                engine,
                flavor='mysql',
                if_exists='replace')
    elif macros_type == 'rrr':
        rrr = ts.get_rrr()
        if rrr is not None:
            rrr.to_sql(
                'macros_rrr', engine, flavor='mysql', if_exists='replace')
    elif macros_type == 'money_supply':
        money_supply = ts.get_money_supply()
        if money_supply is not None:
            money_supply.to_sql(
                'macros_money_supply',
                engine,
                flavor='mysql',
                if_exists='replace')
    elif macros_type == 'money_supply_bal':
        money_supply_bal = ts.get_money_supply_bal()
        if money_supply_bal is not None:
            money_supply_bal.to_sql(
                'macros_money_supply_bal',
                engine,
                flavor='mysql',
                if_exists='replace')
    elif macros_type == 'gdp_year':
        gdp_year = ts.get_gdp_year()
        if gdp_year is not None:
            gdp_year.to_sql(
                'macros_gdp_year', engine, flavor='mysql', if_exists='replace')
    elif macros_type == 'gdp_quater':
        gdp_quater = ts.get_gdp_quarter()
        if gdp_quater is not None:
            gdp_quater.to_sql(
                'macros_gdp_quater',
                engine,
                flavor='mysql',
                if_exists='replace')
    elif macros_type == 'gdp_for':
        gdp_for = ts.get_gdp_for()
        if gdp_for is not None:
            gdp_for.to_sql(
                'macros_gdp_for', engine, flavor='mysql', if_exists='replace')
    elif macros_type == 'gdp_pull':
        gdp_pull = ts.get_gdp_pull()
        if gdp_pull is not None:
            gdp_pull.to_sql(
                'macros_gdp_pull', engine, flavor='mysql', if_exists='replace')
    elif macros_type == 'gdp_contrib':
        gdp_contrib = ts.get_gdp_contrib()
        if gdp_contrib is not None:
            gdp_contrib.to_sql(
                'macros_gdp_contrib',
                engine,
                flavor='mysql',
                if_exists='replace')
    elif macros_type == 'cpi':
        cpi = ts.get_cpi()
        if cpi is not None:
            cpi.to_sql(
                'macros_cpi', engine, flavor='mysql', if_exists='replace')
    elif macros_type == 'ppi':
        ppi = ts.get_ppi()
        if ppi is not None:
            ppi.to_sql(
                'macros_ppi', engine, flavor='mysql', if_exists='replace')


def macro():
    macro_types = ['ppi', 'cpi', 'gdp_contrib', 'gdp_pull', 'gdp_for',
                   'gdp_quater', 'gdp_year', 'money_supply_bal',
                   'money_supply', 'rrr', 'loan_rate', 'deposit_rate']
    thread_pool.map(macro_type, macro_types)
    thread_pool.join()


def top_type(top_type):
    today = datetime.datetime.today().strftime('%Y-%m-%d')
    if top_type == 'top_list':
        top_list = ts.top_list(today)
        if top_list is not None:
            top_list.to_sql(
                'top_list', engine, flavor='mysql', if_exists='append')
    elif top_type == 'cap_tops':
        cap_tops = ts.cap_tops()
        if cap_tops is not None:
            cap_tops['date'] = today
            cap_tops.to_sql(
                'top_cap_tops', engine, flavor='mysql', if_exists='append')
    elif top_type == 'broker_tops':
        broker_tops = ts.broker_tops()
        if broker_tops is not None:
            broker_tops['date'] = today
            broker_tops.to_sql(
                'top_broker_tops', engine, flavor='mysql', if_exists='append')
    elif top_type == 'inst_tops':
        inst_tops = ts.inst_tops()
        if inst_tops is not None:
            inst_tops['date'] = today
            inst_tops.to_sql(
                'top_inst_tops', engine, flavor='mysql', if_exists='append')
    elif top_type == 'inst_detail':
        inst_detail = ts.inst_detail()
        if inst_detail is not None:
            inst_detail.to_sql(
                'top_inst_detail', engine, flavor='mysql', if_exists='append')


def top():
    class_types = ['top_list', 'cap_tops', 'broker_tops', 'inst_tops',
                   'inst_detail']
    thread_pool.map(top_type, class_types)
    thread_pool.join()


def reference(year_to_start=2010):
    def profit_data(year):
        profit_data = ts.profit_data(year=year, top=100)
        profit_data.sort('shares', ascending=False)
        if profit_data is not None:
            profit_data.to_sql(
                'reference_profit_data',
                engine,
                flavor='mysql',
                if_exists='append')

    def forecast_data(year):
        for i in range(4):
            predts = ts.forecast_data(year, i + 1)
            if predts is not None:
                predts.to_sql(
                    'reference_forecast_data',
                    engine,
                    flavor='mysql',
                    if_exists='append')

    def fund_holdings(year):
        for i in range(4):
            predts = ts.fund_holdings(year, i + 1)
            if predts is not None:
                predts.to_sql(
                    'reference_fund_holdings',
                    engine,
                    flavor='mysql',
                    if_exists='append')

    starttime = datetime.datetime.today()
    year = [year_to_start + i
            for i in range(starttime.year - year_to_start + 1)]
    thread_pool.map(profit_data, year)
    thread_pool.map(forecast_data, year)
    thread_pool.map(fund_holdings, year)
    thread_pool.join()

    xsg_data = ts.xsg_data()
    if xsg_data is not None:
        xsg_data.to_sql(
            'reference_xsg_data', engine, flavor='mysql', if_exists='replace')

    new_stocks = ts.new_stocks()
    if new_stocks is not None:
        new_stocks.to_sql(
            'reference_new_stocks',
            engine,
            flavor='mysql',
            if_exists='replace')


def fundamental(year_to_start=2010):
    def report_data(year):
        for i in range(4):
            quarter = i + 1
            predts = ts.get_report_data(year, quarter)
            if predts is not None:
                predts['year'] = year
                predts['quarter'] = quarter
                predts.to_sql(
                    'fundamental_report_data',
                    engine,
                    flavor='mysql',
                    if_exists='append')

    def profit_data(year):
        for i in range(4):
            quarter = i + 1
            predts = ts.get_profit_data(year, quarter)
            if predts is not None:
                predts['year'] = year
                predts['quarter'] = quarter
                predts.to_sql(
                    'fundamental_profit_data',
                    engine,
                    flavor='mysql',
                    if_exists='append')

    def operation_data(year):
        for i in range(4):
            quarter = i + 1
            predts = ts.get_operation_data(year, quarter)
            if predts is not None:
                predts['year'] = year
                predts['quarter'] = quarter
                predts.to_sql(
                    'fundamental_operation_data',
                    engine,
                    flavor='mysql',
                    if_exists='append')

    def debtpaying_data(year):
        for i in range(4):
            quarter = i + 1
            predts = ts.get_debtpaying_data(year, quarter)
            if predts is not None:
                predts['year'] = year
                predts['quarter'] = quarter
                predts.to_sql(
                    'fundamental_debtpaying_data',
                    engine,
                    flavor='mysql',
                    if_exists='append')

    def cashflow_data(year):
        for i in range(4):
            quarter = i + 1
            predts = ts.get_cashflow_data(year, quarter)
            if predts is not None:
                predts['year'] = year
                predts['quarter'] = quarter
                predts.to_sql(
                    'fundamental_cashflow_data',
                    engine,
                    flavor='mysql',
                    if_exists='append')

    def growth_data(year):
        for i in range(4):
            quarter = i + 1
            predts = ts.get_growth_data(year, quarter)
            if predts is not None:
                predts['year'] = year
                predts['quarter'] = quarter
                predts.to_sql(
                    'fundamental_growth_data',
                    engine,
                    flavor='mysql',
                    if_exists='append')

    starttime = datetime.datetime.today()
    year = [year_to_start + i
            for i in range(starttime.year - year_to_start + 1)]
    thread_pool.map(report_data, year)
    thread_pool.map(profit_data, year)
    thread_pool.map(operation_data, year)
    thread_pool.map(debtpaying_data, year)
    thread_pool.map(cashflow_data, year)
    thread_pool.map(growth_data, year)
    thread_pool.join()


def get_hist_data(code, start=None, end=None, ktype='D'):
    '''

    :param code: sh:获取上证指数k线数据 sz:获取深圳成指k线数据 hs300:获取沪深300指数k线数据 sz50:获取上证50指数k线数据
                 zxb:获取中小板指数k线数据 cyb:获取创业板指数k线数据
    :param ktype: D:获取日k线数据 W:获取周k线数据 M:获取月k线数据 5:获取5分钟k线数据 15:获取15分钟k线数据
                30:获取30分钟k线数据 60:获取60分钟k线数据
    '''
    if start is None:
        start = datetime.datetime.today().strftime('%Y-%m-%d')
    if end is None:
        end = datetime.datetime.today().strftime('%Y-%m-%d')
    df = ts.get_hist_data(code=code, start=start, end=end, ktype=ktype)
    df['code'] = code
    return df


def today_all():
    df = ts.get_today_all()
    df['date'] = datetime.datetime.today().strftime('%Y-%m-%d')
    df.to_sql('today_all', engine, flavor='mysql', if_exists='append')


def get_realtime_quotes(code_list):
    return ts.get_realtime_quotes(code_list)


def get_realtime_index():
    return ts.get_realtime_quotes(['sh', 'sz', 'hs300', 'sz50', 'zxb', 'cyb'])


def get_realtime_class_index():
    return ts.get_index()


#市场涨跌统计
def market_stat():
    r = requests.get(
        url='http://home.flashdata2.jrj.com.cn/limitStatistic/market.js')
    market = eval(r.text.replace('var market=', '').replace(';', ''))
    return market


#涨停统计
def zt_stat():
    r = requests.get(
        url='http://home.flashdata2.jrj.com.cn/limitStatistic/zt.js')
    zt = eval(r.text.replace('var zr_zt=', '').replace(';', ''))
    return zt


#跌停统计
def dt_stat():
    r = requests.get(
        url='http://home.flashdata2.jrj.com.cn/limitStatistic/dt.js')
    dt = eval(r.text.replace('var zr_dt=', '').replace(';', ''))
    return dt


#一字板涨停统计
def yzbzt_stat():
    r = requests.get(
        url='http://home.flashdata2.jrj.com.cn/limitStatistic/yzbzt.js')
    yzbzt = eval(r.text.replace('var yzb_zt=', '').replace(';', ''))
    return yzbzt


#涨停强度
def ztforce_stat(day=None):
    if day is None:
        day = datetime.datetime.today().strftime('%Y%m%d')
    r = requests.get(
        url='http://home.flashdata2.jrj.com.cn/limitStatistic/ztForce/' + day +
        '.js')
    zt_force = r.text.replace('var yzb_ztForce=','').replace(';','').replace('size','"size"') \
        .replace('"column":{stockcode:0,stockname:1,nowPrice:2,priceLimit:3,fcb:4,flb:5,fdMoney:6,firstZtTime:7,lastZtTime:8,opentime:9,zhenfu:10,force : 11},','') \
        .replace('time','"time"')
    return eval(zt_force)


#昨日涨停股今日表现
def zrztjrbx_stat(day=None):
    if day is None:
        day = datetime.datetime.today().strftime('%Y%m%d')
    r = requests.get(
        url='http://hqdata.jrj.com.cn/zrztjrbx/history/' + day + '.js')
    zrztjrbx = r.text.replace('var min_performance=','').replace(';','') \
        .replace('dot:','"dot":').replace('pl:','"pl":').replace('ztsize:','"ztsize":')
    return eval(zrztjrbx)


#具体个股昨日涨停股今日表现
def zrztjrbx_limitup():
    r = requests.get(url='http://hqdata.jrj.com.cn/zrztjrbx/limitup.js')
    text = r.text.replace('var stock_performance=', '').replace(';', '').replace(
        '"Column":{index:0,stockcode:1,stockname:2,lastzttime:3,nowprice:4,pricelimit:5,highlimit:6,lowlimit:7,iscon:8,conztnums:9,lastforce:10,todayforce:11,isstop:12,lasttradedate:13,lastcloseprice:14},',
        '')
    return eval(text)


#领涨行业
def leader_industry():
    r = requests.get(
        url='http://q.jrjimg.cn/?q=cn|bk|7&n=leaderindustry&c=l&o=pl,d&p=1020')
    res = r.text.replace('var leaderindustry=','').replace(';','').replace('mstat','"mstat"') \
        .replace('page','"page"').replace('"page"s','"pages"').replace('total','"total"') \
        .replace('Summary','"Summary"').replace('HqData','"HqData"') \
        .replace('Column:{id:0,code:1,name:2,hqtime:3,lcp:4,op:5,np:6,ta:7,tm:8,hlp:9,pl:10,time:11,type:12,scnt:13,pusc:14,pmsc:15,pdsc:16,sid:17,scode:18,sname:19,snp:20,sta:21,stm:22,shlp:23,spl:24},','') \
        .replace('hqtime','"hqtime"')
    return eval(res)


#领涨概念&对应的概念龙头股
def leader_concept():
    r = requests.get(
        url='http://stock.jrj.com.cn/action/concept/queryConceptHQ.jspa?sort=todayPl&vname=desc&order=desc&pn=1&ps=50')
    res = r.text.replace('var desc=', '').replace(';', '')
    return eval(res)


#5分钟异动
def yd_stock():
    r = requests.get(
        url='http://q.jrjimg.cn/?q=cn|s|sa&c=s,ta,tm,sl,cot,cat,ape,min5pl&n=hqa&o=min5pl,d&p=1020')
    res = r.text.replace('var hqa=', '').replace(';', '').replace('Summary','"Summary"').replace('HqData','"HqData"') \
        .replace('mstat','"mstat"').replace('page','"page"').replace('"page"s','"pages"').replace('total','"total"').replace('hqtime','"hqtime"') \
        .replace('Column:{id:0,code:1,name:2,lcp:3,stp:4,np:5,ta:6,tm:7,hlp:8,pl:9,sl:10,cat:11,cot:12,tr:13,ape:14,min5pl:15},','')
    return eval(res)


#量比排行
def liangbi_stat():
    r = requests.get(
        url='http://q.jrjimg.cn/?q=cn|s|sa&c=s,ta,tm,sl,cot,cat,ape&n=hqa&o=cat,d&p=1020')
    res = r.text.replace('var hqa=', '').replace(';', '').replace('Summary','"Summary"').replace('HqData','"HqData"') \
        .replace('mstat','"mstat"').replace('page','"page"').replace('"page"s','"pages"').replace('total','"total"').replace('hqtime','"hqtime"') \
        .replace('Column:{id:0,code:1,name:2,lcp:3,stp:4,np:5,ta:6,tm:7,hlp:8,pl:9,sl:10,cat:11,cot:12,tr:13,ape:14},','')
    return eval(res)


#资金净流入排行
def zjlr_stat():
    r = requests.get(
        url='http://zj.hqquery.jrj.com.cn/szj.do?vname=ggzjlx&c=code,name,np,pl,zjin,inratio,zlin,zlratio,j2,zdratio,j1,xdratio&zj=in&type=s&day=today&market=cn&page=1&size=60&order=desc&sort=zlin')
    res = r.text.replace('var ggzjlx=', '').replace(';', '').replace('Summary','"Summary"').replace('HqData','"HqData"') \
        .replace('page','"page"').replace('"page"s','"pages"').replace('total','"total"').replace('hqtime','"hqtime"') \
        .replace('Column:{code:0 ,name:1 ,np:2 ,pl:3 ,zjin:4 ,inratio:5 ,zlin:6 ,zlratio:7 ,j2:8 ,zdratio:9 ,j1:10 ,xdratio:11 },','')
    return eval(res)


#资金净流出排行
def zjlc_stat():
    r = requests.get(
        url='http://zj.hqquery.jrj.com.cn/szj.do?vname=ggzjlx&c=code,name,np,pl,zjin,inratio,zlin,zlratio,j2,zdratio,j1,xdratio&zj=out&type=s&day=today&market=cn&page=1&size=60&order=asc&sort=zlin')
    res = r.text.replace('var ggzjlx=', '').replace(';', '').replace('Summary','"Summary"').replace('HqData','"HqData"') \
        .replace('page','"page"').replace('"page"s','"pages"').replace('total','"total"').replace('hqtime','"hqtime"') \
        .replace('Column:{code:0 ,name:1 ,np:2 ,pl:3 ,zjin:4 ,inratio:5 ,zlin:6 ,zlratio:7 ,j2:8 ,zdratio:9 ,j1:10 ,xdratio:11 },','')
    return eval(res)
