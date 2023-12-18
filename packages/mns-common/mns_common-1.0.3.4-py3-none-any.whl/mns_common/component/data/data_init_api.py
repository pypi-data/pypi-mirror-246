import sys
import os

file_path = os.path.abspath(__file__)
end = file_path.index('mns') + 13
project_path = file_path[0:end]
sys.path.append(project_path)

import pandas as pd
import mns_common.component.common_service_fun_api as common_service_fun_api


def exclude_st_b(real_time_quotes_now, str_now_date):
    # exclude b symbol
    real_time_quotes_now = common_service_fun_api.exclude_b_symbol(real_time_quotes_now.copy())
    # exclude st symbol
    real_time_quotes_now = common_service_fun_api.exclude_st_symbol(real_time_quotes_now)
    # exclude amount==0 symbol
    real_time_quotes_now = common_service_fun_api.exclude_amount_zero_stock(real_time_quotes_now)
    # classification symbol
    real_time_quotes_now = common_service_fun_api.classify_symbol(real_time_quotes_now.copy())
    # calculate max_chg    chg_fall_back  diff_avg_chg
    real_time_quotes_now = common_service_fun_api.calculate_param(real_time_quotes_now.copy(), str_now_date)
    return real_time_quotes_now


# 初始化
def handle_init_real_time_quotes_data(real_time_quotes_now, str_now_date, number):
    #  exclude b symbol
    real_time_quotes_now = common_service_fun_api.exclude_b_symbol(real_time_quotes_now.copy())

    real_time_quotes_now = common_service_fun_api.exclude_amount_zero_stock(real_time_quotes_now)

    #  classification symbol
    real_time_quotes_now = common_service_fun_api.classify_symbol(real_time_quotes_now.copy())
    #  fix industry
    real_time_quotes_now = fix_industry_data(real_time_quotes_now.copy())
    #  calculate parameter disk info
    real_time_quotes_now = calculate_parameter_factor(real_time_quotes_now.copy())
    # ava price
    real_time_quotes_now = calculate_param(real_time_quotes_now.copy(), str_now_date)
    # set zb  high_chg
    real_time_quotes_now = common_service_fun_api.calculate_zb_high_chg(real_time_quotes_now)

    real_time_quotes_now['str_now_date'] = str_now_date
    real_time_quotes_now['number'] = number

    return real_time_quotes_now


# fix 错杀数据 有成交量的数据
def fix_industry_data(real_time_quotes_now):
    # fix industry
    real_time_quotes_now_r = amendment_industry(real_time_quotes_now.copy())

    symbol_list = list(real_time_quotes_now_r['symbol'])

    na_real_now = real_time_quotes_now.loc[
        ~(real_time_quotes_now['symbol'].isin(symbol_list))]

    na_real_now = na_real_now.loc[na_real_now['amount'] != 0]

    real_time_quotes_now_result = pd.concat([real_time_quotes_now_r, na_real_now], axis=0)
    return real_time_quotes_now_result


def amendment_industry_list_date(real_time_quotes_now):
    industry_group_df = common_service_fun_api.get_company_info_industry_list_date()
    industry_group_df = industry_group_df.set_index(['_id'], drop=True)
    real_time_quotes_now['em_industry'] = real_time_quotes_now['industry']
    real_time_quotes_now = real_time_quotes_now.loc[~(real_time_quotes_now['em_industry'] == '-')]
    real_time_quotes_now.drop(columns=['industry'], inplace=True)
    real_time_quotes_now = real_time_quotes_now.set_index(['symbol'], drop=False)
    real_time_quotes_now = pd.merge(real_time_quotes_now, industry_group_df, how='outer',
                                    left_index=True, right_index=True)

    real_time_quotes_now.loc[
        real_time_quotes_now["mv_circulation_ratio"].isnull(), ['mv_circulation_ratio']] \
        = 1
    real_time_quotes_now.loc[
        real_time_quotes_now["industry"].isnull(), ['industry']] \
        = real_time_quotes_now["em_industry"]
    real_time_quotes_now.dropna(subset=['symbol'], axis=0, inplace=True)
    return real_time_quotes_now


