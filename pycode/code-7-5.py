import pandas as pd
# 读取并清洗分段表
df_score = pd.read_html('gaokao_page_2.html')[0].iloc[1:].reset_index(drop=True)
df_score.columns = ['分数', '人数', '位次']
# 定位并删除本科线之后的行（假设本科线行包含文本标注）
undergrad_idx = df_score[df_score['分数'].astype(str).str.contains('本科线')].index
if len(undergrad_idx):
    df_score = df_score.iloc[:undergrad_idx[0]+1]
# 提取分数数字，处理第一行特殊情况
df_score['分数'] = df_score['分数'].astype(str).str.extract(r'(\d+)')[0]
df_score.loc[0, '分数'] = '700'  # 将"700-750"简化为"700"
df_score['分数'] = pd.to_numeric(df_score['分数'])
# 创建分数-位次映射字典
score_to_rank = dict(zip(df_score['分数'], df_score['位次']))
# 读取并清洗投档线表
df_admission = pd.read_html('gaokao_page_1.html')[0].iloc[1:].reset_index(drop=True)
df_admission.columns = ['院校代码', '院校', '专业组代码', '限制', '投档线']
df_admission['投档线'] = pd.to_numeric(df_admission['投档线'].astype(str).str.extract(r'(\d+)')[0])
# 添加位次列（通过映射字典）
df_admission['位次'] = df_admission['投档线'].map(score_to_rank)
# 输出CSV文件
df_score.to_csv('cleaned_score_segments.csv', index=False, encoding='utf-8-sig')
df_admission.to_csv('cleaned_admission_lines.csv', index=False, encoding='utf-8-sig')
