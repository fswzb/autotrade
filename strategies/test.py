# coding:utf-8
# 引入策略模板
from common.strategyTemplate import StrategyTemplate
import time
import datetime as dt
from dateutil import tz

# 定义策略类
class Strategy(StrategyTemplate):
    name = 'test'  # 定义策略名字

    def init(self):
        # 通过下面的方式来获取时间戳
        now_dt = self.clock_engine.now_dt
        now = self.clock_engine.now
        now = time.time()
        # 注册时钟事件
        clock_type = "盘尾"
        moment = dt.time(14, 56, 30, tzinfo=tz.tzlocal())
        self.clock_engine.register_moment(clock_type, moment)

        # 注册时钟间隔事件, 不在交易阶段也会触发, clock_type == minute_interval
        minute_interval = 1.5
        self.clock_engine.register_interval(minute_interval, trading=False)
        # 进行相关的初始化定义
        self.buy_stocks = []  # 假如一个股票一天只想买入一次。定义一个列表用来存储策略买过的股票

    # 策略函数，收到行情推送后会自动调用
    def strategy(self, event):
        # 使用 self.user 来操作账户
        # 使用 self.log.info('message') 来打印你所需要的 log
        self.log.info('\n\n策略1触发')
        self.log.info('行情数据: 万科价格: %s' % event.data['000002'])
        self.log.info('检查持仓')
        self.log.info(self.user.balance)
        # 在未买入的情况下买入万科
        if '000002' not in self.buy_stocks:
            # self.user.buy('000002')
            self.buy_stocks.append('000002')

    # 时钟引擎，用于推送开市、收市以及其他定时事件
    def clock(self, event):
        """在交易时间会定时推送 clock 事件
        :param event: event.data.clock_event 为 [0.5, 1, 3, 5, 15, 30, 60] 单位为分钟,  ['open', 'close'] 为开市、收市
            event.data.trading_state  bool 是否处于交易时间
        """
        print event.data.trading_state
        if event.data.clock_event == 'open':
            # 开市了
            self.log.info('open')
        elif event.data.clock_event == 'pause':
            #上午休市
            self.log.info('pause')
        elif event.data.clock_event == 'continue':
            #下午开市
            self.log.info('continue')
        elif event.data.clock_event == 'close':
            # 收市了
            self.log.info('close')
            # 收盘时清空已买股票列表 self.buy_stocks
            del self.buy_stocks[:]
        elif event.data.clock_event == 1:
            # 5 分钟的 clock
            self.log.info("1分钟")
