import streamlit as st

update = """
# 更新记录
- 2023-09-12的数据已上传，且更新防治记录；
- 2023-09-11的数据已上传；
- 2023-09-10的数据已上传；
- 2023-09-08的数据已上传；
- 2023-09-07的数据已上传；
- 2023-09-06的数据已上传；
"""


# 调整页面布局
st.set_page_config(layout='wide')

if __name__ == '__main__':
    # 设置页面标题
    st.title("林业有害生物防治系统")
    st.markdown(update)
