#!/usr/bin/env python
# -*- coding: utf-8 -*-

import inspect

import talib as ta
import numpy as np
from talib.abstract import Function


def get_ta_functions():
    func_groups = ['Volume Indicators', 'Volatility Indicators',
                   'Overlap Studies', 'Momentum Indicators']
    func_names = [func_name
                  for g in func_groups
                  for func_name in ta.get_function_groups()[g]]
    funcs = {func_name: Function(func_name) for func_name in func_names}
    return funcs


def get_default_args(func):
    """
    returns a dictionary of arg_name:default_values for the input function
    """
    args, varargs, keywords, defaults = inspect.getargspec(func)
    if defaults:
        ret = dict(zip(reversed(args), reversed(defaults)))
        # 本来函数的default应该是周期，是整型.
        # 比如ret={'timeperiod1': 14, timeperiod2: 20}
        # 但是有一些函数的缺省值是字符串。这些函数
        # 是为了方便，可以使用不同的price来计算.
        # 比如TMA(prices, timeperiod=14, price='high')
        # 我们要去掉这些字符型的字典项
        numeric_value_dict = {
            key: val
            for key, val in ret.iteritems() if isinstance(val, int)
        }
        return numeric_value_dict
    else:
        return {'None': None}


def num_bars_to_accumulate(func_name,
                           timeperiod=np.nan,
                           timeperiod1=np.nan,
                           timeperiod2=np.nan,
                           timeperiod3=np.nan,
                           timeperiod4=np.nan):
    tables = {
        'ACC': timeperiod * 2 + 1,
        'ACD': timeperiod,
        'ADTM': timeperiod,
        'AR': timeperiod,
        'ARC': timeperiod * 2 + 1,
        'ASI': timeperiod + 1,
        'BIAS': timeperiod,
        'BR': timeperiod,
        'CMF': timeperiod,
        'CR': timeperiod,
        'CVI': 2 * timeperiod,
        'DDI': timeperiod + 1,
        'DPO': timeperiod,
        'IMI': timeperiod,
        'MI': (timeperiod - 1) * 3 + 1,
        'MTM': timeperiod,
        'QST': timeperiod,
        'TMA': timeperiod,
        'TS': timeperiod,
        'UI': timeperiod * 2 - 1,
        # 'UPN'  : None,
        'VAMA': timeperiod,
        'VHF': timeperiod + 1,
        'VIDYA': timeperiod + 1,
        'VR': timeperiod,
        'VROC': timeperiod + 1,
        'VRSI': 1,
        'WAD': 1,
        # =============================================== 4 个周期
        'BBI': max(timeperiod1, timeperiod2, timeperiod3, timeperiod4),
        # =============================================== 3 个周期
        'SMI': timeperiod1 + timeperiod2 + timeperiod3 - 2,
        'VMACD': timeperiod2 + timeperiod3 - 1,
        'DBCD': timeperiod1 + timeperiod2 + timeperiod3 - 1,
        # ============================================== 2 个周期
        'VOSC': max(timeperiod1, timeperiod2),
        'RVI': timeperiod1 + timeperiod2 + 1,
        'TSI': timeperiod1 + timeperiod2,
        'SRSI': timeperiod1 + timeperiod2,
        'DMI': timeperiod1 + timeperiod2 - 1,
        'RI': timeperiod1 + timeperiod2 - 1,
        'VO': max(timeperiod1, timeperiod2),
        'RMI': timeperiod1 + timeperiod2 + 1,
        'PFE': timeperiod1 + timeperiod2
    }

    return tables[func_name]


if __name__ == '__main__':
    print num_bars_to_accumulate('ACC')
    print get_ta_functions()
