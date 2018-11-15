import telebot
from config import Config
from bot.handlers import *


config = Config()

# if bot started localhost then use proxy
if config.is_local:
    telebot.apihelper.proxy = {
        'https': config.proxy
    }

bot = telebot.TeleBot(config.bot_token)
