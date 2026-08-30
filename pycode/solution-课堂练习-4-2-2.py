import pandas as pd


raw_data = {
    "姓名": ["张三", "张三", "李四", "李四", "王五", "王五"],
    "学科": ["语文", "数学", "语文", "数学", "语文", "数学"],
    "成绩": [85, 92, 78, 88, 90, 85]
}
score_table = pd.DataFrame(raw_data)

# Solution 1: 基于pivot
new_table = score_table.pivot(index='姓名', columns='学科', values='成绩')
new_table = new_table.reset_index()
for subject in ['数学', '语文']:
    best = new_table[subject].argmax()
    print(f'{subject}成绩最高的是 {new_table['姓名'][best]}，{new_table[subject][best]}分')

# Solution 2: 基于boolean indexing
for subject in ['数学', '语文']:
    sub_table = score_table[score_table['学科'] == subject].reset_index(drop=True)
    best = sub_table['成绩'].argmax()
    print(f'{subject}成绩最高的是 {sub_table['姓名'][best]}，{sub_table['成绩'][best]}分')