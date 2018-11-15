from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate
from data import DB_URL
import telebot
from bot import bot


config = Config()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = config.db_url
db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.route('/' + config.bot_token, methods=['POST'])
def webhook():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update, {}])
    return ''
