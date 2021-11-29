import logging
import logging.config


def setup_logger(level='NOTSET', filename=None):
    logging.basicConfig(level=logging.DEBUG)
    logging.debug(f'Set log level to {level}')
    config = {
        'version': 1,
        'formatters': {
            'default': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            },
            'to_file': {
                'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'stream': 'ext://sys.stdout',
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
                'class': 'logging.handlers.RotatingFileHandler',
                'formatter': 'to_file',
                'filename': filename,
                'maxBytes': 500,
                'backupCount': 3,
        }

        config['root']['handlers'].append('file')

    logging.config.dictConfig(config)
