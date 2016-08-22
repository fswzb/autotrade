# coding=utf-8
import gevent
import schedule
from helpers.quotes import get_realtime_class_index, get_realtime_index, get_realtime_quotes
from stragy import *


def task():
    pass
    #tushare get data

    #stragy

    #trade


if __name__ == '__main__':
    schedule.every(1).minutes.do(task)
    while True:
        schedule.run_pending()
        gevent.sleep(0.2)
