from app.aws import get_secret
from app.constant import GoogleCampaignType, GOOGLE_REPORT_FIELDS
from app.utils import to_snakecase

from google.ads.googleads.client import GoogleAdsClient
from google.protobuf import json_format

import pandas as pd


class GoogleAdsAPI:
    def __init__(self, project_id, credential_id):
        api_keys = {
                    "developer_token": "yrn8DNwjmxOf3aSVZhBdpA",
                    "client_id": "973022936082-6hcepnle00cel1sbvajo6vqlehp7641m.apps.googleusercontent.com",
                    "client_secret": "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"}

        api_keys = get_secret(secret_key, credential_id)

        self.credentials = {**api_keys,
                            **get_secret(project_id, credential_id),
                            "use_proto_plus": False}

        self.client = GoogleAdsClient.load_from_dict(self.credentials)

    def report(self, customer_id, campaign_type: GoogleCampaignType, start_date, end_date):

        if campaign_type == GoogleCampaignType.SEARCH:
            resource = "keyword_view"
            fields = GOOGLE_REPORT_FIELDS
            project_units = (
                "ad_group_criterion.criterion_id, ad_group_criterion.keyword.text"
            )
            where_clause = "ad_group_criterion.type = 'KEYWORD'"
        else:
            resource = "ad_group_ad"
            fields = GOOGLE_REPORT_FIELDS
            project_units = "ad_group_ad.ad.id, ad_group_ad.ad.name"
            where_clause = (
                f"campaign.advertising_channel_type = '{campaign_type.value}'"
            )

        if start_date is not None:
            where_clause += f" and segments.date >= '{start_date}'"
        if end_date is not None:
            where_clause += f" and segments.date <= '{end_date}'"
        if start_date is None and end_date is None:
            where_clause += f" and segments.date DURING LAST_30_DAYS"

        query = f"""
               SELECT
                   campaign.id, campaign.name,
                   ad_group.id, ad_group.name,
                   {project_units},
                   segments.date,
                   {",".join(f"metrics.{field}" for field in fields)}
               FROM {resource}
               WHERE {where_clause}
               PARAMETERS omit_unselected_resource_names = true"""

        svc = self.client.get_service("GoogleAdsService")
        search_request = self.client.get_type("SearchGoogleAdsStreamRequest")
        search_request.customer_id = customer_id
        search_request.query = query

        stream = svc.search_stream(search_request)
        ret = []
        for batch in stream:
            for raw_row in batch.results:
                row = json_format.MessageToDict(raw_row, use_integers_for_enums=False)
                temp = {}
                for google_entity, val_dict in row.items():
                    for field, val in val_dict.items():
                        if google_entity == "metrics":
                            temp[to_snakecase(field)] = val
                        elif google_entity == "adGroupCriterion":
                            if field == "criterionId":
                                temp["keyword_id"] = val
                        else:
                            if field == "ad":
                                temp["ad_id"] = val["id"]
                            else:
                                temp[
                                    f"{to_snakecase(google_entity)}_{to_snakecase(field)}"
                                ] = val

                ret.append(temp)

        return pd.DataFrame.from_dict(ret).to_csv(index=False)


if __name__ == '__main__':
    project_id = 'project_bat'
    credential_id = 'google_credential'
    secret_key = f'mini-hub/{project_id}'

    googleads = GoogleAdsAPI(project_id, credential_id)

    # connection_id로 서비스를 식별하고 datasource -> customer을 식별(서버에서 진행하고 서비스 모듈에 사용 x)
    # get_credential+도 빼야하는지 고민..


    customer_id = '6925749295'
    campaign_type = GoogleCampaignType.APP
    start_date = '2023-01-01'
    end_date = '2023-01-01'

    csv = googleads.report(customer_id, campaign_type, start_date, end_date)
    print(csv)


