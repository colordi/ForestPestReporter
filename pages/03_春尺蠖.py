import sqlite3

from datetime import date

import streamlit as st
import pandas as pd
from tools import get_last_result, get_current_status, filter_data

# 查询数据
conn = sqlite3.connect('forestry_pests_2024.sqlite3')
adult_survey = pd.read_sql("SELECT * FROM `2024_春尺蠖_成虫_调查表`", conn)
larva_survey = pd.read_sql("SELECT * FROM `2024_春尺蠖_幼虫_调查表`", conn)
larva_treatment = pd.read_sql("SELECT * FROM `2024_春尺蠖_幼虫_防治表`", conn)
conn.close()

# 日期格式转换
adult_survey['日期'] = pd.to_datetime(adult_survey['日期'], format='%Y-%m-%d')
larva_survey['日期'] = pd.to_datetime(larva_survey['日期'], format='%Y-%m-%d')
larva_survey['派单时间'] = pd.to_datetime(larva_survey['派单时间'], format='mixed')
larva_treatment['日期'] = pd.to_datetime(larva_treatment['日期'], format='%Y-%m-%d')

# 成虫初次受害的数据
adult_damage_data = adult_survey[adult_survey['总虫量/10株'] > 0]
_ = adult_damage_data.groupby('点位编号')
idx = _['日期'].idxmin()
adult_damage_first = adult_damage_data.loc[idx]

# 幼虫初次受害的数据
larva_damage_data = larva_survey[larva_survey['总虫量/5枝'] > 0]
_ = larva_damage_data.groupby('点位编号')
idx = _['日期'].idxmin()
larva_damage_first = larva_damage_data.loc[idx]

tab1, tab2 = st.tabs(['巡查数据汇总', '防治台账'])
# 巡查数据汇总
with tab1:
    date = st.date_input('当前数据截止至：', value=date.today(), key='adult')

    # 过滤数据(根据日期)
    adult_survey = filter_data(adult_survey, date)
    adult_damage_first = filter_data(adult_damage_first, date)
    larva_survey = filter_data(larva_survey, date)
    larva_treatment = filter_data(larva_treatment, date)
    larva_damage_first = filter_data(larva_damage_first, date)

    # 成虫调查数据汇总
    st.markdown('## 羽化成虫巡查点位信息汇总\n')
    total_survey_site_counts = len(adult_survey)  # 总巡查点位数
    total_damage_site_counts = len(adult_damage_first)  # 总受害点位数
    total_pest_counts = adult_damage_first['总虫量/10株'].sum()  # 总虫口数
    per = total_damage_site_counts / total_survey_site_counts

    col1, col2,col3 = st.columns(3)
    col1.markdown(f'- 巡查点位数：{total_survey_site_counts}\n')
    col2.markdown(f'- :red[受害点位数：{total_damage_site_counts}]\n')
    col3.markdown(f'- :red[总虫口数：{total_pest_counts}]\n')
    st.progress(per, f":orange[受害占比{round(per * 100, 2)}%]")

    # 幼虫调查数据汇总
    st.markdown('## 幼虫巡查点位信息汇总\n')
    total_survey_site_counts = len(larva_survey)  # 总巡查点位数
    total_damage_site_counts = len(larva_damage_first)  # 总受害点位数
    total_pest_counts = larva_damage_first['总虫量/5枝'].sum()  # 总虫口数
    per = total_damage_site_counts / total_survey_site_counts

    col1, col2,col3 = st.columns(3)
    col1.markdown(f'- 巡查点位数：{total_survey_site_counts}\n')
    col2.markdown(f'- :red[受害点位数：{total_damage_site_counts}]\n')
    col3.markdown(f'- :red[总虫口数：{total_pest_counts}]\n')
    st.progress(per, f":orange[受害占比{round(per * 100, 2)}%]")
    # 防治点位数量计算
    treated_sites = len(larva_damage_data[larva_damage_data['点位编号'].isin(larva_treatment['点位编号'].tolist())])
    col1, col2 = st.columns(2)
    col1.markdown(f'- :red[已防治点位数：{treated_sites}]\n')
    per = treated_sites / total_damage_site_counts
    st.progress(per, f":orange[防治完成占比{round(per * 100, 2)}%]")

# 防治台账
with tab2:
    pass
