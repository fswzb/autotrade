# coding: utf-8
from configs.stock import stock_list
from engine.base_engine import BaseEngine
from helpers.quotes import get_realtime_quotes, get_realtime_index, get_realtime_class_index
from gevent import monkey
monkey.patch_all()

class DefaultQuotationEngine(BaseEngine):
    """行情推送引擎"""
    EventType = 'quotation'
    stock_codes = []
    def init(self):
        self.stock_codes = stock_list

    def fetch_quotation(self):
        return get_realtime_quotes(self.stock_codes)

    def set_stock_codes(self,code_list=None):
        if code_list is not None:
            self.stock_codes = code_list
