import streamlit as st
import random

if 'target' not in st.session_state:          # 第一访问或刷新时初始化
    st.session_state.target = random.randint(1, 1000)
    st.session_state.tries = 0
st.title("猜数字游戏（1-1000）")
guess = st.number_input("输入你的猜测：", min_value=1, max_value=1000, step=1)
if st.button("猜！"):
    st.session_state.tries += 1
    if guess == st.session_state.target:
        st.success(f"恭喜，猜对了！共猜了 {st.session_state.tries} 次。")
        if st.button("再来一局"):
            for key in ('target', 'tries'):
                del st.session_state[key]
            st.rerun()
    else:
        st.info("大了" if guess > st.session_state.target else "小了")
