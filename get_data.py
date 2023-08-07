import pandas as pd
import yaml

# 读取配置文件
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

# 提取连接信息
host = config["database"]["host"]
port = config["database"]["port"]
username = config["database"]["username"]
password = config["database"]["password"]
database = config["database"]["database"]


def get_data(gen=1):
    # 读取调查表和防治表
    if gen == 1:
        pass
    elif gen == 2:
        # 从MySQL数据库中读取调查表和防治表
        df_survey = pd.read_sql_table('2023年第二代美国白蛾调查表',
                                      'mysql+pymysql://{}:{}@{}:{}/{}'.format(username, password, host, port, database))
        df_treatment = pd.read_sql_table('2023年第二代美国白蛾防治表',
                                         'mysql+pymysql://{}:{}@{}:{}/{}'.format(username, password, host, port,
                                                                                 database))
    elif gen == 3:
        pass
    # 获取每个点位第一次受害的数据
    df_survey_filtered = df_survey[df_survey['受害株数'] > 0]
    df_survey_filtered_grouped = df_survey_filtered.groupby('点位编号')
    idx = df_survey_filtered_grouped['调查日期'].idxmin()
    df_first_damage = df_survey_filtered.loc[idx]
    return df_survey, df_treatment, df_first_damage


df_survey_2, df_treatment_2, df_first_damage_2 = get_data(gen=2)
