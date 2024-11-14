import os
from utils import add_file, employ_list, on_line, group_update, start
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

bot = telebot.TeleBot('6261116025:AAFmRm6NX0BFCdulSncXzjq0jbY3RS-zqbc')

bot.remove_webhook()

start()
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Внесение нового файла
@bot.message_handler(content_types=['document'])
def handle_docs(message):
    try:
        # Получаем информацию о файле
        # Создаем путь для сохранения файла
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_path = os.path.join(UPLOAD_DIR, message.document.file_name)
        with open('cache.txt', 'w') as file:
            file.write(file_path)
        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        # Проверяем, является ли файл Excel
        if message.document.mime_type in ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                                          'application/vnd.ms-excel']:
            add_file(file_path)
            group_update()
            bot.reply_to(message, "Ш Б \nмнк\n")
        else:
            bot.reply_to(message, "Пожалуйста, загрузите файл Excel.")
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")

# Команда на тег вообще на всех
@bot.message_handler(commands=['вообще_все', 'general', 'путукфд'])
def newall(message):
    try:
        text = ''
        for emp in employ_list:
            if emp.tag != 'Уволенный сотрудник':
                text += f'{emp.tag}, '
        print (f'{text[:-2]}')
        bot.send_message(message.chat.id, f'{text[:-2]}')
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")

# Команда на тег тех кто на смене
@bot.message_handler(commands=['на_смене', 'онлайн', 'on_shift', 'online', 'all', 'фдд'])
def online(message):
    try:
        text = ''
        for on_name in on_line:
            for emp in employ_list:
                if on_name == emp.name:
                    text += f'{emp.tag}, '
                    break
        print (f'{text[:-2]}')
        bot.send_message(message.chat.id, f'{text[:-2]}')
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")

# Команда на справку (пользовательская)
@bot.message_handler(commands=['help', 'помощь'])
def newhelp(message):
    try:
        text = (f'Справка: \n/all - тег сотрудников находящихся на смене в данный момент\n/general - тег всех '
                f'сотрудников 1 линии\n\n')
        bot.reply_to(message, f'{text}')
    except Exception as e:
             bot.reply_to(message, f"Произошла ошибка: {e}")

# Открытие админ панели
@bot.message_handler(content_types=["text"])
def handle_text_message(message):
    try:
        if "админ панель: ff234" in message.text.lower():
            text = (f'Справка: \n/all - тег сотрудников находящихся на смене в данный момент\n/general - тег всех '
                    f'сотрудников 1 линии\n\n'
                    f'Если необходимо внести обновленное расписание сотрудников просьба приложить файл в excel.\n'
                    f'Более точное описание нюансов заполнения данного файла '
                    f'(в т.ч. пример документа) по кнопке ниже.')
            markup = InlineKeyboardMarkup()
            tablebutton = InlineKeyboardButton("Подробнее о таблице", callback_data="tablebutton_pressed")
            markup.add(tablebutton)
            bot.reply_to(message, f'{text}', reply_markup=markup)
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")

# Обработчик кнопки для доп инфы по таблице
@bot.callback_query_handler(func=lambda call: call.data == "tablebutton_pressed")
def handle_button_press(call):
    try:
        text = (f'Для корректного считывания данных ботом необходимо:\n'
                f'1. Таблица с расписанием месяцев должна быть разделена с последующей пустой строкой.\n'
                f'2. Файл обязательно должен содержать в себе лист "Сотрудники" с данными всех актуальных сотрудников.\n'
                f'(сотрудники отсутствующие в данном листе не будут учитываться)\n'
                f'3. Не забывайте, что тадлица обязательно должна содержать столбец для последнего дня предыдущего '
                f'месяца. Он считается частью разметки страницы.\n')
        # Отправка файла пользователю
        file_path = os.path.join(os.getcwd(), 'uploads/correct_file.xlsx')
        with open(file_path, 'rb') as file:
            bot.send_document(call.message.chat.id, file, caption=text)
    except Exception as e:
        bot.reply_to(call.message, f"Произошла ошибка: {e}")

bot.infinity_polling()


