import telebot
from utills import CheckInput
from utills import UserError
from config import d_currency, TOKEN
from data import data_now, weak_weather_fc

bot = telebot.TeleBot(TOKEN)

words = ["неделя", "сегодня", "/weather"]


class Start:
    weather = False
    exchange = False

    def __init__(self):
        self.weather = False
        self.exchange = False

    def clear(self):
        self.__init__()

    @classmethod
    def now(cls):
        @bot.message_handler(commands=["start", "help"])
        def info(message: telebot.types.Message):
            bot.reply_to(message, "\n/exchange - конвертировать валюту\
\n/weather - погода в г. Москва")

        @bot.message_handler(commands=["exchange"])
        def exchange(message: telebot.types.Message):
            bot.send_message(message.chat.id, "для конвертации валюты введите данные в следующем формате\n \
<валюта 'из'> <валюта 'в'> <кол-во>) \
\n/currencies - список допустимых валют")
            Start.weather = False
            Start.exchange = True

        @bot.message_handler(commands=['currencies'])
        def currencies(message: telebot.types.Message):
            if Start.exchange:
                txt = "список допустимых валют:\n"
                for k in d_currency:
                    txt += f"{k}\n"
                bot.reply_to(message, txt)
                Start.weather = False
                Start.exchange = True



        @bot.message_handler(commands=['weather'])
        def weather(message: telebot.types.Message):
            bot.reply_to(message, "выберите из списка:<сегодня>, <неделя>")
            Start.exchange = False
            Start.weather = True

        @bot.message_handler(content_types=['text'])
        def weather_words(message: telebot.types.Message):
            if Start.weather:
                if message.text == "сегодня":
                    bot.send_message(message.chat.id, data_now)
                    Start.weather = False
                elif message.text == "неделя":
                    bot.send_message(message.chat.id, weak_weather_fc)
                    Start.weather = False

        @bot.message_handler(content_types=['text'])
        def convert(message: telebot.types.Message):
            possible_commands = ["/start", "/back", "/currencies"]
            if Start.exchange and message.text not in possible_commands:
                try:
                    words = message.text.lower().split()
                    txt = CheckInput.get_price(words)
                except UserError as e:
                    bot.reply_to(message, f"UserError: {e}")
                except Exception as e:
                    bot.reply_to(message, f"системный сбой: {e}")
                else:
                    bot.send_message(message.chat.id, txt)
                    Start.exchange = False

        bot.polling(none_stop=True)


if __name__ == "__main__":
    Start.now()

# @bot.message_handler()
# def echo(message):
#     bot.send_message(message.chat.id, "привет")
