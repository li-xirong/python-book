import io

csv_data = '''麦当劳 35
沙县小吃 15
海底捞火锅 120
轻食沙拉日记 45'''
df = pd.read_csv(io.StringIO(csv_data), sep=' ', names=['餐厅', '消费'])
print(f'共消费了{df['消费'].sum()}元')
