# from utils import group_update
from utils.botdata import is_not_nan, month
import pandas as pd

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
    print(f'{employ_list} \nData loaded')