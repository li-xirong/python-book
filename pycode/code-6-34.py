# 利用Streamlit展示DataFrame表格数据
import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")
with st.sidebar:
    year = st.selectbox("选择年份", [2021, 2022, 2023])
    prov = st.selectbox("选择省份", ["北京市", "浙江省", "福建省"])

st.header(f'{year}年-中国人民大学-{prov}录取分数线')
csv_file = f'pybook-data/ruc_data/{prov}/{year}.csv'
df = pd.read_csv(csv_file)
target_cols = [col for col in df.columns if col != '专业名称'] # 选择目标列
styler = df.style.format({c:'{:.0f}' for c in target_cols}) # 保留0位小数
# 高亮显示每列最高值与最低值
styler = styler.highlight_max(subset=target_cols, axis=0, color='lightgreen')
styler = styler.highlight_min(subset=target_cols, axis=0, color='lightyellow')
st.dataframe(styler)
