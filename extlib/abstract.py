#!/usr/bin/env python
# -*- coding: utf-8 -*-

import inspect

import numpy as np
import talib.abstract as ab

import common

EXT_FUNCTION_NAMES = set(common.__all__)


class Function(ab.Function):
    def __init__(self, func_name, *args, **kwargs):
        """
        :type kwargs: object
        """
        self.__name = func_name.upper()
        self.__parameters = {}

        if self.__name in EXT_FUNCTION_NAMES:
            self.__doc__ = common.__getattribute__(self.__name).__doc__

            # self.parameters = {}
        else:
            super(Function, self).__init__(func_name, *args, **kwargs)

        if kwargs:
            self.parameters = kwargs

    def __call__(self, *args, **kwargs):
        if not self.parameters:
            self.parameters.update(**kwargs)

        if self.__name in EXT_FUNCTION_NAMES:
            func = common.__getattribute__(self.__name)
            return func(*args, **kwargs)
        else:
            return super(Function, self).__call__(*args, **kwargs)

    @property
    def parameters(self):
        if self.__name in EXT_FUNCTION_NAMES:
            return self.__parameters
        else:
            return super(Function, self).parameters

    @parameters.setter
    def parameters(self, parameters):
        if self.__name in EXT_FUNCTION_NAMES:
            self.__parameters.update(parameters)
        else:
            super(Function, self).set_parameters(parameters)

    @property
    def lookback(self):
        if self.__name in EXT_FUNCTION_NAMES:
            kwargs = self.parameters if self.parameters else self.__get_default_args(
                self.__name)
            return self.__lookback(self.__name, **kwargs)
        else:
            return super(Function, self).lookback

    @staticmethod
    def __lookback(func_name, **kwargs):
        param_dict = dict(
            timeperiod=np.nan,
            timeperiod1=np.nan,
            timeperiod2=np.nan,
            timeperiod3=np.nan,
            timeperiod4=np.nan)
        param_dict.update(**kwargs)
        tables = {
            # =====================================0 个周期
            'WC': 0,
            'EMV': 1,
            'PVT': 1,
            'TR': 1,
            'PVI': 0,
            'NVI': 0,
            # =====================================1 个周期
            'ACC': param_dict['timeperiod'] * 2,
            'ACD': param_dict['timeperiod'],
            'ADTM': param_dict['timeperiod'],
            'AR': param_dict['timeperiod'] - 1,
            'ARC': param_dict['timeperiod'] * 2,
            'ASI': param_dict['timeperiod'],
            'BIAS': param_dict['timeperiod'] - 1,
            'BR': param_dict['timeperiod'],
            'CMF': param_dict['timeperiod'] - 1,
            'CR': param_dict['timeperiod'],
            'CVI': 2 * param_dict['timeperiod'] - 1,
            'DDI': param_dict['timeperiod'],
            'DPO': param_dict['timeperiod'] - 1,
            'IMI': param_dict['timeperiod'] - 1,
            'MI': (param_dict['timeperiod'] - 1) * 3,
            'MTM': param_dict['timeperiod'],
            'QST': param_dict['timeperiod'] - 1,
            'TMA': param_dict['timeperiod'] - 1,
            'TS': param_dict['timeperiod'] - 1,
            'UI': param_dict['timeperiod'] * 2 - 2,
            # 'UPN'  : None,
            'VAMA': param_dict['timeperiod'] - 1,
            'VHF': param_dict['timeperiod'],
            'VIDYA': param_dict['timeperiod'],
            'VR': param_dict['timeperiod'] - 1,
            'VROC': param_dict['timeperiod'],
            'VRSI': 1,
            'WAD': 0,
            # =============================================== 4 个周期
            'BBI':
            max(param_dict['timeperiod1'], param_dict['timeperiod2'],
                param_dict['timeperiod3'], param_dict['timeperiod4']) - 1,
            # =============================================== 3 个周期
            'SMI': param_dict['timeperiod1'] + param_dict['timeperiod2'] +
            param_dict['timeperiod3'] - 3,
            'VMACD': max(param_dict['timeperiod1'], param_dict['timeperiod2'])
            + param_dict['timeperiod3'] - 2,
            'DBCD': param_dict['timeperiod1'] + param_dict['timeperiod2'] +
            param_dict['timeperiod3'] - 2,
            'KVO': max(param_dict['timeperiod1'], param_dict['timeperiod2']) +
            param_dict['timeperiod3'] - 2,
            # ============================================== 2 个周期
            'VOSC':
            max(param_dict['timeperiod1'], param_dict['timeperiod2']) - 1,
            'RVI': param_dict['timeperiod1'] + param_dict['timeperiod2'],
            'TSI': param_dict['timeperiod1'] + param_dict['timeperiod2'] - 1,
            'SRSI': param_dict['timeperiod1'] + param_dict['timeperiod2'] - 1,
            'DMI': param_dict['timeperiod1'] + param_dict['timeperiod2'] - 2,
            'RI': param_dict['timeperiod1'] + param_dict['timeperiod2'] - 1,
            'VO':
            max(param_dict['timeperiod1'], param_dict['timeperiod2']) - 1,
            'RMI': param_dict['timeperiod1'] + param_dict['timeperiod2'],
            'PFE': param_dict['timeperiod1'] + param_dict['timeperiod2'] - 1
        }
        return tables[func_name]

    @property
    def default_args(self):
        return self.__get_default_args(self.__name)

    def __get_default_args(self, func_name):
        """
        returns a dictionary of arg_name:default_values for the input function
        """
        func = common.__getattribute__(func_name)
        args, varargs, keywords, defaults = inspect.getargspec(func)
        if defaults:
            ret = dict(list(zip(reversed(args), reversed(defaults))))
            # 本来函数的default应该是周期，是整型.
            # 比如ret={'timeperiod1': 14, timeperiod2: 20}
            # 但是有一些函数的缺省值是字符串。这些函数
            # 是为了方便，可以使用不同的price来计算.
            # 比如TMA(prices, param_dict.timeperiod=14, price='high')
            # 我们要去掉这些字符型的字典项
            numeric_value_dict = {
                key: val
                for key, val in ret.items() if isinstance(val, int)
            }
            return numeric_value_dict
        else:
            # print func_name
            return {}


def test_ls_talib():
    for func_name in EXT_FUNCTION_NAMES:
        dict_param = dict(
            timeperiod=np.random.randint(10, 100, 1)[0],
            timeperiod1=np.random.randint(10, 100, 1)[0],
            timeperiod2=np.random.randint(10, 100, 1)[0],
            timeperiod3=np.random.randint(10, 100, 1)[0],
            timeperiod4=np.random.randint(10, 100, 1)[0]
            # timeperiod1 = np.random.randint(10,100,1),
        )
        func = Function(func_name, **dict_param)
        lookback = func.lookback
        default_args = func.default_args
        real_args = default_args.copy()
        for key, val in real_args.items():
            real_args[key] = dict_param[key]

        print(func_name)
        print(dict_param)
        print(('lookback={0}'.format(lookback)))


def test_talib():
    func_names = list(filter(str.isupper, dir(ab)))
    func_names = [x for x in func_names if not x.startswith('_')]
    print(func_names)
    ad = Function('ADOSC')
    param = {'fastperiod': 20}
    ad.parameters = param
    print((dir(ad)))
    ad.lookback


for name in EXT_FUNCTION_NAMES:
    exec ("%s = Function('%s')" % (name, name))

__all__ = ['Function'] + list(EXT_FUNCTION_NAMES)

if __name__ == '__main__':
    acd = Function('ACD')
    test_ls_talib()
    test_talib()
    print(acd.lookback)
