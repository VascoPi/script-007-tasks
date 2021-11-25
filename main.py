#!/usr/bin/env python3
from server import FileService
import argparse
import logging
import os

PARENT_DIR = 'data'

def main():
    logging.debug('Start server')
    os.chdir(os.path.join(os.getcwd(), PARENT_DIR))
    aparser = argparse.ArgumentParser()
    aparser.add_argument("-d", required=False, type=str, default=os.getcwd(), help="Change work directory")

    args = aparser.parse_args()

    if args.d:
        FileService.change_dir(path=args.d)

    logging.debug('Stop server')


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    main()
