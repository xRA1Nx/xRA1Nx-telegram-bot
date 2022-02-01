import telebot
from utills import CheckInput, UserError
from config import TOKEN
from data import data_now, weak_weather_fc, d_currency, d_massages

bot = telebot.TeleBot(TOKEN)


class Start:
    weather = False
    exchange = False

    def __init__(self):
        self.weather = False
        self.exchange = False

    @classmethod
    def clear(cls):
        cls.weather = False
        cls.exchange = False

    @classmethod
    def now(cls):
        @bot.message_handler(commands=["start", "help"])
        def info(message: telebot.types.Message):
            bot.reply_to(message, d_massages["start"])

        @bot.message_handler(commands=['back'])
        def back_to_start_menu(message: telebot.types.Message):
            Start.clear()
            bot.send_message(message.chat.id, d_massages["start"])

        @bot.message_handler(commands=["exchange"])
        def exchange(message: telebot.types.Message):
            bot.send_message(message.chat.id, "\n".join([d_massages["exchange"], d_massages["back"]]))
            Start.clear()
            cls.exchange = True

        @bot.message_handler(commands=['currencies'])
        def currencies(message: telebot.types.Message):
            if cls.exchange:
                txt = "список допустимых валют:\n"
                for k in d_currency:
                    txt += f"{k}\n"
                bot.reply_to(message, "\n".join([txt, d_massages['back']]))
                Start.clear()
                cls.exchange = True

        @bot.message_handler(commands=['weather'])
        def weather(message: telebot.types.Message):
            bot.reply_to(message, "\n".join([d_massages["weather_intro"], d_massages["back"]]))
            Start.clear()
            cls.weather = True

        @bot.message_handler(content_types=['text'])
        def text_operations(message: telebot.types.Message):
            if cls.weather:
                if message.text.lower() not in ["сегодня", "неделя"]:
                    bot.reply_to(message, f'данные введены не верно\n{d_massages["weather_intro"]}\
\n{d_massages["back"]}')
                else:
                    if message.text.lower() == "сегодня":
                        bot.send_message(message.chat.id, data_now)
                    elif message.text.lower() == "неделя":
                        bot.send_message(message.chat.id, weak_weather_fc)
                    cls.weather = False
                    bot.send_message(message.chat.id, d_massages["start"])

            if cls.exchange:
                try:
                    words = message.text.lower().split()
                    txt = CheckInput.get_price(words)
                except UserError as e:
                    bot.reply_to(message, f"UserError: {e}")
                except Exception as e:
                    bot.reply_to(message, f"системный сбой: {e}")
                else:
                    bot.send_message(message.chat.id, txt)
                    cls.exchange = False
                    bot.send_message(message.chat.id, d_massages["start"])

        bot.polling(none_stop=True)


if __name__ == "__main__":
    Start.now()
