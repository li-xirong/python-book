
# 高考志愿填报推荐系统（大模型辅助生成）


## 数据准备

Step 1. 利用[网络爬虫](crawler.py)抓取数据

```python
python crawler.py
```

Step 2. 对抓取的网页数据进行清洗
```python
python clean_data.py
```

## 运行推荐系统

```bash
streamlit run main.py
```

## 推荐系统代码框架

+ [main.py](main.py): Streamlit入口，页面布局与逻辑
+ [config.py](config.py): 配置参数（人数、区间系数等）
+ [data\_loader.py](data_loader.py): 数据加载与预处理
+ [calculator.py](calculator.py): 位次调整与区间计算逻辑
+ [recommender.py](recommender.py): 推荐算法实现
+ [ui\_components.py](ui_components.py): UI组件渲染函数




