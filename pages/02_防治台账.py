import streamlit as st
import pandas as pd
from home import df_survey, df_treatment, df_first_damage


# 定义一个函数用于获取最新一次的调查结果和防治结果
def get_last_result():
    df_survey_grouped = df_survey.groupby('点位编号')
    df_survey_res = df_survey_grouped.apply(lambda g: pd.Series({
        '总调查次数': g['调查日期'].count(),
        '最新调查日期': g['调查日期'].max(),
        '最新调查结果': g.loc[g['调查日期'].idxmax(), '调查结果']
    }))
    df_treatment_grouped = df_treatment.groupby('点位编号')
    df_treatment_res = df_treatment_grouped.apply(lambda g: pd.Series({
        '总防治次数': g['防治日期'].count(),
        '最新防治日期': g['防治日期'].max(),
        '首次防治日期': g['防治日期'].min(),
    }))
    df_last_result = pd.merge(df_survey_res, df_treatment_res, on='点位编号', how='outer')
    # 把点位编号作为列
    df_last_result.reset_index(inplace=True)
    # df_last_result的点位需要过滤，必须在df_first_damage中才能显示
    df_last_result = pd.merge(df_last_result, df_first_damage, on='点位编号', how='inner')

    return df_last_result


# 定义用于根据业务逻辑计算每个点位的当前状态的函数
def get_current_status(row):
    if pd.isnull(row['最新防治日期']) or row['最新调查日期'] > row['最新防治日期']:
        if row['最新调查结果'] == '合格':
            return '合格'
        else:
            return '待防治'
    else:
        return '待复查'


# 展示当前点位信息
df_last_result_all = get_last_result()
df_last_result_all['当前状态'] = df_last_result_all.apply(get_current_status, axis=1)
# 修改列名的顺序
df_last_result = df_last_result_all[
    ['点位编号', '最新调查日期', '最新防治日期', '最新调查结果', '总调查次数', '总防治次数', '当前状态']]


def show_current_status():
    total_damage_site_counts = len(df_first_damage)  # 总受害点位数
    # 总已经防治点位数，即初次受害点位中剪网是否彻底为是的点位数和为否且防治次数大于0的点位数
    # 剪网是否彻底为否的点位数据
    no_treated_site_counts = df_first_damage[df_first_damage['剪网是否彻底'] == '否']
    print(len(no_treated_site_counts))
    # 从df_treatment中将点位编号转换为列表
    treatment_list = df_treatment['点位编号'].tolist()
    no_treated_site_counts = len(no_treated_site_counts[no_treated_site_counts['点位编号'].isin(treatment_list)])
    # 剪网是否彻底为是的点位数
    yes_treated_site_counts = len(df_first_damage[df_first_damage['剪网是否彻底'] == '是'])
    print(yes_treated_site_counts)
    total_treated_site_counts = no_treated_site_counts + yes_treated_site_counts
    # 合格点位数
    total_qualified_site_counts = len(df_last_result[df_last_result['当前状态'] == '合格'])
    # 使用监视器展示
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label='总受害点位数', value=total_damage_site_counts)
    with col2:
        st.metric(label='总已防治点位数', value=total_treated_site_counts)
    with col3:
        st.metric(label='合格点位数', value=total_qualified_site_counts)

    # 为了展示好看，将日期转换为字符串格式
    df_last_result['最新调查日期'] = df_last_result['最新调查日期'].dt.strftime('%Y-%m-%d')
    df_last_result['最新防治日期'] = df_last_result['最新防治日期'].dt.strftime('%Y-%m-%d')

    # 展示整体的防治台账
    x = df_last_result_all.copy()
    x = x[['调查日期','区域','乡镇/街道','点位编号','点位名','发生位置','地块类型','危害寄主','受害株数','网幕数','巡查是否剪网',
           '剪网是否彻底','派单时间','首次防治日期','最新调查日期','最新调查结果','总调查次数','总防治次数','当前状态']]
    # 为了展示好看，将日期转换为字符串格式
    x['调查日期'] = x['调查日期'].dt.strftime('%Y-%m-%d')
    x['派单时间'] = x['派单时间'].dt.strftime('%Y-%m-%d')
    x['首次防治日期'] = x['首次防治日期'].dt.strftime('%Y-%m-%d')
    x['最新调查日期'] = x['最新调查日期'].dt.strftime('%Y-%m-%d')
    # 按照调查日期升序排列
    x.sort_values(by='调查日期', inplace=True)
    # 重置索引
    x.reset_index(inplace=True, drop=True)
    st.subheader('整体防治台账')
    st.dataframe(x, use_container_width=True)

    # 共展示3个数据框

    # 状态为待防治
    df_to_treat = df_last_result[df_last_result['当前状态'] == '待防治']
    df_to_treat.reset_index(inplace=True, drop=True)
    st.subheader('待防治点位')
    st.dataframe(df_to_treat, use_container_width=True)

    # 状态为待复查
    df_to_review = df_last_result[df_last_result['当前状态'] == '待复查']
    df_to_review.reset_index(inplace=True, drop=True)
    st.subheader('待复查点位')
    # 生成复查表的按钮
    col1, col2 = st.columns(2)
    if col1.button('生成复查表'):
        # 获取df_survey中调查日期为df_to_review中最新调查日期的数据且点位编号在df_to_review中的数据
        df_survey_copy = df_survey.copy()
        df_survey_copy['调查日期'] = df_survey_copy['调查日期'].dt.strftime('%Y-%m-%d')
        df_to_review_survey = pd.merge(df_survey_copy, df_to_review,
                                       left_on=['点位编号', '调查日期'], right_on=['点位编号', '最新调查日期'],
                                       how='inner')
        df_to_review_survey['时间'] = ""
        df_to_review_survey = df_to_review_survey[['乡镇/街道', '点位编号', '点位名', '时间', '发生位置','危害寄主',
                                                   '受害株数', '网幕数', '虫龄', '备注']]
        # df_to_review_survey.to_excel('复查表.xlsx', index=False)
        st.dataframe(df_to_review_survey, use_container_width=True)
        pass
    st.dataframe(df_to_review, use_container_width=True)
    if col2.button('清除复查表'):
        st.empty()

    # 状态为合格
    df_qualified = df_last_result[df_last_result['当前状态'] == '合格']
    df_qualified.reset_index(inplace=True, drop=True)
    st.subheader('合格点位')
    st.dataframe(df_qualified, use_container_width=True)


if __name__ == '__main__':
    show_current_status()
    pass
