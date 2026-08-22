# 基于Streamlit 的学生信息查询系统
import streamlit as st
import pandas as pd
import os

student_file = 'pybook-data/ch3/rawdata.txt'
photo_dir = 'pybook-data/ch3/portraits'
columns = '姓名,性别,出生日期,学号,所属学院,入学年份,籍贯,GPA,总学分'.split(',')
df = pd.read_csv(student_file, header=None, names=columns)

st.set_page_config(layout="wide")
st.title('学生信息查询系统')
col1, col2 = st.columns(2, gap="large")

with col1:
    st.dataframe(df)

with col2:
    with st.form("query_form"):
        query = st.text_input("请输入学号:")
        submitted = st.form_submit_button("查询")
        if submitted:
            result = df[df['学号'].astype('str')==query]
            if not result.empty:
                st.info('查询结果')
                st.dataframe(result)
                st.image(os.path.join(photo_dir,f'{query}.png'), width=200)
            else:
                st.warning(f'学号{query}不存在')


