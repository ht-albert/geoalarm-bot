import time
from flask import Flask, request, render_template
import telebot
from config import Config

config = Config()

# if bot started localhost then use proxy
if config.is_local:
    telebot.apihelper.proxy = {
        'https': config.proxy
    }

app = Flask(__name__)
bot = telebot.TeleBot(config.bot_token)


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
    __send_location(mess.chat.id, mess.location.latitude,
                    mess.location.longitude)


@bot.edited_message_handler(content_types=['location'])
def location_upd(mess):
    __send_location(mess.chat.id, mess.location.latitude,
                    mess.location.longitude)


@bot.message_handler(commands=['start'])
def hello_bot(mess):
    bot.send_message(mess.chat.id,
                     "Укажите адрес на карте {}".format(config.host+str(mess.chat.id)))

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
