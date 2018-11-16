import time

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy

from geoalarm.bot import *

from geoalarm.config import Config

config = Config()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.db_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route('/' + config.bot_token, methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return ''


def start_on_server():
    bot.set_webhook(url=config.host + config.bot_token)
    time.sleep(0.1)
    app.run(host='0.0.0.0', port=config.port, debug=True)


if __name__ == '__main__':
    from geoalarm.models import *
    db.create_all()
    bot.polling() if config.is_local else start_on_server()
