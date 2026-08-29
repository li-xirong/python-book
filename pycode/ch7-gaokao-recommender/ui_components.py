import streamlit as st

def render_recommendation_section(recommendations):
    """渲染三列推荐结果"""
    cols = st.columns(3)
    category_names = {
        'challenge': ('冲一冲', '冲击院校，录取概率约30-50%'),
        'stable': ('稳一稳', '稳妥选择，录取概率约70-80%'),
        'safe': ('保一保', '保底院校，录取概率>90%')
    }
    for idx, (category, df) in enumerate(recommendations.items()):
        with cols[idx]:
            title, desc = category_names[category]
            st.markdown(f"### {title}")
            st.caption(desc)
            if df.empty:
                st.info("该区间暂无推荐")
                continue
            for _, row in df.iterrows():
                with st.container():
                    st.markdown(f"**{row['college_name']}**")
                    st.markdown(f"专业组: {row['group_code']}\t|\t选考科目: {row['subject_limit']}\t|\t位次: {row['rank']}\t|\t投档线: {row['score']}分")
                    st.divider()
