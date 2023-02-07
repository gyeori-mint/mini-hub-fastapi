from sqlalchemy import Column, DateTime, DATE, INTEGER, VARCHAR, FLOAT, ForeignKey, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from database import Base


class Project(Base):
    __tablename__ = 'project'
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())
    name = Column(VARCHAR)


class Service(Base):
    __tablename__ = 'service'
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())


class ServiceConnection(Base):
    __tablename__ = 'service_connection'
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())


class DataConnection(Base):
    __tablename__ = 'data_connection'
    id = Column(UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid())


# Media
class GoogleAdsReport(Base):
    __tablename__ = 'google_ads_report'
    date = Column(DATE, primary_key=True)
    datasource_id = Column(VARCHAR, primary_key=True)
    campaign_id = Column(VARCHAR, nullable=False)
    campaign_name = Column(VARCHAR, nullable=False)
    ad_group_id = Column(VARCHAR, nullable=False)
    ad_group_name = Column(VARCHAR, nullable=False)
    ad_id = Column(VARCHAR, primary_key=True)
    ad_name = Column(VARCHAR)
    utm_source = Column(VARCHAR)
    utm_medium = Column(VARCHAR)
    utm_campaign = Column(VARCHAR)
    utm_content = Column(VARCHAR)
    utm_term = Column(VARCHAR)
    impressions = Column(INTEGER)
    clicks = Column(INTEGER)
    cost_micro = Column(FLOAT)
    all_conversions = Column(JSON)


class MetaReport(Base):
    __tablename__ = 'meta_report'
    date = Column(DATE, primary_key=True)
    datasource_id = Column(VARCHAR, primary_key=True)
    campaign_id = Column(VARCHAR, nullable=False)
    campaign_name = Column(VARCHAR, nullable=False)
    adset_id = Column(VARCHAR, nullable=False)
    adset_name = Column(VARCHAR, nullable=False)
    ad_id = Column(VARCHAR, primary_key=True)
    ad_name = Column(VARCHAR)
    utm_source = Column(VARCHAR)
    utm_medium = Column(VARCHAR)
    utm_campaign = Column(VARCHAR)
    utm_content = Column(VARCHAR)
    utm_term = Column(VARCHAR)
    impressions = Column(INTEGER)
    clicks = Column(INTEGER)
    spend = Column(FLOAT)
    actions = Column(JSON)


class NaverSaReport(Base):
    date = Column(DATE, primary_key=True)
    datasource_id = Column(VARCHAR, primary_key=True)
    campaign_id = Column(VARCHAR)
    campaign_name = Column(VARCHAR)
    adgroup_id = Column(VARCHAR)
    adgroup_name = Column(VARCHAR)
    keyword_id = Column(VARCHAR)
    keyword_name = Column(VARCHAR, primary_key=True)
    utm_source = Column(VARCHAR)
    utm_medium = Column(VARCHAR)
    utm_campaign = Column(VARCHAR)
    utm_content = Column(VARCHAR)
    utm_term = Column(VARCHAR)
    imp_cnt = Column(INTEGER)
    clk_cnt = Column(INTEGER)
    avg_rnk = Column(FLOAT)
    sales_amt = Column(INTEGER)


class KakaoKeywordadFile(Base):
    __tablename__ = 'kakao_keywordad_file'
    date = Column(DATE, primary_key=True)
    datasource_id = Column(VARCHAR, primary_key=True)
    biz_channel_name = Column(VARCHAR)
    campaign_name = Column(VARCHAR)
    ad_group_name = Column(VARCHAR)
    keyword_name = Column(VARCHAR, primary_key=True)
    device = Column(VARCHAR)
    imp = Column(INTEGER)
    click = Column(INTEGER)
    spending = Column(FLOAT)
    addition = Column(JSON)
    pixel_sdk_conversion = Column(JSON)


class KakaoMomentFile(Base):
    __tablename__ = 'kakao_moment_file'
    date = Column(DATE, primary_key=True)
    datasource_id = Column(VARCHAR, primary_key=True)
    biz_channel_name = Column(VARCHAR)
    campaign_name = Column(VARCHAR)
    ad_group_name = Column(VARCHAR)
    creative_name = Column(VARCHAR, primary_key=True)
    imp = Column(INTEGER)
    click = Column(INTEGER)
    cost = Column(FLOAT)
    addition = Column(JSON)
    pixel_sdk_conversion = Column(JSON)


class GoogleAnalytics4File(Base):
    __tablename__ = 'google_analytics4_file'
    date = Column(DATE, primary_key=True)
    datasource_id = Column(VARCHAR, primary_key=True)
    utm_source = Column(VARCHAR, primary_key=True)
    utm_medium = Column(VARCHAR, primary_key=True)
    utm_campaign = Column(VARCHAR, primary_key=True)
    event_name = Column(VARCHAR, primary_key=True)
    event_count = Column(INTEGER)
    event_value = Column(FLOAT)


class GoogleDatastudioFile(Base):
    __tablename__ = 'google_datastudio_file'
    date = Column(DATE, primary_key=True)
    datasource_id = Column(VARCHAR, primary_key=True)
    utm_source = Column(VARCHAR, primary_key=True)
    utm_medium = Column(VARCHAR, primary_key=True)
    utm_campaign = Column(VARCHAR, primary_key=True)
    event_name = Column(VARCHAR, primary_key=True)
    event_count = Column(INTEGER)
    event_value = Column(FLOAT)
