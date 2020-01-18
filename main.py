#!/usr/bin/env python3

from os import makedirs
from atexit import register
from shutil import rmtree
import argparse
import logging

from auth import refresh_token, request
import playlist
import config


def main():

    parser = argparse.ArgumentParser(description='Make some brownies')

    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('-p', '--playlist', required=True,
                               help='set playlist ID')
    requiredNamed.add_argument('-d', '--dir', required=True,
                               help='set directory for MP3s')

    requiredNamed.add_argument('-c', '--client',
                               help='set client id')
    requiredNamed.add_argument('-s', '--secret',
                               help='set client secret')
    requiredNamed.add_argument('-r', '--refresh',
                               help='set refresh token')

    parser.add_argument('-l', '--log', default='INFO',
                        help='set logging level (default: INFO)')

    args = vars(parser.parse_args(namespace=config))

    temp_dir = '%s/tmp' % args['dir']
    makedirs(temp_dir, exist_ok=True)

    logging.basicConfig(level=args['log'].upper())

    def exit_handler():
        rmtree(temp_dir)
        request('PUT', 'https://api.spotify.com/v1/me/player/pause')

    register(exit_handler)

    refresh_token()
    playlist.process()


if __name__ == '__main__':
    main()
