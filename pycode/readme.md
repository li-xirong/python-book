# 教材中使用的.py源代码

## 第6章

+ [示例代码6.30](code-6-30.py): Streamlit多列布局
+ [示例代码6.34](code-6-34.py): 利用Streamlit展示DataFrame表格数据
+ [示例代码6.36](code-6-36.py): 利用会话状态记录按钮被点击次数
+ [示例代码6.37](code-6-37.py): 双按钮点击次数统计
+ [示例代码6.38](code-6-38.py): 基于Streamlit的学生信息查询系统
+ [示例代码6.37修正版](code-6-37-bugfix.py): 点击“再来一局”能正常重启游戏

## 第7章

+ [示例代码7.2](code-7-2.py): 大模型给出的网页版猜数字游戏程序（Streamlit）
+ [示例代码7.3](code-7-3-bugfix.py): 大模型改正后的网页版猜数字游戏程序
+ [示例代码7.4](code-7-4.py): 大模型生成的网页数据爬虫代码（保存为crawler.py后运行）
+ [示例代码7.5](code-7-5.py): 大模型生成的网页数据清洗代码（数据文件见 pybook-data/ch7）
+ [示例代码7.6～7.11](ch7-gaokao-recommender/): 高考志愿填报推荐系统（Streamlit多模块项目）
  - [config.py](ch7-gaokao-recommender/config.py): 配置参数模块（示例代码7.6）
  - [data_loader.py](ch7-gaokao-recommender/data_loader.py): 数据加载与预处理（示例代码7.7）
  - [calculator.py](ch7-gaokao-recommender/calculator.py): 位次调整与区间计算（示例代码7.8）
  - [recommender.py](ch7-gaokao-recommender/recommender.py): 推荐算法实现（示例代码7.9）
  - [ui_components.py](ch7-gaokao-recommender/ui_components.py): 推荐结果可视化（示例代码7.10）
  - [main.py](ch7-gaokao-recommender/main.py): 主程序（示例代码7.11），运行 `streamlit run main.py` 启动
+ [示例代码7.12～7.14](ch7-test-debug/): 日期转星期函数的测试与调试
  - [mymodule.py](ch7-test-debug/mymodule.py): 基于Zeller公式的原始实现，带有隐患（示例代码7.12）
  - [test_date_weekday.py](ch7-test-debug/test_date_weekday.py): 大模型生成的pytest测试用例（示例代码7.13）
  - [mymodule_fixed.py](ch7-test-debug/mymodule_fixed.py): 经大模型纠正后的版本（示例代码7.14），可将其重命名为 mymodule.py 后复测
