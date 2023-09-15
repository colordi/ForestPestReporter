import sqlite3

import streamlit as st
import pandas as pd
from tools import get_last_result, get_current_status

st.sidebar.title('美国白蛾防治系统')
radio = st.sidebar.radio('请选择功能', ['巡查数据汇总', '防治台账'])


# 获取数据
def get_data(gen=1):
    # 建立数据库连接
    conn = sqlite3.connect('forestry_pests_2023.sqlite3')
    if gen == 1:
        pass
    elif gen == 2:
        # 执行SQL查询并获取数据
        query_survey = "SELECT * FROM `2023_美国白蛾_2代_调查表`"
        query_treatment = "SELECT * FROM `2023_美国白蛾_2代_防治表`"
        df_survey = pd.read_sql(query_survey, conn)
        df_treatment = pd.read_sql(query_treatment, conn)
    elif gen == 3:
        # 执行SQL查询并获取数据
        query_survey = "SELECT * FROM `2023_美国白蛾_3代_调查表`"
        query_treatment = "SELECT * FROM `2023_美国白蛾_3代_防治表`"
        df_survey = pd.read_sql(query_survey, conn)
        df_treatment = pd.read_sql(query_treatment, conn)
    # 关闭数据库连接
    conn.close()

    df_survey['调查日期'] = pd.to_datetime(df_survey['调查日期'], format='%Y-%m-%d')
    df_survey['派单时间'] = pd.to_datetime(df_survey['派单时间'], format='mixed')
    df_treatment['防治日期'] = pd.to_datetime(df_treatment['防治日期'], format='%Y-%m-%d')

    # 获取每个点位第一次受害的数据
    df_survey_filtered = df_survey[df_survey['受害株数'] > 0]
    df_survey_filtered_grouped = df_survey_filtered.groupby('点位编号')
    idx = df_survey_filtered_grouped['调查日期'].idxmin()
    df_first_damage = df_survey_filtered.loc[idx]
    return df_survey, df_treatment, df_first_damage


# 巡查数据汇总
if radio == '巡查数据汇总':
    def show_summary(gen=1):
        df_survey, df_treatment, df_first_damage = get_data(gen=gen)
        # 汇总信息
        total_survey_site_counts = len(df_survey)  # 总巡查点位数
        total_damage_site_counts = len(df_first_damage)  # 总受害点位数
        total_tree_counts = df_first_damage['受害株数'].sum()  # 总受害株数
        total_net_counts = df_first_damage['网幕数'].sum()  # 总网幕数
        # 乡镇总受害点位数
        town_damage_site_counts = len(df_first_damage[df_first_damage['区域'] == '乡镇'])
        # 城区总受害点位数
        city_damage_site_counts = len(df_first_damage[df_first_damage['区域'] == '城区'])
        # 乡镇总受害株数
        town_damage_tree_counts = df_first_damage[df_first_damage['区域'] == '乡镇']['受害株数'].sum()
        # 城区总受害株数
        city_damage_tree_counts = df_first_damage[df_first_damage['区域'] == '城区']['受害株数'].sum()
        # 乡镇总网幕数
        town_net_counts = df_first_damage[df_first_damage['区域'] == '乡镇']['网幕数'].sum()
        # 城区总网幕数
        city_net_counts = df_first_damage[df_first_damage['区域'] == '城区']['网幕数'].sum()

        # 展示汇总信息
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('### 巡查点位信息汇总\n')
            st.markdown(f'- 总巡查点位数：{total_survey_site_counts}\n')
            st.markdown(f'- 总受害点位数：:red[{total_damage_site_counts}]\n')
            st.markdown(f'- 城区受害点位数：{city_damage_site_counts}\n')
            st.markdown(f'- 乡镇受害点位数：{town_damage_site_counts}\n')
        with col2:
            st.markdown('### 巡查株数信息汇总\n')
            st.markdown(f'- 总受害株数：:red[{total_tree_counts}]\n')
            st.markdown(f'- 城区受害株数：{city_damage_tree_counts}\n')
            st.markdown(f'- 乡镇受害株数：{town_damage_tree_counts}\n')
        with col3:
            st.markdown('### 巡查网幕信息汇总\n')
            st.markdown(f'- 总网幕数：{total_net_counts}\n')
            st.markdown(f'- 城区网幕数：{city_net_counts}\n')
            st.markdown(f'- 乡镇网幕数：{town_net_counts}\n')
        return None


    def show_day_summary(gen=1):
        df_survey, df_treatment, df_first_damage = get_data(gen=gen)
        # 根据调查日期获取乡镇和城区各调查了多少点位
        town_date_sites = df_survey[df_survey['区域'] == '乡镇'].groupby('调查日期')['点位编号'].nunique()
        city_date_sites = df_survey[df_survey['区域'] == '城区'].groupby('调查日期')['点位编号'].nunique()

        # 根据调查日期获取乡镇和城区各受害株数
        town_date_damage = df_first_damage[df_first_damage['区域'] == '乡镇'].groupby('调查日期')['受害株数'].sum()
        city_date_damage = df_first_damage[df_first_damage['区域'] == '城区'].groupby('调查日期')['受害株数'].sum()

        # 根据调查日期获取乡镇和城区各受害点位数
        town_date_damage_sites = df_first_damage[df_first_damage['区域'] == '乡镇'].groupby('调查日期')[
            '点位编号'].nunique()
        city_date_damage_sites = df_first_damage[df_first_damage['区域'] == '城区'].groupby('调查日期')[
            '点位编号'].nunique()

        # 将上述数据合并到一个DataFrame中
        df_town = pd.DataFrame(
            {'调查点位数': town_date_sites, '受害点位数': town_date_damage_sites, '受害株数': town_date_damage})
        df_city = pd.DataFrame(
            {'调查点位数': city_date_sites, '受害点位数': city_date_damage_sites, '受害株数': city_date_damage})
        df_town.reset_index(inplace=True)
        df_city.reset_index(inplace=True)
        # 合并这两个表格
        df_town_city = pd.merge(df_town, df_city, how='outer', on=['调查日期'], suffixes=('_乡镇', '_城区'))
        df_town_city.fillna(0, inplace=True)
        # 索引从1开始
        df_town_city.index = df_town_city.index + 1

        # 展示数据
        st.header("每日巡查数据")
        df_town_city['调查日期'] = df_town_city['调查日期'].dt.strftime('%Y-%m-%d')
        # 排序
        df_town_city.sort_values(by='调查日期', inplace=True)
        st.dataframe(df_town_city, use_container_width=True)
        return None


    st.title("美国白蛾巡查统计汇总信息")
    tab1, tab2, tab3 = st.tabs(["第一代", "第二代", "第三代"])
    with tab1:
        # 展示汇总信息
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown('### 巡查点位信息汇总\n')
            st.markdown('- 总巡查点位数：1366\n')
            st.markdown('- 总受害点位数：:red[373]\n')
            st.markdown('- 城区受害点位数：258\n')
            st.markdown('- 乡镇受害点位数：115\n')
        with col2:
            st.markdown('### 巡查株数信息汇总\n')
            st.markdown('- 总受害株数：:red[1729]\n')
            st.markdown('- 城区受害株数：1161\n')
            st.markdown('- 乡镇受害株数：568\n')
        with col3:
            st.markdown('### 巡查网幕信息汇总\n')
            st.markdown('- 总网幕数：7337\n')
            st.markdown('- 城区网幕数：5057\n')
            st.markdown('- 乡镇网幕数：2280\n')
    with tab2:
        show_summary(gen=2)
        show_day_summary(gen=2)
    with tab3:
        show_summary(gen=3)
        show_day_summary(gen=3)

