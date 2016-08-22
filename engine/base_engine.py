# coding: utf-8
from threading import Thread

from engine.event_engine import Event
import time
import gevent
from gevent import monkey
monkey.patch_all()


class BaseEngine:
    """行情推送引擎基类"""
    EventType = 'base'
    PushInterval = 1

    def __init__(self, event_engine, clock_engine):
        self.event_engine = event_engine
        self.clock_engine = clock_engine
        self.is_pause = not clock_engine.is_tradetime_now()
        self.is_active = True
        self.quotation_thread = Thread(
            target=self.push_quotation,
            name="QuotationEngine.%s" % self.EventType)
        self.quotation_thread.setDaemon(False)
        self.init()

    def start(self):
        self.quotation_thread.start()

    def stop(self):
        self.is_active = False

    def push_quotation(self):
        while self.is_active:
            try:
                response_data = self.fetch_quotation()
            except Exception as e:
                time.sleep(self.PushInterval)
                continue
            event = Event(event_type=self.EventType, data=response_data)
            self.event_engine.put(event)
            time.sleep(self.PushInterval)

    def fetch_quotation(self):
        # return your quotation
        return None

    def init(self):
        # do something init
        pass

    def wait(self):
        interval = self.PushInterval
        if interval < 1:
            gevent.sleep(interval)
            return
        else:
            gevent.sleep(self.PushInterval - int(interval))
            interval = int(interval)
            while interval > 0 and self.is_active:
                gevent.sleep(1)
                interval -= 1
