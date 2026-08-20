# 基于Streamlit的用户信息收集表单
import streamlit as st

st.title("用户信息收集")

with st.form("user_info_form"):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("姓名*")
        age = st.number_input("年龄", 0, 120, 25)
        email = st.text_input("邮箱*")
    with col2:
        gender = st.radio("性别", ["男", "女", "其他"], horizontal=True)
        interests = st.multiselect("兴趣", ["阅读", "运动", "音乐", "旅行", "编程"])
        newsletter = st.checkbox("订阅通讯")

    submitted = st.form_submit_button("提交")
    if submitted:
        if not name or not email:
            st.error("请填写必填字段（带*的）")
        else:
            st.success("信息提交成功！")
            st.json({"姓名":name, "年龄":age, "邮箱":email, "性别":gender, "兴趣":interests, "订阅通讯":newsletter})
