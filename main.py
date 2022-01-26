import telebot
from utills import CheckInput, UserError
from config import TOKEN
from data import data_now, weak_weather_fc, d_currency



bot = telebot.TeleBot(TOKEN)


class Start:
    @staticmethod
    def now():
        @bot.message_handler(commands=["start", "help"])
        def info(message: telebot.types.Message):
            bot.reply_to(message, "для конвертации валюты введите данные в следующем формате\n \
<валюта 'из'> <валюта 'в'> <кол-во>) \
\n/currencies - список допустимых валют\
\n/weather_now - погода в г. Москва сейчас\
\n/weather_weak - погода в г. Москва на неделю")



        @bot.message_handler(commands=['currencies'])
        def currencies(message: telebot.types.Message):
            txt = "список допустимых валют:\n"
            for k in d_currency:
                txt += f"{k}\n"
            bot.reply_to(message, txt)

        @bot.message_handler(commands=['weather_now'])
        def weather_now(message: telebot.types.Message):
            bot.reply_to(message, data_now)

        @bot.message_handler(commands=['weather_weak'])
        def weather_weak(message: telebot.types.Message):
            bot.send_message(message.chat.id, weak_weather_fc)


        @bot.message_handler(content_types=['text'])
        def convert(message: telebot.types.Message):
            try:
                words = message.text.lower().split()
                txt = CheckInput.get_price(words)

            except UserError as e:
                bot.reply_to(message, f"UserError: {e}")
            except Exception as e:
                bot.reply_to(message, f"системный сбой: {e}")
            else:
                bot.send_message(message.chat.id, txt)






        bot.polling(none_stop=True)


if __name__ == "__main__":
    Start.now()


# @bot.message_handler()
# def echo(message):
#     bot.send_message(message.chat.id, "привет")



