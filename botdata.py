from datetime import datetime
import math
from functools import partial
import pandas as pd
import apscheduler
from apscheduler.schedulers.background import BackgroundScheduler
# from test import online
# import time

months = {"01": "Январь", "02": "Февраль", "03": "Март", "04": "Апрель", "05": "Май", "06": "Июнь",
          "07": "Июль", "08": "Август", "09": "Сентябрь", "10": "Октябрь", "11": "Ноябрь", "12": "Декабрь"}

reday = {"01": 1, "02": 2, "03": 3, "04": 4, "05": 5, "06": 6,
          "07": 7, "08": 8, "09": 9}

on_line = []
employ_list = []

# создание класса для объекта сотрудник 1 линии
class FirstLine:
    def __init__(self, name, title, tag):
        self.name = name
        self.title = title
        self.tag = tag
        self.active = {}

    def add_active(self, active):
        self.active = active

    def get_value(self, key):
        return self.active.get(key)

    def __repr__(self):
        return (f"\nFirstLine\nИмя: {self.name}, \nДолжность: {self.title}, "
                f"\nТелега: {self.tag}, \nАктивен: {self.active}\n --------------------- ")

# Запуск при старте бота
def start():
    with open('cache.txt', 'r') as file:
        path = file.readline().strip()
    add_file(path)
    group_update()

# Апдейт классов
def group_update():
    if datetime.strptime("09:00", "%H:%M").time() < datetime.now().time() < datetime.strptime(
            "17:59", "%H:%M").time():
        morning()
    elif datetime.strptime("18:00", "%H:%M").time() < datetime.now().time() < datetime.strptime(
            "20:59", "%H:%M").time():
        evening()
    elif datetime.strptime("21:00", "%H:%M").time() < datetime.now().time() < datetime.strptime(
            "23:59", "%H:%M").time():
        night(0)
    elif datetime.strptime("00:00", "%H:%M").time() < datetime.now().time() < datetime.strptime(
            "8:59", "%H:%M").time():
        night(1)
    time_happening()

# Функция обработки данных из таблицы
def add_file(path):
    # Формирование класса, заполнение свойств name, title, tag
    df = pd.read_excel(path, sheet_name='Сотрудники')
    rows_as_list = df.values.tolist()
    for row in rows_as_list:
        if not any (emp.name == row[0] for emp in employ_list):
            name = row[0]
            title = row[2]
            if is_not_nan(row[1]):
                tag = row[1]
            else: tag = 'Уволенный сотрудник'
            obj = FirstLine(name, title, tag)
            employ_list.append(obj)
    df = pd.read_excel(path, sheet_name=month())
    # Формируем лист активных дней (Ура! мы научились читать то что надо)
    rows_as_list = df.values.tolist()[2:]
    end_list = []
    for row in rows_as_list:
        if pd.isna(row[0]):
            break
        end_list.append(row)
    for row in end_list:
        active_dict = {}
        i = 0
        for elem in row[5:]:
            i += 1
            if is_not_nan(elem) and elem != "Отпуск" and elem != "Гос. Пр.":
                active_dict.update({i: elem})
        # Свойство active заполняется подготовленными значениями
        for emp in employ_list:
            if emp.name == row[0]:
                emp.active = active_dict
    group_update()
    print(f'{employ_list} \nData loaded')

# Функция для обновления данных по времени
def time_happening():
    scheduler = BackgroundScheduler()
    scheduler.add_job(morning, 'cron', hour=9, minute=0)  # Каждый день в 09:00
    scheduler.add_job(evening, 'cron', hour=18, minute=00)
    scheduler.add_job(partial(night, 0), 'cron', hour=21, minute=00)
    scheduler.add_job(partial(night, 1), 'cron', hour=0, minute=0)
    scheduler.start()
    print ('day_update')

# Утренний апдейт
def morning():
    morning_active = []
    for emp in employ_list:
        if day() in emp.active:
            if emp.active[day()] == 'Пятид' or emp.active[day()] == 'День':
                name = emp.name
                morning_active.append(name)
    print (f'\nmorning update: {morning_active}')
    on_line.clear()
    on_line.extend(morning_active)
    return morning_active

# Вечерний апдейт
def evening():
    evening_active = []
    for emp in employ_list:
        if day() in emp.active:
            if emp.active[day()] == 'День':
                name = emp.name
                evening_active.append(name)
    print(f'\nevening update: {evening_active}' )
    on_line.clear()
    on_line.extend(evening_active)
    return evening_active

# Ночной апдейт
def night(i):
    night_active = []
    for emp in employ_list:
        if day()-i in emp.active:
            if emp.active.get(day()-i) == 'Ночь':
                name = emp.name
                night_active.append(name)
    print(f'\nnight update: {night_active}')
    on_line.clear()
    on_line.extend(night_active)
    return night_active

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
