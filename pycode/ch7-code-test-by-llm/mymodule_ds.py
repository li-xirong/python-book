def date_to_weekday(date_str):
    """将 'YYYY-MM-DD' 日期字符串转换为英文星期名（Zeller 公式）。"""
    if not isinstance(date_str, str):
        raise AttributeError("date_str must be a string")
    parts = date_str.split('-')
    # 必须是 3 段且每段为纯数字，否则视为格式错误
    if len(parts) != 3 or not all(p.isdigit() for p in parts):
        return "Invalid date format. Please use 'YYYY-MM-DD'."

    year, month, day = map(int, parts)
    # 1、2 月按上一年的 13、14 月处理
    if month < 3:
        year -= 1
        month += 12

    q, m = day, month
    k, j = year % 100, year // 100
    h = (q + 13 * (m + 1) // 5 + k + k // 4 + j // 4 + 5 * j) % 7
    weekdays = ["Saturday", "Sunday", "Monday", "Tuesday",
                "Wednesday", "Thursday", "Friday"]
    return weekdays[h]


