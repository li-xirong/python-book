from datetime import datetime

_WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
def date_to_weekday(date_str: str) -> str:
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        if dt.year < 1900:                       # 低于题目最小日期
            raise ValueError
    except Exception:
        return "Invalid date format. Please use 'YYYY-MM-DD'."

    # Zeller 公式（简化版）（1900-03-01 起可直接用，1/2 月按上年处理）
    y, m, d = dt.year, dt.month, dt.day
    if m < 3:
        y -= 1
        m += 12
    k, j = y % 100, y // 100
    h = (d + (13 * (m + 1)) // 5 + k + k // 4 + j // 4 + 5 * j) % 7
    # Zeller 原始映射 0=Saturday..6=Friday，与 _WEEKDAYS 顺序对齐
    return _WEEKDAYS[(h + 5) % 7]        # +5 偏移使 0->Monday..6->Sunday
