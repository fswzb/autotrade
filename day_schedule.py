# coding=utf-8
import schedule
from helpers.quotes import *
from gevent.pool import Pool
process_pool = Pool()


def day_task():
    gevent.sleep(0.1)
    process_pool.apply(today_all)
    process_pool.apply(top)
    process_pool.apply(get_code_list)
    process_pool.apply(get_hist_data_all)
    process_pool.apply(get_data_all)
    process_pool.apply(classification)
    process_pool.apply(macro)
    process_pool.apply(reference)
    process_pool.apply(fundamental)
    process_pool.join()


if __name__ == '__main__':
    #day_task()
    schedule.every().day.at('15:01').do(day_task)
    while True:
        schedule.run_pending()
        gevent.sleep(0.1)
