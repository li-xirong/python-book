import pytest
from mymodule import date_to_weekday  # 被测函数
# 工具：已知正确结果对照表（可再扩充）
KNOWN_DATES = {
    "1900-01-01": "Monday",
    "1900-12-31": "Monday",
    "1999-12-31": "Friday",
    "2000-02-29": "Tuesday",   # 闰年
    "2023-12-31": "Sunday",
    "9999-12-31": "Friday",
}
class TestDateToWeekday:
    """全面测试 date_to_weekday 函数"""
    # 1. 已知的正确性对照
    @pytest.mark.parametrize("date_str, expected", KNOWN_DATES.items())
    def test_known_dates(self, date_str, expected):
        assert date_to_weekday(date_str) == expected
    # 此处省略部分代码    
    # 6. 月份 / 天数越界
    @pytest.mark.parametrize("bad_date",
        [   "1900-13-01",  # 13 月
            "1900-00-01",  # 0 月
            "1900-01-32",  # 32 日
            "1900-01-00",  # 0 日
            "1900-02-30",  # 非闰年 2-30
            "2023-04-31",  # 4 月只有 30 天
        ],)
    def test_out_of_range_date_returns_wrong_weekday(self, bad_date):
        # 当前实现不会抛错，但结果必错；可断言与任何正确星期都不匹配
        result = date_to_weekday(bad_date)
        assert result not in KNOWN_DATES.values()        
    # 7. 格式错误
    @pytest.mark.parametrize("bad_format",
        [   "23-06-15",      # 年不是 4 位
            "2023/06/15",    # 分隔符错
            "2023-6-15",     # 月不是 2 位
            "2023-06-5",     # 日不是 2 位
            "2023-06",       # 缺日
            "hello",         # 完全非法
            "",              # 空串
        ],  )
    def test_invalid_format_returns_error_message(self, bad_format):
        assert date_to_weekday(bad_format).startswith("Invalid date format")
    # 此处省略部分代码
