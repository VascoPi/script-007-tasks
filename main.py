#!/usr/bin/env python3
from utils.LoggingUtils import setup_logger
import logging
import logging.config
import sys

from aiohttp import web

from server.WebHandler import WebHandler
from utils.ConfigUtils import config


def setup_logger(level='NOTSET', filename=None):
    logger_conf = {
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
        logger_conf['handlers']['file'] = {
            'class': 'logging.FileHandler',
            'encoding': 'UTF-8',
            'formatter': 'default',
            'filename': filename,
        }
        logger_conf['root']['handlers'].append('file')
    logging.config.dictConfig(logger_conf)


def main():
    setup_logger(level=logging.getLevelName(config['log_level'].upper()), filename=config['log_file'])
    logging.debug('started')
    logging.debug('config %s', config)

    handler = WebHandler()
    app = web.Application()
    app.add_routes([
        web.get('/', handler.handle),
        web.post('/create_file', handler.create_file),
        web.post('/change_dir', handler.change_dir),
        web.get('/get_files', handler.get_files),
        web.get('/get_file_data', handler.get_file_data),
        web.delete('/delete_file', handler.delete_file),
    ])

    web.run_app(app, host=config['host'], port=config['port'])


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        sys.exit('\nERROR: Interrupted by user')
    except BaseException as err:
        print(f'ERROR: Something goes wrong:\n{err}')
        sys.exit(1)
