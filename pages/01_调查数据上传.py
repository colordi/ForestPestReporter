import streamlit as st
import pandas as pd


def upload_excel_to_database():
    # 创建一个上传文件的控件
    uploaded_file = st.file_uploader("上传Excel文件", type=["xlsx", "xls"])

    if uploaded_file is not None:
        # 使用Pandas读取上传的Excel文件
        df = pd.read_excel(uploaded_file)
        # 将上传的数据保存到data文件夹下
        df.to_excel(r"data/{}".format(uploaded_file.name), index=False)
        # 将上传的数据合并到df_survey中
        df_survey = pd.read_excel(r"data/第一代美国白蛾调查表.xlsx")
        # 合并之前，先确定两个表的列名是一致的，否则提示用户上传的数据格式不正确
        if set(df.columns) != set(df_survey.columns):
            st.error("上传的数据格式不正确，请检查！")
        else:
            df_survey = pd.concat([df_survey, df], axis=0)
            df_survey.to_excel(r"data/第一代美国白蛾调查表.xlsx", index=False)
            # 提示上传成功
            st.success("上传成功！")


def show_sample_data():
    text = """
    请确保上传的数据字段和格式和如下内容一致，示例数据如下：
    - 调查日期：如2023/01/01，必须为日期格式;
    - 区域：乡镇或者城区二选一；
    - 乡镇/街道：具体街道或乡镇名称，如永乐店镇，其中于家务必须为于家务回族乡；
    - 点位编号：巡查点编号，如YS04；
    - 点位名：如西槐庄路；
    - 地块类型：行道树、小区绿化、公园绿化等；
    - 危害寄主：需要如同如下格式，海棠2，杨树4，不同的寄主之间用中文逗号隔开；
    - 受害株数：2；
    - 网幕数：16；
    - 虫龄：一般留空；
    - 巡查是否剪网：是或否；
    - 剪网是否彻底：是或否；
    - 上报时间：如2023/6/20 8:31:00，同样需为日期时间格式；
    - 详细描述：例如，复查，西槐庄路西槐庄村南，海棠2棵，杨树4棵，网幕16处， 海棠防治合格，杨树部分还有活虫，防治不合格；
    - 调查结果：合格或不合格，**注意，该字段非常重要，必须为合格或不合格，否则无法上传！**；
    - 派单时间：派单时间默认情况下为巡查时间的第二天，遇到周末或者节假日则顺延；
    - 备注：如有需要，可在此处添加备注信息。
    """
    st.markdown(text)
    st.markdown(":red[请一定确认字段名称完全一致！]")
    # 可以点击下面的按钮下载示例数据
    with open('template/白蛾巡查数据录入模板.xlsx', 'rb') as file:
        st.download_button("下载示例数据", data=file, file_name='白蛾示例数据.xlsx')


if __name__ == '__main__':
    st.header("上传Excel文件")
    show_sample_data()
    upload_excel_to_database()
