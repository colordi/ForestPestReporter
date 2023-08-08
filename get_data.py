import pandas as pd
import yaml
from sqlalchemy import create_engine

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
        # 建立数据库连接
        engine = create_engine('mysql+pymysql://{}:{}@{}:{}/{}'.format(username, password, host, port, database))
        # 执行SQL查询并获取数据
        query_survey = "SELECT * FROM `2023年第二代美国白蛾调查表`"
        query_treatment = "SELECT * FROM `2023年第二代美国白蛾防治表`"
        df_survey = pd.read_sql(query_survey, engine)
        df_survey['调查日期'] = pd.to_datetime(df_survey['调查日期'], format='%Y-%m-%d')
        df_survey['派单时间'] = pd.to_datetime(df_survey['派单时间'], format='%Y-%m-%d')
        df_treatment = pd.read_sql(query_treatment, engine)
        df_treatment['防治日期'] = pd.to_datetime(df_treatment['防治日期'], format='%Y-%m-%d')
        # 关闭数据库连接
        engine.dispose()
    elif gen == 3:
        pass
    print(df_survey.info())
    # 获取每个点位第一次受害的数据
    df_survey_filtered = df_survey[df_survey['受害株数'] > 0]
    df_survey_filtered_grouped = df_survey_filtered.groupby('点位编号')
    idx = df_survey_filtered_grouped['调查日期'].idxmin()
    df_first_damage = df_survey_filtered.loc[idx]
    return df_survey, df_treatment, df_first_damage
