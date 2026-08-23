# 利用会话状态记录按钮被点击次数
import streamlit as st

if 'counter' not in st.session_state:
    st.session_state.counter = 0

if st.button('点我'):
    st.session_state.counter += 1

st.info(f'按钮被点了{st.session_state.counter}次')

