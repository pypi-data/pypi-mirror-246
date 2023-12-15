import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 14
project_path = file_path[0:end]
sys.path.append(project_path)
import akshare as ak
from loguru import logger


def stock_em_zt_pool_df(date):
    try:
        df = ak.stock_zt_pool_em(date)
        if df is None or df.shape[0] == 0:
            return
        df.rename(columns={"序号": "index",
                           "代码": "symbol",
                           "名称": "name",
                           "最新价": "now_price",
                           "涨跌幅": "chg",
                           "成交额": "amount",
                           "流通市值": "flow_mv",
                           "总市值": "total_mv",
                           "换手率": "exchange",
                           "封板资金": "closure_funds",
                           "首次封板时间": "first_closure_time",
                           "最后封板时间": "last_closure_time",
                           "炸板次数": "frying_plates_numbers",
                           "涨停统计": "statistics",
                           "连板数": "connected_boards_numbers",
                           "所属行业": "industry"
                           }, inplace=True)
        df.loc[df['amount'] == '-', 'amount'] = 0
        df.loc[df['exchange'] == '-', 'exchange'] = 0
        df.loc[df['closure_funds'] == '-', 'closure_funds'] = 0
        return df
    except BaseException as e:
        logger.error("同步股票涨停数据出现异常:{},{}", date, e)
        return None


if __name__ == '__main__':
    df = stock_em_zt_pool_df('20231215')
    print(df)