def amendment_industry(real_time_quotes_now_init):
    real_time_quotes_now = real_time_quotes_now_init.copy()
    if 'list_date' in real_time_quotes_now.columns:
        industry_group_df = common_service_fun_api.get_company_info_industry()
    else:
        industry_group_df = common_service_fun_api.get_company_info_industry_list_date()
    industry_group_df = industry_group_df.set_index(['_id'], drop=True)
    real_time_quotes_now['em_industry_temp'] = real_time_quotes_now['industry']
    real_time_quotes_now = real_time_quotes_now.loc[~(real_time_quotes_now['em_industry_temp'] == '-')]
    real_time_quotes_now.drop(columns=['industry'], inplace=True)
    real_time_quotes_now = real_time_quotes_now.set_index(['symbol'], drop=False)
    real_time_quotes_now = pd.merge(real_time_quotes_now, industry_group_df, how='outer',
                                    left_index=True, right_index=True)

    real_time_quotes_now.loc[
        real_time_quotes_now["mv_circulation_ratio"].isnull(), ['mv_circulation_ratio']] \
        = 1
    real_time_quotes_now.loc[
        real_time_quotes_now["industry"].isnull(), ['industry']] \
        = real_time_quotes_now["em_industry_temp"]
    real_time_quotes_now.dropna(subset=['symbol'], axis=0, inplace=True)
    real_time_quotes_now.drop(columns=['em_industry_temp'], inplace=True)

    return real_time_quotes_now


def amendment_industry_exist_na(real_time_quotes_now, symbol_list):
    industry_group_df = common_service_fun_api.get_company_info_industry()
    industry_group_df = industry_group_df.loc[industry_group_df['_id'].isin(symbol_list)]
    industry_group_df = industry_group_df.set_index(['_id'], drop=True)
    real_time_quotes_now.drop(columns=['industry'], inplace=True)
    real_time_quotes_now = real_time_quotes_now.set_index(['symbol'], drop=False)
    real_time_quotes_now = pd.merge(real_time_quotes_now, industry_group_df, how='outer',
                                    left_index=True, right_index=True)
    return real_time_quotes_now


