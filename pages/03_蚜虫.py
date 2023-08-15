import streamlit as st
import pandas as pd
from tools import get_last_result, get_current_status, get_engine


# 获取数据的函数
@st.cache_data
def get_data(gen=1):
    # 读取调查表和防治表
    # 从MySQL数据库中读取调查表和防治表
    # 建立数据库连接
    engine = get_engine()
    if gen == 1:
        pass
    elif gen == 2:
        # 执行SQL查询并获取数据
        query = "SELECT * FROM `2023_蚜虫_2代_调查表`;"
        df_survey = pd.read_sql(query, engine)
        df_survey['调查日期'] = pd.to_datetime(df_survey['调查日期'], format='%Y-%m-%d')

        query = "SELECT * FROM `2023_蚜虫_2代_防治表`;"
        df_treatment = pd.read_sql(query, engine)
        df_treatment['防治日期'] = pd.to_datetime(df_treatment['防治日期'], format='%Y-%m-%d')
        # 关闭数据库连接
        engine.dispose()

        # 获取每个点位第一次受害的数据
        df_survey_filtered = df_survey[df_survey['点位编号'].notnull()]
        df_survey_filtered_grouped = df_survey_filtered.groupby('点位编号')
        idx = df_survey_filtered_grouped['调查日期'].idxmin()
        df_first_damage = df_survey_filtered.loc[idx]
    elif gen == 3:
        pass

    return df_survey, df_treatment, df_first_damage


df_survey, df_treatment, df_first_damage = get_data(gen=2)

st.sidebar.title('蚜虫防治系统')
radio = st.sidebar.radio('请选择功能', ['巡查数据', '防治台账'])

# 巡查数据
if radio == '巡查数据':
    x = df_survey.copy()
    # 把日期转换为字符串
    x['调查日期'] = x['调查日期'].dt.strftime('%Y-%m-%d')
    st.dataframe(x, use_container_width=True)

# 防治台账
elif radio == '防治台账':
    # 获取最新调查结果和最新防治结果
    df_last_result = get_last_result(df_survey, df_treatment, df_first_damage)
    # 计算当前状态
    df_last_result['当前状态'] = df_last_result.apply(get_current_status, axis=1)
    # 仅保留需要的列
    df_last_result = df_last_result[['调查日期', '乡镇/街道', '点位编号', '点位名', '详细描述', '最新调查日期', '最新防治日期',
                                     '总调查次数', '总防治次数', '当前状态']]
    # 为了展示好看，将日期转换为字符串
    df_last_result['调查日期'] = df_last_result['调查日期'].dt.strftime('%Y-%m-%d')
    df_last_result['最新调查日期'] = df_last_result['最新调查日期'].dt.strftime('%Y-%m-%d')
    df_last_result['最新防治日期'] = df_last_result['最新防治日期'].dt.strftime('%Y-%m-%d')
    df_last_result['总防治次数'].fillna(0, inplace=True)
    # 按照日期和乡镇/街道排序
    df_last_result.sort_values(by=['调查日期', '乡镇/街道'], inplace=True)

    st.dataframe(df_last_result, use_container_width=True)