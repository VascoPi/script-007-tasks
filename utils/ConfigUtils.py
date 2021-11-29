import argparse
import logging
import os
import configparser
from utils.Utils import singleton

DEFAULT_CONFIG = "config.ini"
APP_NAME = "FILE_SERVER"
logging.getLogger(APP_NAME)


@singleton
class Config:
    data = {}
    params_keys = {'dir': str,
                   'log_level': str,
                   'log_file': str,
                   'port': int
                   }

    def __init__(self):
        self.set_data()

    def _read_args(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('-d', '--dir', default='data', type=str,
                            help="working directory (default: 'data')")
        parser.add_argument('-l', '--log_level', default='warning', choices=['debug', 'info', 'warning', 'error'],
                            help='Log level to console (default is warning)')
        parser.add_argument('--log_file', type=str, help='Log file.')
        params = parser.parse_args()

        for key in self.params_keys:
            value = getattr(params, key, None)
            if value:
                self[key] = value

    def _read_env(self):
        for param in self.params_keys:
            if os.environ.get(param, None):
                self[param] = os.environ[f"{APP_NAME}_{param.upper()}"]

    def _read_ini(self):
        parser = configparser.ConfigParser()
        parser.read(DEFAULT_CONFIG)

        for section in parser.sections():
            for key, value in parser[section].items():
                self[key] = value

    def set_data(self):
        self._read_ini()
        self._read_env()
        self._read_args()
        logging.debug(f"Set params {self.data}")

    def __setitem__(self, key, value):
        self.data[key] = self.params_keys.get(key, str)(value)

    def __getitem__(self, item):
        return self.data[item]


config_data = Config()
