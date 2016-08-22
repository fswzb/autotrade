# coding: utf-8

from engine.main_engine import MainEngine
from engine.quotation_engine import DefaultQuotationEngine
DefaultQuotationEngine.PushInterval = 10  # 改为 30s 推送一次
broker = 'yjb'
m = MainEngine(broker=broker, quotation_engines=[DefaultQuotationEngine])
m.is_watch_strategy = True  # 策略文件出现改动时,自动重载,不建议在生产环境下使用
m.load_strategy(names=['test'])
m.start()
