# coding=utf-8
import logging

from helpers.log import log
from order.gftrader import GFTrader
from order.httrader import HTTrader
from order.xqtrader import XueQiuTrader
from order.yhtrader import YHTrader
from order.yjbtrader import YJBTrader


def use(broker, debug=True, **kwargs):
    """用于生成特定的券商对象
    :param broker:券商名支持 ['ht', 'HT'] ['yjb', 'YJB'] ['yh', 'YH'] ['gf', 'GF']
    :param debug: 控制 debug 日志的显示, 默认为 True
    :param remove_zero: ht 可用参数，是否移除 08 账户开头的 0, 默认 True
    :return the class of trader

    Usage::
        >>> user = trade.use('ht')
        >>> user.prepare('ht.json')
    """
    if not debug:
        log.handlers = [logging.NullHandler()]
    if broker.lower() in ['ht', 'HT']:
        return HTTrader(**kwargs)
    if broker.lower() in ['yjb', 'YJB']:
        return YJBTrader()
    if broker.lower() in ['yh', 'YH']:
        return YHTrader()
    if broker.lower() in ['xq', 'XQ']:
        return XueQiuTrader()
    if broker.lower() in ['gf', 'GF']:
        return GFTrader()
