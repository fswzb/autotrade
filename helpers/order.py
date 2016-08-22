# coding: utf-8
import datetime
import ssl
import random
from PIL import ImageFilter, Image
import pytesseract
import numpy

import simplejson as json
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager

from io import open


class EntrustProp(object):
    Limit = 'limit'
    Market = 'market'


class Ssl3HttpAdapter(HTTPAdapter):
    def init_poolmanager(self, connections, maxsize, block=False):
        self.poolmanager = PoolManager(
            num_pools=connections,
            maxsize=maxsize,
            block=block,
            ssl_version=ssl.PROTOCOL_TLSv1)


def file2dict(path):
    with open(path, encoding='utf-8') as f:
        return json.load(f)


def get_stock_type(stock_code):
    """判断股票ID对应的证券市场
    匹配规则
    ['50', '51', '60', '90', '110'] 为 sh
    ['00', '13', '18', '15', '16', '18', '20', '30', '39', '115'] 为 sz
    ['5', '6', '9'] 开头的为 sh， 其余为 sz
    :param stock_code:股票ID, 若以 'sz', 'sh' 开头直接返回对应类型，否则使用内置规则判断
    :return 'sh' or 'sz'"""
    assert type(stock_code) is str, 'stock code need str type'
    if stock_code.startswith(('sh', 'sz')):
        return stock_code[:2]
    if stock_code.startswith(
        ('50', '51', '60', '73', '90', '110', '113', '132', '204', '78')):
        return 'sh'
    if stock_code.startswith(
        ('00', '13', '18', '15', '16', '18', '20', '30', '39', '115', '1318')):
        return 'sz'
    if stock_code.startswith(('5', '6', '9')):
        return 'sh'
    return 'sz'


def recognize_verify_code(image_path, broker='ht'):
    """识别验证码，返回识别后的字符串，使用 tesseract 实现
    :param image_path: 图片路径
    :param broker: 券商 ['ht', 'yjb', 'gf', 'yh']
    :return recognized: verify code string"""
    if broker in ['ht', 'yjb']:
        return detect_image_result(image_path)
    elif broker == 'gf':
        return detect_gf_result(image_path)
    elif broker == 'yh':
        return detect_yh_result(image_path)


def detect_gf_result(image_path):
    img = Image.open(image_path)
    if hasattr(img, "width"):
        width, height = img.width, img.height
    else:
        width, height = img.size
    for x in range(width):
        for y in range(height):
            if img.getpixel((x, y)) < (100, 100, 100):
                img.putpixel((x, y), (256, 256, 256))
    gray = img.convert('L')
    two = gray.point(lambda x: 0 if 68 < x < 90 else 256)
    min_res = two.filter(ImageFilter.MinFilter)
    med_res = min_res.filter(ImageFilter.MedianFilter)
    for _ in range(2):
        med_res = med_res.filter(ImageFilter.MedianFilter)
    res = pytesseract.image_to_string(med_res)
    return res.replace(' ', '')


def detect_image_result(image_path):
    img = Image.open(image_path)
    for x in range(img.width):
        for y in range(img.height):
            (r, g, b) = img.getpixel((x, y))
            if r > 100 and g > 100 and b > 100:
                img.putpixel((x, y), (256, 256, 256))
    res = pytesseract.image_to_string(img)
    return res


def detect_yh_result(image_path):
    img = Image.open(image_path)

    brightness = list()
    for x in range(img.width):
        for y in range(img.height):
            (r, g, b) = img.getpixel((x, y))
            brightness.append(r + g + b)
    avgBrightness = int(numpy.mean(brightness))

    for x in range(img.width):
        for y in range(img.height):
            (r, g, b) = img.getpixel((x, y))
            if ((r + g + b) > avgBrightness / 1.5) or (y < 3) or (y > 17) or (
                    x < 5) or (x > (img.width - 5)):
                img.putpixel((x, y), (256, 256, 256))

    res = pytesseract.image_to_string(img)
    return res


def get_mac():
    oui = [0x52, 0x54, 0x00]

    mac = oui + [random.randint(0x00, 0xff), random.randint(0x00, 0xff),
                 random.randint(0x00, 0xff)]
    return ':'.join(map(lambda x: "%02x" % x, mac))


def grep_comma(num_str):
    return num_str.replace(',', '')


def str2num(num_str, convert_type='float'):
    num = float(grep_comma(num_str))
    return num if convert_type == 'float' else int(num)


def get_30_date():
    """
    获得用于查询的默认日期, 今天的日期, 以及30天前的日期
    用于查询的日期格式通常为 20160211
    :return:
    """
    now = datetime.datetime.now()
    end_date = now.date()
    start_date = end_date - datetime.timedelta(days=30)
    return start_date.strftime("%Y%m%d"), end_date.strftime("%Y%m%d")
