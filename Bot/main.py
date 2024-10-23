import telebot

bot = telebot.TeleBot('5448636353:AAHOQzJrin4uvYmhKSFUwUIFd73YDtmEV6E')
print ('В работе')

@bot.message_handler(commands=['фдд', 'all', 'fdd'])
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

bot.infinity_polling()


