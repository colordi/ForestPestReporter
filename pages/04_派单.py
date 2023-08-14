import os
import shutil

import streamlit as st
import pandas as pd
from datetime import date
from PIL import Image
from docx import Document
from docx.shared import Inches
from tools import get_engine

# 显示日期、虫种、代数选择器
col1, col2, col3 = st.columns(3)
with col1:
    selected_date = st.date_input('选择一个日期', value=date.today())
with col2:
    pest = st.selectbox('选择虫种', options=['美国白蛾', '国槐尺蠖'])
with col3:
    gen = st.selectbox('选择代数', options=[1, 2, 3])

# 用选定的内容来过滤数据
