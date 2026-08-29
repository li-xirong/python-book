# 配置参数模块
RAW_DATA_PATH = "cleaned_admission_lines.csv"  # 数据文件路径
# 高考人数配置
STUDENT_COUNT_2024 = 67200  # 2024年考生人数
STUDENT_COUNT_2025 = 78900  # 2025年考生人数
# 位次调整系数
RANK_ADJUSTMENT_RATIO = STUDENT_COUNT_2024 / STUDENT_COUNT_2025
# 推荐区间系数
CHALLENGE_LOWER = 0.85  # 冲击区间下限系数
CHALLENGE_UPPER = 0.95  # 冲击区间上限系数
STABLE_LOWER = 0.95     # 稳妥区间下限系数
STABLE_UPPER = 1.05     # 稳妥区间上限系数
SAFE_LOWER = 1.05       # 保底区间下限系数
SAFE_UPPER = 1.15       # 保底区间上限系数
# 每档最大推荐数量
MAX_RECOMMENDATIONS = 10
