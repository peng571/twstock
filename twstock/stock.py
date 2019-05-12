# -*- coding: utf-8 -*-
import time
import datetime
import urllib.parse
from collections import namedtuple
try:
    from json.decoder import JSONDecodeError
except ImportError:
    JSONDecodeError = ValueError

import requests

import importlib.util
spec = importlib.util.spec_from_file_location("twstock", "../twstock/twstock")

TWSE_BASE_URL = 'http://www.twse.com.tw/'
TPEX_BASE_URL = 'http://www.tpex.org.tw/'
DATATUPLE = namedtuple('Data', ['date', 'capacity', 'turnover', 'open',
                                'high', 'low', 'close', 'change', 'transaction'])

class BaseFetcher(object):
    def fetch(self, year, month, sid, retry):
        pass

    def _convert_date(self, date):
        """Convert '106/05/01' to '2017/05/01'"""
        return '/'.join([str(int(date.split('/')[0]) + 1911)] + date.split('/')[1:])

    def _make_datatuple(self, data):
        pass

    def purify(self, original_data):
        pass


class TWSEFetcher(BaseFetcher):
    REPORT_URL = urllib.parse.urljoin(TWSE_BASE_URL, 'exchangeReport/STOCK_DAY')

    def __init__(self):
        pass

    def fetch(self, year: int, month: int, sid: str, retry: int=5):
        params = {'date': '%d%02d01' % (year, month), 'stockNo': sid}
        for retry_i in range(retry):
            r = requests.get(self.REPORT_URL, params=params)
            time.sleep(2)
            try:
                data = r.json()
            except JSONDecodeError:
                continue
            else:
                break
        else:
            # Fail in all retries
            data = {'stat': '', 'data': []}
        return data

    def _make_datatuple(self, data):
        data[0] = datetime.datetime.strptime(self._convert_date(data[0]), '%Y/%m/%d')
        data[1] = int(data[1].replace(',', ''))
        data[2] = int(data[2].replace(',', ''))
        data[3] = None if data[3] == '--' else float(data[3].replace(',', ''))
        data[4] = None if data[4] == '--' else float(data[4].replace(',', ''))
        data[5] = None if data[5] == '--' else float(data[5].replace(',', ''))
        data[6] = None if data[6] == '--' else float(data[6].replace(',', ''))
        # +/-/X表示��
