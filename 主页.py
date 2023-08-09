import streamlit as st
import pandas as pd
import yaml
# 获取数据
from get_data import get_data

# 调整页面布局
st.set_page_config(layout='wide')


# 定义展示汇总数据的函数
def show_summary_data(df_survey, df_first_damage):
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
        st.markdown(
            '### 巡查点位信息汇总\n - 总巡查点位数：{}\n - 总受害点位数：:red[{}]\n - 城区受害点位数：{}\n - 乡镇受害点位数：{}'.format(
                total_survey_site_counts, total_damage_site_counts, city_damage_site_counts, town_damage_site_counts))
    with col2:
        st.markdown(
            '### 巡查株数信息汇总\n - 总受害株数：:red[{}]\n - 城区受害株数：{}\n - 乡镇受害株数：{}'.format(total_tree_counts,
                                                                                                    city_damage_tree_counts,
                                                                                                    town_damage_tree_counts))
    with col3:
        st.markdown('### 巡查网幕信息汇总\n - 总网幕数：{}\n - 城区网幕数：{}\n - 乡镇网幕数：{}'.format(total_net_counts,
                                                                                                      city_net_counts,
                                                                                                      town_net_counts))


# 定义展示巡查数据的函数
def show_survey_data(df_survey, df_first_damage):
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
    # 从数据库中获取数据
    df_survey_2, df_treatment_2, df_first_damage_2 = get_data(gen=2)

    tab1, tab2, tab3 = st.tabs(["第一代", "第二代", "第三代"])
    with tab1:
        # 展示汇总信息
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(
                '### 巡查点位信息汇总\n - 总巡查点位数：1366\n - 总受害点位数：:red[373]\n - 城区受害点位数：258\n - 乡镇受害点位数：115')
        with col2:
            st.markdown(
                '### 巡查株数信息汇总\n - 总受害株数：:red[1729]\n - 城区受害株数：1161\n - 乡镇受害株数：568')
        with col3:
            st.markdown('### 巡查网幕信息汇总\n - 总网幕数：7337\n - 城区网幕数：5057\n - 乡镇网幕数：2280')
    with tab2:
        # 展示汇总数据
        show_summary_data(df_survey=df_survey_2, df_first_damage=df_first_damage_2)
        # 展示巡查数据
        show_survey_data(df_survey=df_survey_2, df_first_damage=df_first_damage_2)
