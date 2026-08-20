import streamlit as st

cols = st.columns(3)
headers = '冲击区间 稳妥区间 保底区间'.split()
colleages = 'A大学 B大学 C大学'.split()
subjects = 'D专业 E专业 F专业'.split()

for i,col in enumerate(cols):
    with col:
        st.header(headers[i])
        st.subheader(f'{colleages[i]}')
        st.write(f'{subjects[i]}')