# 防治台账
elif radio == '防治台账':
    def show_treat_status(gen=1):
        df_survey, df_treatment, df_first_damage = get_data(gen=gen)
        total_damage_site_counts = len(df_first_damage)  # 受害点位数
        # 总防治点位数
        incomplete_sites = df_first_damage[df_first_damage['剪网是否彻底'] == '否']
        complete_sites = df_first_damage[df_first_damage['剪网是否彻底'] == '是']
        treated_sites = incomplete_sites[incomplete_sites['点位编号'].isin(df_treatment['点位编号'].tolist())]
        total_treated_site_counts = len(treated_sites) + len(complete_sites)
        # 防治点位占比
        total_qualified_site_counts = total_treated_site_counts / total_damage_site_counts

        # 展示汇总信息
        col1, col2, col3 = st.columns(3)
        col1.metric(label='总受害点位数', value=total_damage_site_counts)
        col2.metric(label='总已防治点位数', value=total_treated_site_counts)
        col3.progress(total_qualified_site_counts, '防治点位占比: {:.2%}'.format(total_qualified_site_counts))

        return None


    def show_ledger(gen=1):
        df_survey, df_treatment, df_first_damage = get_data(gen=gen)
        df_status = get_last_result(df_survey, df_treatment, df_first_damage)
        df_status['当前状态'] = df_status.apply(get_current_status, axis=1)
        # 修改列名的顺序
        df_status = df_status[
            ['调查日期', '区域', '乡镇/街道', '点位编号', '点位名', '发生位置', '地块类型', '危害寄主', '受害株数',
             '网幕数', '巡查是否剪网', '剪网是否彻底', '派单时间', '首次防治日期', '最新调查日期', '最新调查结果',
             '总调查次数', '总防治次数', '当前状态']]
        # 按照调查日期升序排列
        df_status.sort_values(by=['调查日期', '点位编号'], inplace=True)
        df_status.index = df_status.index + 1
        df_status['总防治次数'].fillna(0, inplace=True)

        # 展示数据
        st.subheader(f"2023 年美国白蛾第{gen}代防治台账")
        df_status['调查日期'] = df_status['调查日期'].dt.strftime('%Y-%m-%d')
        df_status['派单时间'] = df_status['派单时间'].dt.strftime('%Y-%m-%d')
        df_status['首次防治日期'] = df_status['首次防治日期'].dt.strftime('%Y-%m-%d')
        df_status['最新调查日期'] = df_status['最新调查日期'].dt.strftime('%Y-%m-%d')
        options = st.multiselect('请选择点位状态', ['待防治', '待复查', '合格'], default=['待防治', '待复查', '合格'],key=str(gen))
        # 根据选择的点位状态筛选数据
        filtered_df = df_status[df_status['当前状态'].isin(options)]
        # 重置索引
        filtered_df.reset_index(inplace=True, drop=True)
        # 索引从1开始
        filtered_df.index = filtered_df.index + 1
        st.dataframe(filtered_df, use_container_width=True)

        return None


    st.header("2023 年美国白蛾防治台账")
    tab1, tab2, tab3 = st.tabs(["第一代", "第二代", "第三代"])
    with tab1:
        pass
    with tab2:
        show_treat_status(gen=2)
        show_ledger(gen=2)
    with tab3:
        show_treat_status(gen=3)
        show_ledger(gen=3)
