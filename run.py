import atexit
import parse
from os import makedirs
import argparse
import process
from atexit import register
from shutil import rmtree
import logging


def main():

    parser = argparse.ArgumentParser(description='Make some brownies')

    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('-i', '--id', required=True,
                               help='playlist ID')
    requiredNamed.add_argument('-d', '--dir', required=True,
                               help='directory for MP3s')
    requiredNamed.add_argument('-t', '--token', required=True,
                               help='OAuth token')

    parser.add_argument('-m', '--market', default='US',
                        help='market (default: US)')
    parser.add_argument('-l', '--log', default='INFO',
                        help='logging level (default: INFO)')

    args = vars(parser.parse_args())
    temp_dir = '%s/tmp' % args['dir']
    makedirs(temp_dir, exist_ok=True)
    logging.basicConfig(level=args['log'].upper())

    def exit_handler():
        rmtree(temp_dir)

    register(exit_handler)

    process.playlist(args['dir'], args['id'], args['token'], args['market'])


if __name__ == '__main__':
    main()
