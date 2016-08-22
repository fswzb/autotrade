# coding: utf-8

from engine.base_engine import BaseEngine
from helpers.quotes import get_realtime_quotes, get_realtime_index, get_realtime_class_index
from gevent import monkey
monkey.patch_all()


class DefaultQuotationEngine(BaseEngine):
    """行情推送引擎"""
    EventType = 'quotation'

    def init(self):
        self.stock_codes = ['sh','000002','000839']

    def fetch_quotation(self):
        return get_realtime_quotes(self.stock_codes)
