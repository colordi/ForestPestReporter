import pandas as pd
import yaml
import pymysql

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
        conn = pymysql.connect(host=host, port=port, user=username, password=password, database=database)
        # 执行SQL查询并获取数据
        query_survey = "SELECT * FROM `2023年第二代美国白蛾调查表`"
        query_treatment = "SELECT * FROM `2023年第二代美国白蛾防治表`"
        df_survey = pd.read_sql(query_survey, conn)
        df_treatment = pd.read_sql(query_treatment, conn)

        # 关闭数据库连接
        conn.close()
    elif gen == 3:
        pass
    # 获取每个点位第一次受害的数据
    df_survey_filtered = df_survey[df_survey['受害株数'] > 0]
    df_survey_filtered_grouped = df_survey_filtered.groupby('点位编号')
    idx = df_survey_filtered_grouped['调查日期'].idxmin()
    df_first_damage = df_survey_filtered.loc[idx]
    return df_survey, df_treatment, df_first_damage
