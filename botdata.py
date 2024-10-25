from datetime import datetime
import math
# import openpyxl
import pandas as pd
# from gi.overrides.keysyms import value

months = {"01": "Январь", "02": "Февраль", "03": "Март", "04": "Апрель", "05": "Май", "06": "Июнь",
          "07": "Июль", "08": "Август", "09": "Сентябрь", "10": "Октябрь", "11": "Ноябрь", "12": "Декабрь"}

# создание класса для объекта сотрудник 1 линии
# class FirstLine:
#     def __init__(self, name, active):
#         self.name = name
#         self.active = active
#         # self.title = title
#     def show(self):
#         return f"Name: {self.name} /// Active days: {self.active}"
#
# First_Line = set()
employ_dict = {}

# ща тут будет функция обработки данных
def add_file(path):
    # Чтение данных из таблицы
    df = pd.read_excel(path, sheet_name=month())
    # Преобразование в лист листов (Ура! мы научились читать то что надо)
    rows_as_list = df.values.tolist()[2:]
    end_list = []
    for row in rows_as_list:
        if pd.isna(row[0]):
            break
        end_list.append(row)
    for row in end_list:
        # name = row[0]
        active_dict = {}
        i = 0
        for elem in row[5:]:
            i += 1
            if is_not_nan(elem):
                active_dict.update({i: elem})
        employ_dict.update({row[0]: active_dict})
    print(employ_dict)

# Функция для проверки значения на NaN
def is_not_nan(value):
    return not (isinstance(value, float) and math.isnan(value))

# это функция для определения месяца
def month():
    today = datetime.now()
    month_name = months[today.strftime("%m")]
    return month_name

# это функция для определения дня
def day():
    today = datetime.now()
    day_name = today.strftime("%d")
    return day_name
