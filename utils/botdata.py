import math
from datetime import datetime
# from classcreate import add_file
# from classupdate import group_update

months = {"01": "Январь", "02": "Февраль", "03": "Март", "04": "Апрель", "05": "Май", "06": "Июнь",
          "07": "Июль", "08": "Август", "09": "Сентябрь", "10": "Октябрь", "11": "Ноябрь", "12": "Декабрь"}

reday = {"01": 1, "02": 2, "03": 3, "04": 4, "05": 5, "06": 6,
          "07": 7, "08": 8, "09": 9}

# Функция для проверки значения на NaN
def is_not_nan(value):
    return not (isinstance(value, float) and math.isnan(value))

# Функция для определения месяца
def month():
    today = datetime.now()
    month_name = months[today.strftime("%m")]
    return month_name

# Функция для определения дня
def day():
    today = datetime.now()
    if today.strftime("%d") in reday:
        day_name = reday[today.strftime("%d")]
    else:
        day_name = int(today.strftime("%d"))
    return day_name
