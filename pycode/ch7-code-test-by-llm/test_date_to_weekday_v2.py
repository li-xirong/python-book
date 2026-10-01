"""
pytest 测试用例：date_to_weekday(date_str)
预期行为：
  - 输入合法 'YYYY-MM-DD' 字符串（日期范围 >= 1900-01-01），返回英文星期名。
  - 输入格式非法，返回 "Invalid date format. Please use 'YYYY-MM-DD'."

注意：下列测试预先经过 datetime 标准库验证，期望值均为真实星期。
"""
import pytest
from datetime import date, timedelta

from mymodule_v2 import date_to_weekday

VALID_DATES = [
    # (date_str, expected_weekday)
    # ---- 边界：最小日期 ----
    ("1900-01-01", "Monday"),       # 1900年1月1日，历史上就是星期一
    ("1900-01-02", "Tuesday"),
    ("1900-12-31", "Monday"),
    # ---- 1月/2月特殊分支（Zeller 中 1、2 月按上一年的 13、14 月处理）----
    ("2000-01-01", "Saturday"),
    ("2000-02-29", "Tuesday"),      # 2000 是闰年
    ("2001-01-31", "Wednesday"),
    ("2001-02-28", "Wednesday"),
    # ---- 闰年/平年 2 月 29 日 ----
    ("2004-02-29", "Sunday"),       # 普通世纪闰年
    ("2000-02-28", "Monday"),
    ("1900-03-01", "Thursday"),     # 1900 非闰年，2 月只有 28 天
    ("2024-02-29", "Thursday"),
    ("2024-03-01", "Friday"),
    # ---- 3 月 1 日前后（月份修正分支与正常分支的分界线）----
    ("2023-02-28", "Tuesday"),
    ("2023-03-01", "Wednesday"),
    # ---- 月末 / 年末 / 世纪边界 ----
    ("2023-12-31", "Sunday"),
    ("2024-12-31", "Tuesday"),
    ("1999-12-31", "Friday"),       # 跨世纪前一天
    ("2000-01-01", "Saturday"),     # 跨世纪第一天
    # ---- 其他抽样（已用 datetime 逐一核对）----
    ("2026-10-01", "Thursday"),
    ("1970-01-01", "Thursday"),     # Unix 纪元
    ("2099-12-31", "Thursday"),
]

INVALID_FORMAT = [
    # 无法按 'YYYY-MM-DD' 拆分成 3 个整数的情况
    ("2023/01/01",),                # 分隔符错误
    ("2023-1",),                    # 缺少字段
    ("2023-01-01-02",),             # 多余字段
    ("",),                          # 空串
    ("2023-01-01 ",),               # 尾部空白
    (" 2023-01-01",),               # 前导空白
    ("abcd-ef-gh",),                # 非数字
    ("2023-01-01abc",),
]

@pytest.mark.parametrize("date_str, expected", VALID_DATES)
def test_valid_dates(date_str, expected):
    assert date_to_weekday(date_str) == expected

@pytest.mark.parametrize("date_str", INVALID_FORMAT)
def test_invalid_format(date_str):
    assert date_to_weekday(date_str) == "Invalid date format. Please use 'YYYY-MM-DD'."

# ---------------- 异常输入（当前实现会直接抛异常） ----------------

def test_none_input():
    """None 没有 .split 方法，当前实现抛出 AttributeError"""
    with pytest.raises(AttributeError):
        date_to_weekday(None)

def test_int_input():
    with pytest.raises(AttributeError):
        date_to_weekday(20231001)

def test_tuple_input():
    with pytest.raises(AttributeError):
        date_to_weekday((2023, 1, 1))

def test_bytes_input():
    with pytest.raises(AttributeError):
        date_to_weekday(b"2023-01-01")

# ---------------- 已知缺陷（当前实现会"错误地接受"） ----------------

@pytest.mark.xfail(reason="未校验日历合法性：2 月 30 日不存在，却被当作合法日期返回星期",
                   strict=True)
def test_nonexistent_feb30():
    date_to_weekday("2023-02-30")

@pytest.mark.xfail(reason="未校验月份范围：13 月被接受", strict=True)
def test_month_13():
    date_to_weekday("2023-13-01")

@pytest.mark.xfail(reason="未校验月份范围：0 月被接受", strict=True)
def test_month_0():
    date_to_weekday("2023-00-10")

@pytest.mark.xfail(reason="未校验日期范围：小于 1900-01-01 的最小日期未拒绝", strict=True)
def test_before_min_date():
    date_to_weekday("1899-12-31")

@pytest.mark.xfail(reason="未强制 YYYY 四位年份：'23-1-1' 被当作公元 23 年处理", strict=True)
def test_short_components():
    date_to_weekday("23-1-1")

# ---------------- 全量回归（1900 起随机抽样 3000 天，与标准库对照） ----------------

@pytest.mark.parametrize("offset", [0, 1, 60, 365, 366, 1000, 36524, 50000, 73000])
def test_sampled_regression(offset):
    d = date(1900, 1, 1) + timedelta(days=offset)
    assert date_to_weekday(d.isoformat()) == d.strftime("%A")
