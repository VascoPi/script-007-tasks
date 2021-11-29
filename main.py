#!/usr/bin/env python3
import argparse
import logging
import logging.config
import sys
from utils.ConfigUtils import config_data

import server.FileService as FileService


def setup_logger(level='NOTSET', filename=None):
    config = {
        'version': 1,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'level': level,
            },
        },
        'root': {
            'level': 'DEBUG',
            'handlers': ['console'],
        }
    }
    if filename:
        config['handlers']['file'] = {
            'class': 'logging.FileHandler',
            'encoding': 'UTF-8',
            'formatter': 'default',
            'filename': filename,
        }
        config['root']['handlers'].append('file')
    logging.config.dictConfig(config)


def main():

    setup_logger(level=logging.getLevelName(config_data['log_level'].upper()), filename=config_data['log_file'])
    logging.debug('started')
    FileService.change_dir(config_data['dir'])


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit('\nERROR: Interrupted by user')
    except BaseException as err:
        print(f'ERROR: Something goes wrong:\n{err}')
        sys.exit(1)
