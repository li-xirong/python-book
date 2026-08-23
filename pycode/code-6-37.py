# 双按钮点击次数统计
import streamlit as st

if 'c1' not in st.session_state:
    st.session_state.c1 = 0
if 'c2' not in st.session_state:
    st.session_state.c2 = 0

if st.button('第一个按钮'):
    st.session_state.c1 += 1
    if st.button('第二个按钮'):
        st.session_state.c2 += 1

st.info(f'第1个按钮被点了{st.session_state.c1}次，第2个按钮被点了{st.session_state.c2}次')