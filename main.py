import telebot
from config import keys, TOKEN
from classes import MSGException, Convertor


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands = ['start','help'])
def instructions(message:telebot.types.Message):
    text = "Чтобы начать работу введите запрос на конвертацию валют в форме: '<Исходная валюта>, <Желаемая валюта>, <Сумма исходной валюты>'"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands = ['values',])
def value(message:telebot.types.Message):
    text = "Доступные валюты: "
    for key in keys.keys():
        text = "\n".join((text,key))
    bot.reply_to(message,text)

@bot.message_handler(content_types = ['text'])
def convert(message:telebot.types.Message):
    try:
        values = message.text.split(' ')
        From, To, Amount = values

        if len(values) != 3:
            raise MSGException('Необходимое количество параметров:3')
        total_value = Convertor.get_price(From, To, Amount) * int(Amount)
    except MSGException as e:
        bot.reply_to(message,f"Ошибка в вашей команде: \n{e}")
    except Exception as e:
        bot.reply_to(message,f"Ошибка сервера: \n{e}")
    else:
        text = f"Стоимость {Amount} {From} в {To} - {total_value}"
        bot.send_message(message.chat.id, text)

bot.polling(True)


