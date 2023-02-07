from app.aws import get_secret
from app.utils import get_date_list
from app.constant import META_INSIGHTS_FIELDS

import requests
import json
import pandas as pd


class MetaAPI:
    # https://developers.facebook.com/docs/marketing-api/insights
    VERSION = "v16.0"
    URL = f"https://graph.facebook.com/{VERSION}{{}}"

    def __init__(self):
        self.service_name = 'META'
        self.access_token = None

    def set_secret(self,secret):
        self.access_token = secret['long_live_token']

    def report(self, account_id, start_date, end_date):
        base_params = {
            "access_token": self.access_token,
            "fields": ",".join(META_INSIGHTS_FIELDS),
            "level": "ad",
            "time_increment": 1
        }
        date_list = get_date_list(start_date, end_date)

        ret = []
        for date in date_list:
            params = {**base_params,
                      "time_range": json.dumps({"since": date, "until": date})}
            res = requests.get(
                self.URL.format(f"/act_{account_id}/insights"),
                params=params
            )

            try:
                data = res.json()["data"]
                for idx, d in enumerate(data):
                    if "date_start" in d:
                        data[idx] = {
                            **d,
                            "ymd": d["date_start"],
                        }
                ret += data

            except Exception as e:
                print(res.json())
                raise e

        return ret


if __name__ == '__main__':
    from app.aws import get_secret
    project_id = 'project_bat'
    credential_id = 'meta_credential'
    secret = get_secret(project_id, credential_id)
    meta = MetaAPI()
    meta.set_secret(secret)
    account_id = '513038489411939'
    start_date = '2023-01-01'
    end_date = '2023-01-03'

    data = meta.report(account_id, start_date, end_date)
    print(data)

