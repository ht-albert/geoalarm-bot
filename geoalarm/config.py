import yaml
import os

from utils import SingletonDecorator


DB_URL = 'sqlite:////{}'.format(os.path.dirname(os.path.abspath(__file__)))


@SingletonDecorator
class Config:
    config_file = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        'config.yaml'
    )

    def __init__(self, *args, **kwargs):

        with open(self.config_file, 'r') as c:
            config = yaml.load(c)

        self.bot_token = self.get_from_env_or_config(config, 'bot_token')
        self.port = self.get_from_env_or_config(config, 'port', 5000)
        self.host = self.get_from_env_or_config(config, 'host')
        self.proxy = self.get_from_env_or_config(config, 'proxy')
        self.db_url = os.path.join(
            DB_URL,
            self.get_from_env_or_config(config, 'db_name')
        )
        self.is_local = True if self.host == 'localhost' else False

    @staticmethod
    def get_from_env_or_config(config, param, default=None):
        return os.environ.get(param.upper()) or config.get(param, default)
