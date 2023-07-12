import streamlit as st
import pandas as pd

# 调整页面布局
st.set_page_config(layout='wide')


# @st.cache_data
# 读取数据库
def get_data():
    # 读取调查表和防治表
    df_survey = pd.read_excel(r"data/第一代美国白蛾调查表.xlsx")
    df_treatment = pd.read_excel(r"data/第一代美国白蛾防治表.xlsx")
    return df_survey, df_treatment


df_survey, df_treatment = get_data()

# 获取每个点位第一次受害的数据
df_survey_filtered = df_survey[df_survey['受害株数'] > 0]
df_survey_filtered_grouped = df_survey_filtered.groupby('点位编号')
idx = df_survey_filtered_grouped['调查日期'].idxmin()
df_first_damage = df_survey_filtered.loc[idx]


# 定义展示汇总数据的函数
def show_summary_data():
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

    # 展示汇总信息
    st.header('汇总信息')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="总巡查点位数", value=total_survey_site_counts)
    with col2:
        st.metric(label="总受害点位数", value=total_damage_site_counts)
    with col3:
        st.metric(label="总受害株数", value=total_tree_counts)
    col4, col5, col6 = st.columns(3)
    with col4:
        st.metric(label="总网幕数", value=total_net_counts)
    with col5:
        st.metric(label="城区受害点位数", value=city_damage_site_counts)
    with col6:
        st.metric(label="城区受害株数", value=city_damage_tree_counts)
    col7, col8, col9 = st.columns(3)
    with col8:
        st.metric(label="乡镇受害点位数", value=town_damage_site_counts)
    with col9:
        st.metric(label="乡镇受害株数", value=town_damage_tree_counts)


# 定义展示巡查数据的函数
def show_survey_data():
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
    df = pd.merge(df_town, df_city, how='outer', on=['调查日期'], suffixes=('_乡镇', '_城区'))

    # 展示数据
    st.header("巡查数据")

    # 为了展示好看，将日期转换为字符串
    df['调查日期'] = df['调查日期'].dt.strftime('%Y-%m-%d')
    # 排序
    df.sort_values(by='调查日期', inplace=True)
    st.dataframe(df, use_container_width=True)


if __name__ == '__main__':
    # 设置页面标题
    st.title("美国白蛾巡查统计")
    # 展示汇总数据
    show_summary_data()
    # 展示巡查数据
    show_survey_data()
