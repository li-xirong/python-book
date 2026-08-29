from config import MAX_RECOMMENDATIONS

def get_recommendations(df, intervals, user_subjects):
    """
    根据位次区间和选科要求筛选推荐专业组
    Returns: dict with three categories of DataFrames
    """
    results = {}
    for category, (lower, upper) in intervals.items():
        # 筛选符合位次区间和选科要求的数据
        mask = (df['rank'] > lower) & (df['rank'] <= upper)
        # 根据选科筛选（不限或包含用户选科）
        if user_subjects:
            subject_mask = df['subject_limit'].str.contains('不限', na=False) | df['subject_limit'].str.contains('|'.join(user_subjects))
            mask = mask & subject_mask
        filtered = df[mask].copy()
        # 按位次排序并限制数量
        results[category] = filtered.sort_values('rank').head(MAX_RECOMMENDATIONS)
    return results
