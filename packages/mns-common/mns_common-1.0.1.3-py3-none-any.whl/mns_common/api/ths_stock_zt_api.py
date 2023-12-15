import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 7
project_path = file_path[0:end]
sys.path.append(project_path)
import re

# question
# 必填，查询问句
#
# sort_key
# 非必填，指定用于排序的字段，值为返回结果的列名
#
# sort_order
# 非必填，排序规则，至为asc（升序）或desc（降序）
#
# page
# 非必填，查询的页号，默认为1
#
# perpage
# 非必填，每页数据条数，默认值100，由于问财做了数据限制，最大值为100，指定大于100的数值无效。
#
# loop
# 非必填，是否循环分页，返回多页合并数据。默认值为False，可以设置为True或具体数值。
#
# 当设置为True时，程序会一直循环到最后一页，返回全部数据。
#
# 当设置具体数值n时，循环请求n页，返回n页合并数据。


import pywencai


def wei_cai_api(question):
    response = pywencai.get(question=question, loop=True)
    return response


def get_zt_reason():
    zt_df = wei_cai_api('涨停')
    zt_df.columns = ["symbol",
                     "name",
                     "now_price",
                     "chg",
                     "zt_tag",

                     "first_closure_time",
                     "last_closure_time",
                     "zt_detail",
                     "connected_boards_numbers",
                     "zt_reason",

                     "closure_volume",
                     "closure_funds",
                     "closure_funds_per_amount",
                     "closure_funds_per_flow_mv",
                     "frying_plates_numbers",

                     "flow_mv",
                     "statistics_detail",
                     "zt_type",
                     "market_code",
                     "code",
                     ]
    zt_df['statistics'] = zt_df['statistics_detail'].apply(convert_statistics)
    del zt_df['code']
    return zt_df


# 定义一个函数，用于将统计数据转换成相应的格式
def convert_statistics(stat):
    match = re.match(r'(\d+)天(\d+)板', stat)
    if match:
        n, m = map(int, match.groups())
        return f'{n}/{m}'
    elif stat == '首板涨停':
        return '1/1'
    else:
        return stat


if __name__ == '__main__':
    res = get_zt_reason()
    print(res)
