# coding:utf8
import logging
from logging.handlers import RotatingFileHandler

import sys, os
import traceback

log_common = {
    'mode': 'a+',
    'maxBytes': 1073741824,  #1G
    'backupCount': 5
}


def print_stack():
    ex_type, value, tb = sys.exc_info()
    errorlist = [line.lstrip()
                 for line in traceback.format_exception(ex_type, value, tb)]
    errorlist.reverse()
    return '\n' + ''.join(errorlist)


log_dir = os.path.dirname('./logs/debug.log')
if not os.path.isdir(log_dir):
    os.makedirs(log_dir, 0777)
log = logging.getLogger('trade')
log.setLevel(logging.DEBUG)

fmt = logging.Formatter(
    '%(asctime)s [%(levelname)s] %(filename)s %(lineno)s: %(message)s')
handler = RotatingFileHandler('./logs/debug.log', **log_common)
log.addHandler(handler)
