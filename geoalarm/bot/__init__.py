import telebot

from geoalarm.config import Config
from geoalarm.bot.constant import HELLO_MESSAGE, WAIT_LOCATION
from geoalarm.models import User


config = Config()

bot = telebot.TeleBot(config.bot_token)

if config.is_local:
    telebot.apihelper.proxy = {'https': config.proxy}


@bot.message_handler(content_types=['location'])
def location(mess):

    lat, lon = mess.location.latitude, mess.location.longitude
    if not all([lat, lon]):
        bot.send_message(mess.shat.id, "Invalid lat, lon")

    keyboard = telebot.types.InlineKeyboardMarkup()
    row = []
    for key, val in {'no': 'Нет', 'yes': "Да"}.items():
        row.append(telebot.types.InlineKeyboardButton(text=val,
                                                      callback_data=key))
    keyboard.add(*row)

    bot.send_location(chat_id=mess.chat.id, latitude=lat,
                      longitude=lon, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in ['no', 'yes'])
def processing(call):
    user = {}
    if call.data == 'yes':

        bot.edit_message_text("Поделись  геолокацие в режиме реального времени", call.from_user.id,
                              call.message.message_id, reply_markup=None)
        bot.answer_callback_query(call.id, text="")
    else:
        bot.edit_message_text("Задай место у которого тебя будить", call.from_user.id,
                              call.message.message_id, reply_markup=None)
        bot.answer_callback_query(call.id, text="")


@bot.edited_message_handler(content_types=['location'])
def location_upd(mess):
    pass


@bot.message_handler(commands=['start'])
def hello_bot(mess):
    User().get_or_create(tg_user=mess.from_user)
    bot.send_message(mess.chat.id, HELLO_MESSAGE.format(mess.from_user.first_name))
    bot.send_message(mess.chat.id, "Задай место у которого тебя будить")
