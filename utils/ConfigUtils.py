import argparse
import logging
import os
import configparser


DEFAULT_CONFIG = "config.ini"


def singleton(cls):
    instances = {}

    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return getinstance


@singleton
class Config:
    data = {}
    params_keys = ['dir', 'log_level', 'log_file', 'port']

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
                self.data[key] = value

    def _read_env(self):
        for param in self.params_keys:
            if os.environ.get(param, None):
                self.data[param] = os.environ[param]

    def _read_ini(self):
        parser = configparser.ConfigParser()
        parser.read(DEFAULT_CONFIG)

        for section in parser.sections():
            for k, v in parser[section].items():
                self.data[k] = v

    def set_data(self):
        self._read_ini()
        self._read_env()
        self._read_args()
        print(f"Set params {self.data}")


config_data = Config()
