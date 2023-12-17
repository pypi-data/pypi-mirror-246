import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 14
project_path = file_path[0:end]
sys.path.append(project_path)
import akshare as ak
from loguru import logger
from mns_common.db.MongodbUtil import MongodbUtil
import mns_common.utils.data_frame_util as data_frame_util

mongodb_util = MongodbUtil('27017')


def sync_trade_date():
    trade_date_list = ak.tool_trade_date_hist_sina()
    trade_date_list.trade_date = trade_date_list.trade_date.astype(str)
    trade_date_list['_id'] = trade_date_list['trade_date']
    trade_date_list['tag'] = False
    exist_trade_date_list = mongodb_util.find_all_data('trade_date_list')
    if data_frame_util.is_empty(exist_trade_date_list):
        mongodb_util.insert_mongo(trade_date_list, 'trade_date_list')
    else:
        new_trade_date_list = trade_date_list.loc[~(trade_date_list['_id'].isin(exist_trade_date_list['_id']))]
        if data_frame_util.is_not_empty(new_trade_date_list):
            mongodb_util.save_mongo(new_trade_date_list, 'trade_date_list')
        logger.info('同步交易日期任务完成')


if __name__ == '__main__':
    sync_trade_date()
