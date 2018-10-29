import time
from flask import Flask, request, render_template
import telebot
from config import Config
from constant import HELLO_MESSAGE, WAIT_LOCATION, WAIT_LIVE
import collections


config = Config()

# if bot started localhost then use proxy
if config.is_local:
    telebot.apihelper.proxy = {
        'https': config.proxy
    }

app = Flask(__name__)
bot = telebot.TeleBot(config.bot_token)
data = {}
GeoUser = collections.namedtuple("GeoUser", ['geo_status', 'name', 'lat', 'lon'])


@app.route('/' + config.bot_token, methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return ''


def __send_location(chat_id, lat, lon):
    bot.send_message(chat_id, 'Location ({}, {})'.format(lat, lon))


@bot.message_handler(content_types=['location'])
def location(mess):
    user = data.get(mess.chat.id)
    if user.geo_status == WAIT_LOCATION:
        lat, lon = mess.location.latitude, mess.location.longitude
        if not all([lat, lon]):
            bot.send_message(mess.shat.id, "Invalid lat, lon")

        keyboard = telebot.types.InlineKeyboardMarkup()
        row = []
        for key, val in {'no': 'Нет', 'yes': "Да"}.items():
            row.append(telebot.types.InlineKeyboardButton(text=val,
                                                          callback_data=key))
        keyboard.add(*row)

        bot.send_location(chat_id=mess.chat.id, latitude=lat, longitude=lon, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in ['no', 'yes'])
def processing(call):
    user = data.get(call.message.chat.id)
    if call.data == 'yes':
        user.geo_status = WAIT_LIVE
        bot.edit_message_text("Поделись  геолокацие в режиме реального времени", call.from_user.id,
                            call.message.message_id, reply_markup=None)
        bot.answer_callback_query(call.id, text="")
    else:
        bot.edit_message_text("Задай место у которого тебя будить", call.from_user.id,
                              call.message.message_id, reply_markup=None)
        bot.answer_callback_query(call.id, text="")

@bot.edited_message_handler(content_types=['location'])
def location_upd(mess):
    __send_location(mess.chat.id, mess.location.latitude,
                    mess.location.longitude)


@bot.message_handler(commands=['start'])
def hello_bot(mess):
    user = GeoUser(geo_status=WAIT_LOCATION, name=mess.chat.first_name, lat=None, lon=None)
    data[mess.chat.id] = user
    bot.send_message(mess.chat.id, HELLO_MESSAGE.format(user.name))
    bot.send_message(mess.chat.id, "Задай место у которого тебя будить")


@app.route('/<int:chat_id>', methods=['GET'])
def hell(chat_id):
    return render_template('map.html')


if __name__ == '__main__':
    if config.is_local:
        bot.polling()
    else:
        bot.set_webhook(url=config.host + config.bot_token)
        time.sleep(0.1)
        app.run(host='0.0.0.0', port=config.port, debug=True)
