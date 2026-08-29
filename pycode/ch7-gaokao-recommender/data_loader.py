import pandas as pd

def load_admission_data(file_path):
    """
    加载并预处理录取数据
    Returns: DataFrame with columns: [code, name, group, subject_limit, score, rank]
    """
    df = pd.read_csv(file_path, encoding='utf-8-sig')
    # 标准化列名
    df.columns = ['college_code', 'college_name', 'group_code', 'subject_limit', 'score', 'rank']
    # 清理数据
    df = df.dropna(subset=['rank'])
    df['rank'] = df['rank'].astype(int)
    return df
