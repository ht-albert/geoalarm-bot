import yaml
import os

from utils import Singleton


class Config(Singleton):
    config_file = './config.yaml'

    def __init__(self, *args, **kwargs):

        with open(Config.config_file, 'r') as c:
            config = yaml.load(c)

        self.bot_token = self.get_from_env_or_config(config, 'bot_token')
        self.port = self.get_from_env_or_config(config, 'port', 5000)
        self.host = self.get_from_env_or_config(config, 'host')
        self.proxy = self.get_from_env_or_config(config, 'proxy')
        self.is_local = True if self.host == 'localhost' else False

    @staticmethod
    def get_from_env_or_config(config, param, default=None):
        return os.environ.get(param.upper()) or config.get(param, default)
