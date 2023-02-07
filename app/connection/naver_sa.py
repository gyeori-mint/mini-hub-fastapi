from app.utils import get_date_list
from datetime import datetime as dt
from datetime import timedelta
import pandas as pd
import requests
import time
import base64

import hmac
import hashlib

COL_MAP = {'id': 'keyword_id',
           'impCnt': 'impression',
           'clkCnt': 'click',
           'avgRnk': 'avg_rank',
           'salesAmt': 'spend'}


class NaverSa:
    base_url = 'https://api.searchad.naver.com'

    def __init__(self, secret):
        self.x_api_key = secret['x_api_key']
        self.secret_key = secret['secret_key']
        self.customer_id = secret['customer_id']

        self.edit_tm_min = dt.today() - timedelta(days=60)
        self.edit_tm_format = '%Y-%m-%dT%H:%M:%S.%fZ'
        self.stat_fields = ["impCnt", "clkCnt", "avgRnk", "salesAmt"]

    def set_header(self, method, service):
        timestamp = str(round(time.time() * 1000))
        message = f"{timestamp}.{method}.{service}"
        hash = hmac.new(bytes(self.secret_key, "utf-8"), bytes(message, "utf-8"), hashlib.sha256)
        hash.hexdigest()
        signature = base64.b64encode(hash.digest())
        header = {'Content-Type': 'application/json; charset=UTF-8',
                  'X-Timestamp': timestamp,
                  'X-Signature': signature,
                  'X-API-KEY': self.x_api_key,
                  'X-Customer': self.customer_id}
        return header

    def get_campaigns(self):
        method = 'GET'
        service = '/ncc/campaigns'
        url = self.base_url + service
        header = self.set_header(method, service)
        params = {'customerId': self.customer_id}

        r = requests.get(url, headers=header, params=params)
        return r.json()

    def get_adgroups(self, campaign_id):
        method = 'GET'
        service = '/ncc/adgroups'
        url = self.base_url + service
        header = self.set_header(method, service)
        params = {'nccCampaignId': campaign_id}

        # Be able to Modify Hierarchy
        r = requests.get(url, headers=header, params=params)
        return r.json()

    def get_ads(self, adgroup_id):
        method = 'GET'
        service = '/ncc/ads'
        url = self.base_url + service
        header = self.set_header(method, service)

        params = {'nccAdgroupId': adgroup_id}

        r = requests.get(url, headers=header, params=params)
        return r.json()

    def get_keywords(self, adgroup_id):
        method = 'GET'
        service = '/ncc/keywords'
        url = self.base_url + service
        header = self.set_header(method, service)
        params = {'nccAdgroupId': adgroup_id}
        r = requests.get(url, headers=header, params=params)

        return r.json()

    def get_stats(self, object_ids, start_date, end_date=None):
        # Object ID can be Campaign ID, Adgroup ID, ..
        if not end_date:
            end_date = start_date

        method = 'GET'
        service = '/stats'
        url = self.base_url + service
        header = self.set_header(method, service)

        params = {'ids': object_ids,
                  'fields': '["impCnt", "clkCnt", "salesAmt"]',
                  'timeRange': f'{{"since": "{start_date}", "until": "{end_date}"}}'}

        r = requests.get(url, headers=header, params=params)
        return r.json()

    def get_daily_stats(self, object_ids, start_date, end_date):
        date_list = get_date_list(start_date, end_date)
        result = []
        for _date in date_list:
            response = self.get_stats(object_ids, _date)
            for _data in response['data']:
                _data['ymd'] = _date
                result.append(_data)
        return result

    def _fetch(self):
        def validate_objects(data_list):
            valid_data_list = []
            for _d in data_list:
                if _d['status'] == 'ELIGIBLE':
                    valid_data_list.append(_d)

                elif _d['status'] == 'PAUSED':
                    if 'editTm' in _d.keys():
                        if dt.strptime(_d['editTm'], self.edit_tm_format) > self.edit_tm_min:
                            valid_data_list.append(_d)

            return valid_data_list

        response = self.get_campaigns()
        valid_campaigns = validate_objects(response)

        fetch_data = []
        for _c in valid_campaigns:
            response = self.get_adgroups(_c['nccCampaignId'])
            valid_adgroups = validate_objects(response)

            for _g in valid_adgroups:
                response = self.get_keywords(_g['nccAdgroupId'])
                valid_keywords = validate_objects(response)

                for _k in valid_keywords:
                    # Aggregate Campaign / Group / Keyword

                    new_c = dict(campaign_id=_c['nccCampaignId'],
                                 campaign_name=_c['name'])
                    new_g = dict(adgroup_id=_g['nccAdgroupId'],
                                 adgroup_name=_g['name'])
                    new_k = dict(keyword_id=_k['nccKeywordId'],
                                 keyword_name=_k['keyword'],
                                 landing_url=_k['links']['pc']['final'])
                    fetch_dict = {**new_c, **new_g, **new_k}

                    fetch_data.append(fetch_dict)
        return fetch_data

    def report(self, start_date, end_date):
        # Get Object Info
        fetch_data = self._fetch()
        df_fetch = pd.json_normalize(fetch_data)
        keyword_ids = df_fetch['keyword_id']

        # Get Report(by keyword)
        response = self.get_daily_stats(keyword_ids, start_date, end_date)
        df_stat = pd.json_normalize(response)
        df_stat.rename(columns=COL_MAP, inplace=True)
        df_report = df_fetch.merge(df_stat, how='right', on='keyword_id')

        return df_report


if __name__ == '__main__':

    project_id = 'project_bat'
    credential_id = 'naver_sa_credential'
    secret_key = f"mini-hub/{project_id}"

    naversa = NaverSa(secret_key, credential_id)
    start_date = '2022-12-01'
    end_date = '2022-12-31'
    df = naversa.report(start_date, end_date)
    print(df)