def calculate_parameter_factor(real_time_quotes_now):
    # 单位亿
    real_time_quotes_now['amount_level'] = round(
        (real_time_quotes_now['amount'] / common_service_fun_api.hundred_million), 3)
    if bool(1 - ("disk_diff_amount_exchange" in real_time_quotes_now.columns)) or bool(
            1 - ("disk_diff_amount" in real_time_quotes_now.columns)):
        try:
            if 'average_price' in real_time_quotes_now.columns:
                # 外盘与内盘的金额差额 100 为1手
                real_time_quotes_now['disk_diff_amount'] = round(
                    (real_time_quotes_now['outer_disk'] - real_time_quotes_now['inner_disk']) * real_time_quotes_now[
                        "average_price"] * 100,
                    2)
            else:
                # 外盘与内盘的金额差额
                real_time_quotes_now['disk_diff_amount'] = round(
                    (real_time_quotes_now['outer_disk'] - real_time_quotes_now['inner_disk']) * real_time_quotes_now[
                        "now_price"] * 100,
                    2)
        except BaseException:
            real_time_quotes_now['disk_diff_amount'] = 0
    # 使用 平均价和内外盘差值之积除流通市值之比 和 内外盘差值/流通股 误差很小
    # # 内外盘为手       flow_share 单位为股 所以要乘100
    # real_time_quotes_now['disk_diff_share'] = round(
    #     (real_time_quotes_now['outer_disk'] - real_time_quotes_now['inner_disk']) * 100, 2)
    # # 计算千分比 百分比太小
    # real_time_quotes_now['disk_diff_share_exchange'] = (real_time_quotes_now['disk_diff_share']
    # / real_time_quotes_now[
    #     'flow_share']) * 1000

    real_time_quotes_now['disk_diff_amount_exchange'] = round(
        (real_time_quotes_now['disk_diff_amount'] / real_time_quotes_now['flow_mv']) * 1000, 2)

    real_time_quotes_now.loc[:, 'large_order_net_inflow_ratio'] = round(
        (real_time_quotes_now['large_order_net_inflow'] / real_time_quotes_now['amount']) * 100, 2)

    real_time_quotes_now.loc[:, 'reference_main_inflow'] = round(
        (real_time_quotes_now['flow_mv'] * (1 / 1000)), 2)

    real_time_quotes_now.loc[:, 'main_inflow_multiple'] = round(
        (real_time_quotes_now['today_main_net_inflow'] / real_time_quotes_now['reference_main_inflow']), 2)

    real_time_quotes_now.loc[:, 'super_main_inflow_multiple'] = round(
        (real_time_quotes_now['super_large_order_net_inflow'] / real_time_quotes_now['reference_main_inflow']), 2)
    real_time_quotes_now['large_inflow_multiple'] = round(
        (real_time_quotes_now['large_order_net_inflow'] / real_time_quotes_now['reference_main_inflow']), 2)

    real_time_quotes_now.loc[:, 'real_disk_diff_amount_exchange'] = round(
        (real_time_quotes_now['disk_diff_amount_exchange'] / real_time_quotes_now['mv_circulation_ratio']), 2)

    real_time_quotes_now.loc[:, 'real_main_inflow_multiple'] = round(
        (real_time_quotes_now['main_inflow_multiple'] / real_time_quotes_now['mv_circulation_ratio']), 2)

    real_time_quotes_now.loc[:, 'real_super_main_inflow_multiple'] = round(
        (real_time_quotes_now['super_main_inflow_multiple'] / real_time_quotes_now['mv_circulation_ratio']), 2)
    real_time_quotes_now.loc[:, 'real_exchange'] = round(
        (real_time_quotes_now['exchange'] / real_time_quotes_now['mv_circulation_ratio']), 2)

    real_time_quotes_now.loc[:, 'max_real_main_inflow_multiple'] = real_time_quotes_now[
        ['real_main_inflow_multiple', 'real_super_main_inflow_multiple']].max(axis=1)

    real_time_quotes_now.loc[:, 'sum_main_inflow_disk'] = real_time_quotes_now['max_real_main_inflow_multiple'] + \
                                                          real_time_quotes_now['real_disk_diff_amount_exchange']

    real_time_quotes_now.loc[:, "real_flow_mv"] = round(
        (real_time_quotes_now['flow_mv'] * real_time_quotes_now['mv_circulation_ratio']), 2)

    real_time_quotes_now.loc[:, 'reference_main_inflow'] = round(
        (real_time_quotes_now['flow_mv'] * (1 / 1000)), 2)

    real_time_quotes_now.loc[:, ['flow_mv_level']] \
        = ((real_time_quotes_now["flow_mv"] / common_service_fun_api.hundred_million) // 10) + 1

    real_time_quotes_now.loc[:, ['total_mv_level']] \
        = ((real_time_quotes_now["total_mv"] / common_service_fun_api.hundred_million) // 10) + 1

    return real_time_quotes_now


# 计算 当如最大涨幅  回落的幅度 超平均价幅度
def calculate_param(real_time_quotes_now):
    # 最大涨幅
    real_time_quotes_now['max_chg'] = round(
        (((real_time_quotes_now['high'] - real_time_quotes_now['yesterday_price']) / real_time_quotes_now[
            'yesterday_price']) * 100), 2)
    # 最大涨幅与当前涨幅的差值 越大表明是拉高出货
    real_time_quotes_now['chg_fall_back'] = round(real_time_quotes_now['max_chg'] - real_time_quotes_now['chg'], 2)
    # 当前价格与今天开盘价格的差值 为负表明为下跌趋势
    real_time_quotes_now['chg_from_open'] = round(
        (((real_time_quotes_now['now_price'] - real_time_quotes_now['open']) / real_time_quotes_now[
            'open']) * 100), 2)

    if 'average_price' in real_time_quotes_now.columns:
        # 高于平均线的差值 越大表明极速拉伸
        real_time_quotes_now['diff_avg_chg'] = round(
            (((real_time_quotes_now['now_price'] - real_time_quotes_now['average_price']) / real_time_quotes_now[
                'average_price']) * 100), 2)
    else:
        real_time_quotes_now['diff_avg_chg'] = 0
    return real_time_quotes_now


# 获取当天炸板股票代码 zb
def get_today_zb_symbol_list(real_time_quotes_now):
    real_time_quotes_now = real_time_quotes_now.loc[(real_time_quotes_now['wei_bi'] != 100)]
    real_time_quotes = real_time_quotes_now.loc[
        ((real_time_quotes_now['classification'].isin(['S', 'H'])) & (real_time_quotes_now['max_chg'] >= 9.90)) |
        (real_time_quotes_now['classification'].isin(['K', 'C', 'X'])) & (real_time_quotes_now['max_chg'] >= 19.90)]

    if real_time_quotes.shape[0] == 0:
        zb_symbol_list = ['000001']
    else:
        zb_symbol_list = list(real_time_quotes['symbol'])
    return zb_symbol_list


def calculate_zb_high_chg(real_time_quotes_now):
    zb_symbol_list = get_today_zb_symbol_list(real_time_quotes_now.copy())
    real_time_quotes_now['is_zb'] = False
    real_time_quotes_now.loc[real_time_quotes_now['symbol'].isin(zb_symbol_list), 'is_zb'] = True
    # 涨幅过高股
    real_time_quotes_now.loc[:, 'high_standard'] = False
    real_time_quotes_now.loc[((real_time_quotes_now['classification'].isin(['S', 'H']))
                              & (real_time_quotes_now['chg'] > max_chg_sz) |
                              (real_time_quotes_now['classification'].isin(['X', 'K', 'C']))
                              & (real_time_quotes_now['chg'] > max_chg_kcx)
                              ), 'high_standard'] = True
    return real_time_quotes_now
