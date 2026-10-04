
# 大模型辅助代码测试与调试


+ [原始目标函数](mymodule.py): 基于Zeller公式实现的日期转星期几的函数，带有隐患


## 代码测试

### 提示词

>你是一个Python程序测试专家，善于生成各种测试样例，用于发现程序中的不完善之处。
>请为附件中的date_to_weekday函数生成一组pytest风格的全面的测试用例。要求尽可能多地覆盖边界条件、异常场景和正常功能。
>最小日期设置为 1900 年 1 月 1 日。

+ [Kimi生成的测试代码](test_date_to_weekday.py)
+ [测试日志](test.log): 执行`pytest -q test_date_to_weekday.py`后产生的测试日志


## 代码调试


### 提示词

>你是一个Python程序调试专家，善于根据代码的测试结果，发现并修改程序中的不完善之处。
>下面是我写的代码和测试信息。请帮我检查并调式，找出其中的错误，给出最终改进后的代码。
>+ 目标函数date_to_weekday位于mymodule.py
>+ 测试脚本为test_date_to_weekday.py
>+ 测试日志为test.log
>在确保代码正确的前提下，代码尽可能简洁高效（最好不超过50行），且要包含必要的注释。

+ [Kimi修改方案](mymodule_kimi.py), 测试命令`pytest -q test_date_to_weekday_kimi.py`
+ [DeepSeek修改方案](mymodule_ds.py), 测试命令`pytest -q test_date_to_weekday_ds.py`

