"""date_to_weekday：根据 'YYYY-MM-DD' 字符串返回英文星期名。

错误处理约定（与测试用例保持一致）：
  - 非字符串输入（None/int/tuple/bytes）-> 抛出 AttributeError
  - 格式错误（分隔符、字段数、非数字、空白等）-> 返回 INVALID_MSG
  - 数字但位数不足（如 '23-1-1'）   -> 抛出 ValueError
  - 日历非法（2月30日、13月等）     -> 抛出 ValueError（date 构造自然抛出）
  - 早于 1900-01-01               -> 抛出 ValueError
"""
import re
from datetime import date

MIN_DATE = date(1900, 1, 1)  # 支持的最小日期
INVALID_MSG = "Invalid date format. Please use 'YYYY-MM-DD'."
# date.weekday() 的返回值：0=Monday ... 6=Sunday
_WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday",
             "Friday", "Saturday", "Sunday"]


def date_to_weekday(date_str):
    """返回 date_str 对应的英文星期名；非法输入按模块 docstring 的约定处理。"""
    if not isinstance(date_str, str):
        # None/int/tuple 无 .split，bytes.split 则抛 TypeError；统一为 AttributeError
        raise AttributeError("date_str must be a str, got %r" % type(date_str).__name__)
    m = re.fullmatch(r"(\d{4})-(\d{2})-(\d{2})", date_str)
    if m:
        y, mo, d = map(int, m.groups())
        dt = date(y, mo, d)  # 日历非法（如 2 月 30 日、13 月）在此抛出 ValueError
        if dt < MIN_DATE:
            raise ValueError("dates before 1900-01-01 are not supported")
        return _WEEKDAYS[dt.weekday()]
    # 能拆成 3 个整数但位数不对（如 '23-1-1'）：属越界输入，抛错而非返回提示
    if re.fullmatch(r"\d+-\d+-\d+", date_str):
        raise ValueError("date components must be zero-padded, e.g. 'YYYY-MM-DD'")
    return INVALID_MSG
