import pandas as pd


def get_last_result(df_survey, df_treatment, df_first_damage):
    """
    :param df_survey: A pandas DataFrame containing survey data. It should have the following columns: 点位编号, 调查日期, 调查结果.
    :param df_treatment: A pandas DataFrame containing treatment data. It should have the following columns: 点位编号, 防治日期.
    :param df_first_damage: A pandas DataFrame containing the first damage data. It should have the following columns: 点位编号.

    :return: A pandas DataFrame, df_last_result, containing the last survey and treatment results for each 点位编号 in df_first_damage, along with additional information. The columns in df_last_result are as follows: 点位编号, 总调查次数, 最新调查日期, 最新调查结果, 总防治次数, 最新防治日期, 首次防治日期.

    """
    df_survey_grouped = df_survey.groupby('点位编号')
    df_survey_res = df_survey_grouped.apply(lambda g: pd.Series({
        '总调查次数': g['调查日期'].count(),
        '上报次数': g['上报时间'].count(),
        '最新调查日期': g['调查日期'].max(),
        '最新调查结果': g.loc[g['调查日期'].idxmax(), '调查结果']
    }))
    if df_treatment.empty:
        df_treatment_res = pd.DataFrame(columns=['点位编号', '总防治次数', '最新防治日期', '首次防治日期'])
    else:
        df_treatment_grouped = df_treatment.groupby('点位编号')
        df_treatment_res = df_treatment_grouped.apply(lambda g: pd.Series({
            '总防治次数': g['防治日期'].count(),
            '最新防治日期': g['防治日期'].max(),
            '首次防治日期': g['防治日期'].min(),
        }))

    # 把索引列点位编号转换为普通列
    df_survey_res.reset_index(inplace=True)
    df_treatment_res.reset_index(inplace=True)
    df_last_result = pd.merge(df_survey_res, df_treatment_res, on='点位编号', how='outer')
    # df_last_result的点位需要过滤，必须在df_first_damage中才能显示
    df_last_result = pd.merge(df_last_result, df_first_damage, on='点位编号', how='inner')

    return df_last_result


# 定义用于根据业务逻辑计算每个点位的当前状态的函数
def get_current_status(row):
    """
    Get current status based on the row data.

    :param row: A row of data containing the necessary fields for determining the current status.
    :return: The current status of the row.

    """
    if pd.isnull(row['最新防治日期']) or row['最新调查日期'] > row['最新防治日期']:
        if row['最新调查结果'] == '合格':
            return '合格'
        else:
            return '待防治'
    else:
        return '待复查'


def filter_data(data, date):
    return data[data['日期'] == pd.to_datetime(date)]
