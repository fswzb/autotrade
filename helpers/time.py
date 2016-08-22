# coding:utf8

import datetime


def is_weekend(now_time):
    return now_time.weekday() >= 5

#to get the latest trade day
except_trade_day_list=['2015-05-01','2015-06-22','2015-09-03','2015-10-01','2015-10-02','2015-10-06', \
                       '2015-10-07','2015-10-08', '2016-04-04','2016-05-02','2016-06-09','2016-06-10', \
                       '2016-09-15','2016-09-16','2016-10-03','2016-10-04','2016-10-05','2016-10-06', \
                       '2016-10-07','2017-01-02','2017-01-30','2017-01-31','2017-02-01','2017-02-02', \
                       '2017-04-03','2017-05-29','2017-10-02','2017-10-03','2017-10-04','2017-10-05','2017-10-06']


def is_trade_date(given_date_str=None):
    """
    :param given_date_str: str type, like '2017-10-01'
    :return: bool type
    """
    this_day = datetime.datetime.now()
    date_format = '%Y-%m-%d'
    this_str = this_day.strftime(date_format)
    open_str = ' 09:15:00'
    if this_str in except_trade_day_list:
        return False
    return this_day.isoweekday() < 6


def get_latest_trade_date(this_date=None, date_format='%Y-%m-%d'):
    """
    :param this_date: datetime.datetim type, like datetime.datetime.now()
    :return: latest_day_str, str type
    """
    this_day = datetime.datetime.now()
    if this_date != None:
        this_day = this_date
    open_str = ' 09:25:00'
    time_format = date_format + ' %X'
    this_str = this_day.strftime(time_format)
    if (this_day.hour >= 0 and this_day.hour < 9) or (this_day.hour == 9 and
                                                      this_day.minute < 15):
        this_day = datetime.datetime.strptime(
            this_str, time_format) + datetime.timedelta(days=-1)
        this_str = this_day.strftime(date_format)
    latest_day_str = ''
    this_str = this_str[:10]
    while this_str >= '1990-01-01':
        if is_trade_date(this_str):
            return this_str
            #break
        else:
            this_day = this_day + datetime.timedelta(days=-1)
            this_str = this_day.strftime(date_format)


def get_next_trade_date(now_time):
    """
    :param now_time: datetime.datetime
    :return:
    >>> import datetime
    >>> get_next_trade_date(datetime.date(2016, 5, 5))
    datetime.date(2016, 5, 6)
    """
    now = now_time
    max_days = 365
    days = 0
    while 1:
        days += 1
        now += datetime.timedelta(days=1)
        if is_trade_date(now):
            if isinstance(now, datetime.date):
                return now
            else:
                return now.date()
        if days > max_days:
            raise ValueError('无法确定 %s 下一个交易日' % now_time)


OPEN_TIME = ((datetime.time(9, 15, 0), datetime.time(11, 30, 0)),
             (datetime.time(13, 0, 0), datetime.time(15, 0, 0)), )


def is_tradetime(now_time):
    """
    :param now_time: datetime.time()
    :return:
    """
    now = now_time.time()
    for begin, end in OPEN_TIME:
        if begin <= now < end:
            return True
    else:
        return False


PAUSE_TIME = ((datetime.time(11, 30, 0), datetime.time(12, 59, 30)), )


def is_pause(now_time):
    """
    :param now_time:
    :return:
    """
    now = now_time.time()
    for b, e in PAUSE_TIME:
        if b <= now < e:
            return True


CONTINUE_TIME = ((datetime.time(12, 59, 30), datetime.time(13, 0, 0)), )


def is_continue(now_time):
    now = now_time.time()
    for b, e in CONTINUE_TIME:
        if b <= now < e:
            return True
    return False


CLOSE_TIME = (datetime.time(15, 0, 0), )


def is_closing(now_time, start=datetime.time(14, 54, 30)):
    now = now_time.time()
    for close in CLOSE_TIME:
        if start <= now < close:
            return True
    return False
