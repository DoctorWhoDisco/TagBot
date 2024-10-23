import os
import botdata
import telebot
import openpyxl
import pandas as pd

botdata.time_set()

bot = telebot.TeleBot('5448636353:AAHOQzJrin4uvYmhKSFUwUIFd73YDtmEV6E')

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@bot.message_handler(content_types=['document'])
def handle_docs(message):
    try:
        # Получаем информацию о файле
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        # Создаем путь для сохранения файла
        file_path = os.path.join(UPLOAD_DIR, message.document.file_name)
        # Сохраняем файл
        with open(file_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        # Проверяем, является ли файл Excel
        if message.document.mime_type in ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
                                          'application/vnd.ms-excel']:
            # Чтение Excel-файла с помощью pandas
            df = pd.read_excel(file_path)
            # Выводим первые несколько строк из Excel файла
            content = df.head().to_string()
            # Отправляем содержимое пользователю
            bot.reply_to(message, f"Первые строки файла:\n{content}")
        else:
            bot.reply_to(message, "Пожалуйста, загрузите файл Excel.")
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")

@bot.message_handler(commands=['all'])
def all(message):
    try:
        text = ''
        with open('allmem.txt', 'r') as f:
            while True:
                line = f.readline()
                if not line:
                    break
                tag = line.split("\n")[0]
                text += f'{tag}, '
            #print(message)
        bot.send_message(message.chat.id, f'{text[:-2]}')
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")

print ('В работе')
bot.infinity_polling()






# import telebot
#
# bot = telebot.TeleBot('7437491590:AAGKhPXa5LqECvlZUSHD3I6M3yDUY_Hj2Kg')
#
# @bot.message_handler(commands=['all'])
# def all(message):
#     with open('allmem.txt', 'r') as f:
#         while True:
#             line = f.readline()
#             if not line:
#                 break
#             part = line.split(":")
#             name = part[0]
#             link = part[1].strip()
#             # id = line.split()[2]
#             text = text + f'[{name}]({link}\u200B), '
#         #print(message)
#     bot.send_message(message.chat.id, f'{text[:-2]}', parse_mode='MarkdownV2')
#
# bot.infinity_polling()
#
# text = ''
# with open('allmem.txt', 'r') as f:
#     while True:
#         line = f.readline()
#         if not line:
#             break
#         tag = line.split("\n")[0]
#         text += f'{tag}, '
# print (text[:-2])

