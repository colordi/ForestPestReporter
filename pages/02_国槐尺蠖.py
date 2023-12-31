import sqlite3

import streamlit as st
import pandas as pd
from tools import get_last_result, get_current_status


# 获取数据的函数
def get_data(gen=1):
    # 建立数据库连接
    conn = sqlite3.connect('forestry_pests_2023.sqlite3')
    if gen == 1:
        pass
    elif gen == 2:
        # 执行SQL查询并获取数据
        query = '''
        SELECT x.*,
               x."1号" + x."2号" + x."3号" + x."4号" + x."5号" AS 总数,
               (x."1号" + x."2号" + x."3号" + x."4号" + x."5号") / 5 AS 平均
        FROM `2023_国槐尺蠖_2代_调查表` AS x
        ORDER BY x.调查日期, 平均 DESC;
        '''
        df_survey = pd.read_sql(query, conn)
        df_survey['调查日期'] = pd.to_datetime(df_survey['调查日期'], format='%Y-%m-%d')

        query = "SELECT * FROM `2023_国槐尺蠖_2代_防治表`;"
        df_treatment = pd.read_sql(query, conn)
        df_treatment['防治日期'] = pd.to_datetime(df_treatment['防治日期'], format='%Y-%m-%d')
        # 关闭数据库连接
        conn.close()

        # 获取每个点位第一次受害的数据
        df_survey_filtered = df_survey[df_survey['点位名'].notnull()]
        df_survey_filtered_grouped = df_survey_filtered.groupby('点位编号')
        idx = df_survey_filtered_grouped['调查日期'].idxmin()
        df_first_damage = df_survey_filtered.loc[idx]
    elif gen == 3:
        pass

    return df_survey, df_treatment, df_first_damage


df_survey, df_treatment, df_first_damage = get_data(gen=2)

st.sidebar.title('国槐尺蠖防治系统')
radio = st.sidebar.radio('请选择功能', ['巡查记录', '防治台账'])

# 巡查记录
if radio == '巡查记录':
    x = df_survey.copy()
    # 把日期转换为字符串
    x['调查日期'] = x['调查日期'].dt.strftime('%Y-%m-%d')
    # 索引从1开始
    x.index = range(1, len(x) + 1)


    def show_progress():
        # 读取数据库中的国槐点位信息表
        conn = sqlite3.connect('forestry_pests_2023.sqlite3')
        query = "SELECT * FROM `国槐点位信息表`;"
        df = pd.read_sql(query, conn)
        conn.close()
        # 计算调查日期列中非空值的个数
        current = df['2代调查日期'].notnull().sum()
        allcounts = len(df['2代调查日期'])
        value = current / allcounts
        # 显示进度条
        st.progress(value, f"当前调查:red[{current}]总点位:blue[{allcounts }]进度:orange[{round(value * 100, 2)}%]")
        return None
    show_progress()
    st.dataframe(x, use_container_width=True)

# 防治台账
elif radio == '防治台账':
    # 获取最新调查结果和最新防治结果
    df_last_result = get_last_result(df_survey, df_treatment, df_first_damage)
    # 计算当前状态
    df_last_result['当前状态'] = df_last_result.apply(get_current_status, axis=1)
    # 仅保留需要的列
    df_last_result = df_last_result[
        ['调查日期', '乡镇/街道', '点位编号', '点位名', '详细描述', '最新调查日期', '最新防治日期',
         '总调查次数', '总防治次数', '当前状态']]
    # 为了展示好看，将日期转换为字符串
    df_last_result['调查日期'] = df_last_result['调查日期'].dt.strftime('%Y-%m-%d')
    df_last_result['最新调查日期'] = df_last_result['最新调查日期'].dt.strftime('%Y-%m-%d')
    df_last_result['最新防治日期'] = df_last_result['最新防治日期'].dt.strftime('%Y-%m-%d')
    df_last_result['总防治次数'].fillna(0, inplace=True)
    # 按照日期和乡镇/街道排序
    df_last_result.sort_values(by=['调查日期', '乡镇/街道'], inplace=True)

    st.dataframe(df_last_result, use_container_width=True)
