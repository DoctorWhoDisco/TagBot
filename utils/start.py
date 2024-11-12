from utils.classcreate import add_file
from utils.classupdate import group_update
from utils.botdata import day, month

def start():
    try:
        with open('./cache.txt', 'r') as file:
            path = file.readline().strip()
        add_file(path)
        group_update()
        today = [month(), day()]
        print (today)
        print ('Данные из кэша получены')
        print ('В работе')
    except Exception as e:
        print(f"Произошла ошибка: {e}")