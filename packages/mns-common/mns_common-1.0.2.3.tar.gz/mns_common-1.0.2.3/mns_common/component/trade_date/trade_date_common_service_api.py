import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 14
project_path = file_path[0:end]
sys.path.append(project_path)

from functools import lru_cache
from mns_common.db.MongodbUtil import MongodbUtil

mongodb_util = MongodbUtil('27017')


# 获取上一个交易日期
@lru_cache(maxsize=None)
def get_last_trade_day(str_day):
    query = {'trade_date': {'$lt': str_day}}
    last_stock_zt_pool_group = mongodb_util.descend_query(query, 'trade_date_list', 'trade_date', 1)
    last_stock_zt_pool_group = last_stock_zt_pool_group.sort_values(by=['trade_date'],
                                                                    ascending=True)
    return list((last_stock_zt_pool_group.iloc[0:1])['trade_date'])[0]


# 前number个交易日 number=1 为当前时间
def get_before_trade_date(begin_day, number):
    query = {"_id": {'$lte': begin_day}}
    trade_date_list = mongodb_util.descend_query(query, 'trade_date_list', "_id", number)
    trade_date_list = trade_date_list.sort_values(by=['_id'],
                                                  ascending=True)
    before_days = list(trade_date_list[0:1]["_id"])[0]
    return before_days


# 获取未来第number个交易日
@lru_cache(maxsize=None)
def get_further_trade_date(begin_day, number):
    query = {"_id": {'$gte': begin_day}}
    trade_date_list = mongodb_util.ascend_query(query, 'trade_date_list', "_id", number)
    trade_date_list = trade_date_list.sort_values(by=['_id'],
                                                  ascending=False)
    before_days = list(trade_date_list[0:1]["_id"])[0]
    return before_days


def is_trade_day(str_day):
    query = {"trade_date": str_day}
    return mongodb_util.exist_data_query("trade_date_list", query)


if __name__ == '__main__':
    get_further_trade_date('2023-12-15', 5)
