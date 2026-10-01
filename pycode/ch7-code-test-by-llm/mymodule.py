def date_to_weekday(date_str):
    try:
        year, month, day = map(int, date_str.split('-'))
    except:
        return "Invalid date format. Please use 'YYYY-MM-DD'."
    if month < 3:
        year -= 1
        month += 12 #1月和2月变为上一年的13月和14月
    q = day
    m = month
    k = year % 100
    j = year // 100
    h = (q + (13 * (m + 1)) // 5 + k + k // 4 + j // 4 + 5 * j) % 7
    weekdays = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    return weekdays[h]
