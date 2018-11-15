import time
from app import app, db
from bot import bot
from config import Config

config = Config()

if __name__ == '__main__':
    if config.is_local:
        db.create_all()
        bot.polling()
    else:
        bot.set_webhook(url=config.host + config.bot_token)
        time.sleep(0.1)
        app.run(host='0.0.0.0', port=config.port, debug=True)
