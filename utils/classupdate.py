from datetime import datetime
from functools import partial
from apscheduler.schedulers.background import BackgroundScheduler
from utils.classcreate import employ_list
from utils.botdata import day

on_line = []

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