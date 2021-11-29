#!/usr/bin/env python3
import argparse
import os
from utils.LoggingUtils import setup_logger
import logging

import server.FileService as FileService


def main():
    """Entry point of app.

    Get and parse command line parameters and configure web app.

    Command line options:
    -d --dir  - working directory (absolute or relative path, default: current_app_folder/data).
    -h --help - help.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', default='data', type=str,
                        help="working directory (default: 'data')")
    parser.add_argument('-l', '--log_level', default='DEBUG',
                        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR', 'WARNING'],
                        help="logging level (default: 'DEBUG')")

    parser.add_argument('--log_file', default='server.log', type=str,
                        help="logging file (default: 'server.log')")

    params = parser.parse_args()

    setup_logger(level=params.log_level.upper(), filename=params.log_file)

    work_dir = params.dir if os.path.isabs(params.dir) else os.path.join(os.getcwd(), params.dir)
    FileService.change_dir(work_dir)


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.error(e)
