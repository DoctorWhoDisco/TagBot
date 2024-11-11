import os
import botdata
import telebot

bot = telebot.TeleBot('5448636353:AAHOQzJrin4uvYmhKSFUwUIFd73YDtmEV6E')

today = [botdata.month(), botdata.day()]
print (today)
botdata.start()
print ('Данные из кэша получены')
print ('В работе')

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

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
            botdata.add_file(file_path)
        else:
            bot.reply_to(message, "Пожалуйста, загрузите файл Excel.")
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")

@bot.message_handler(commands=['вообще_все', 'general', 'путукфд'])
def all(message):
    try:
        text = ''
        for emp in botdata.employ_list:
            if emp.tag != 'Уволенный сотрудник':
                text += f'{emp.tag}, '
        print (f'{text[:-2]}')
        bot.send_message(message.chat.id, f'{text[:-2]}')
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")

@bot.message_handler(commands=['на_смене', 'онлайн', 'on_shift', 'online', 'all', 'фдд'])
def online(message):
    try:
        text = ''
        for on_name in botdata.on_line:
            for emp in botdata.employ_list:
                if on_name == emp.name:
                    text += f'{emp.tag}, '
                    break
        print (f'{text[:-2]}')
        bot.send_message(message.chat.id, f'{text[:-2]}')
    except Exception as e:
        bot.reply_to(message, f"Произошла ошибка: {e}")

bot.infinity_polling()


