import telebot

from geoalarm.config import Config
from geoalarm.bot.constant import HELLO_MESSAGE
from geoalarm.models import Users
import geopy.distance

config = Config()

temporary_storage = {}

bot = telebot.TeleBot(config.bot_token)

if config.is_local:
    telebot.apihelper.proxy = {'https': config.proxy}


@bot.message_handler(content_types=['location'])
def location(mess):
    lat, lon = mess.location.latitude, mess.location.longitude
    if not all([lat, lon]):
        bot.send_message(mess.shat.id, "Что-то не так, не могу понять твои координаты")

    user = Users.query.filter_by(chat_id=mess.chat.id).first()
    if user.status != Users.WAIT_LOCATION:
        return

    temporary_storage[user.chat_id] = {'lat': lat, 'lon': lon}
    keyboard = telebot.types.InlineKeyboardMarkup()
    row = []
    for key, val in {'no': 'Отмена', 'yes': "Поехали"}.items():
        row.append(telebot.types.InlineKeyboardButton(text=val, callback_data=key))
    keyboard.add(*row)
    bot.send_message(chat_id=mess.chat.id, text="Если место указал верно жми поехали и поехали!", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in ['no', 'yes'])
def processing(call):
    user = Users.query.filter_by(chat_id=call.from_user.id).first()
    if call.data == 'yes':
        point = temporary_storage.pop(user.chat_id)
        user.set_point(point.get('lat'), point.get('lon'))
        user.set_status(Users.WAIT_LIVE)
        bot.delete_message(user.chat_id, call.message.message_id)
        bot.send_location(user.chat_id, latitude=user.lat, longitude=user.lon, live_period=8*60*60)
        bot.send_message(user.chat_id, "Я поделился постоянной гео-локацией, тебе нужно сделать "
                                       "тоже самое чтобы я знал когда тебя предупредить")
    else:
        bot.edit_message_text("Давай попробуем еще раз", call.from_user.id, call.message.message_id)


@bot.edited_message_handler(content_types=['location'])
def location_upd(mess):
    lat, lon = mess.location.latitude, mess.location.longitude
    if not all([lat, lon]):
        bot.send_message(mess.shat.id, "Что-то не так, не могу понять твои координаты")
    user = Users.query.filter_by(chat_id=mess.chat.id).first()

    if user.status == Users.WAIT_LIVE:
        user.set_status(Users.TRACING)

    if user.status != Users.TRACING:
        return

    if geopy.distance.vincenty((lat, lon), (user.lat, user.lon)).m < 500:
        bot.send_message(chat_id=user.chat_id, text="Ну все мы подъезжаем, не проспи! Удачи тебе!")
        user.set_status(Users.WAIT_LOCATION)


@bot.message_handler(commands=['start'])
def hello_bot(mess):
    try:
        user = Users().get_or_create(tg_user=mess.from_user)
    except AttributeError:
        bot.send_message(mess.chat.id, "Ошибка активации бота")
    user.set_status(Users.WAIT_LOCATION)
    bot.send_message(user.chat_id, HELLO_MESSAGE.format(user.first_name))
    bot.send_message(user.chat_id, "Задай место у которого тебя будить")
