import streamlit as st
from data_loader import load_admission_data
from calculator import adjust_rank_for_2025, calculate_recommendation_intervals
from recommender import get_recommendations
from ui_components import render_recommendation_section

def main():
    st.set_page_config(page_title="北京高考志愿推荐系统", layout="wide")
    st.title("�� 北京高考志愿智能推荐")
    st.caption("基于2024年录取数据为2025年考生提供参考")
    # 用户输入区域
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            user_rank = st.number_input("请输入您的市排名（位次）", min_value=1, max_value=78900, value=5000,step=1)
        with col2:
            subject_options = ['物理', '化学', '生物', '政治', '历史', '地理']
            selected_subjects = st.multiselect("请选择您的选考科目（可不选）", subject_options)
    # 生成推荐
    if st.button("生成推荐方案", type="primary"):
        with st.spinner("正在分析数据..."):
            # 加载数据
            df = load_admission_data("cleaned_admission_lines.csv")
            # 计算等效位次和区间
            adjusted_rank = adjust_rank_for_2025(user_rank)
            intervals = calculate_recommendation_intervals(adjusted_rank)
            # 获取推荐
            recommendations = get_recommendations(df, intervals, selected_subjects)
            # 显示统计信息
            st.info(f"您的位次: **{user_rank:,}** | 调整后等效2024年位次: **{adjusted_rank:,}**")
            # 渲染结果
            render_recommendation_section(recommendations)
if __name__ == "__main__":
    main()
