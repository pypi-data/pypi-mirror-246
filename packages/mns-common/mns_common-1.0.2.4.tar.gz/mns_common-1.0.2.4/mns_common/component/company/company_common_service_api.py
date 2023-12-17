import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 14
project_path = file_path[0:end]
sys.path.append(project_path)
from functools import lru_cache
from mns_common.db.MongodbUtil import MongodbUtil
import pandas as pd
mongodb_util = MongodbUtil('27017')


@lru_cache(maxsize=None)
def get_company_info_industry():
    return mongodb_util.find_query_data_choose_field('company_info', {},
                                                     {"_id": 1, "industry": 1, "company_type": 1,
                                                      "ths_concept_name": 1, "ths_concept_code": 1,
                                                      "ths_concept_sync_day": 1, 'sub_stock': 1,
                                                      "first_sw_industry": 1, "second_sw_industry": 1,
                                                      "third_sw_industry": 1, "mv_circulation_ratio": 1,
                                                      "diff_days": 1,
                                                      'em_industry': 1,
                                                      'ths_concept_list_info': 1,
                                                      "kpl_plate_name": 1,
                                                      "kpl_plate_list_info": 1})


@lru_cache(maxsize=None)
def get_company_info_industry_list_date():
    return mongodb_util.find_query_data_choose_field('company_info', {},
                                                     {"_id": 1, "industry": 1, "company_type": 1,
                                                      "ths_concept_name": 1, "ths_concept_code": 1,
                                                      "ths_concept_sync_day": 1, 'sub_stock': 1,
                                                      "first_sw_industry": 1, "second_sw_industry": 1,
                                                      "third_sw_industry": 1, "mv_circulation_ratio": 1,
                                                      "list_date": 1, 'ths_concept_list_info': 1,
                                                      "diff_days": 1, 'em_industry': 1,
                                                      "kpl_plate_name": 1, "kpl_plate_list_info": 1
                                                      })


@lru_cache(maxsize=None)
def get_company_info_industry_mv():
    return mongodb_util.find_query_data_choose_field('company_info', {},
                                                     {"_id": 1, "industry": 1,
                                                      "ths_concept_name": 1, "ths_concept_code": 1,
                                                      "ths_concept_sync_day": 1, 'sub_stock': 1,
                                                      "first_sw_industry": 1, "second_sw_industry": 1,
                                                      "third_sw_industry": 1, "mv_circulation_ratio": 1,
                                                      "diff_days": 1, 'em_industry': 1, 'ths_concept_list_info': 1,
                                                      "flow_mv_sp": 1, "total_mv_sp": 1,
                                                      "kpl_plate_name": 1, "kpl_plate_list_info": 1})


def fix_symbol_industry(realtime_quotes_now_list):
    company_info_industry = get_company_info_industry()
    realtime_quotes_now_list.drop(columns=['industry'], inplace=True)
    realtime_quotes_now_list = realtime_quotes_now_list.set_index(['symbol'], drop=False)

    company_info_industry = company_info_industry.set_index(['_id'], drop=True)

    realtime_quotes_now_list = pd.merge(realtime_quotes_now_list, company_info_industry, how='outer',
                                        left_index=True, right_index=True)

    realtime_quotes_now_list = realtime_quotes_now_list.dropna(inplace=False)
    return realtime_quotes_now_list


def company_info_industry_cache_clear():
    get_company_info_industry.cache_clear()
    get_company_info_industry_list_date.cache_clear()
