import atexit
import parse
from os import makedirs
import argparse
import process
from atexit import register
from shutil import rmtree
import logging
import encode
import refresh


def main():

    parser = argparse.ArgumentParser(description='Make some brownies')

    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('-p', '--playlist', required=True,
                               help='set playlist ID')
    requiredNamed.add_argument('-d', '--dir', required=True,
                               help='set directory for MP3s')
    requiredNamed.add_argument(
        '-t', '--token', help='set access token. ignored if using -c, -s, and -r')

    parser.add_argument('-c', '--client',
                        help='set client id')
    parser.add_argument('-s', '--secret',
                        help='set client secret')
    parser.add_argument('-r', '--refresh',
                        help='set refresh token')

    parser.add_argument('-m', '--market', default='US',
                        help='set market (default: US)')
    parser.add_argument('-l', '--log', default='INFO',
                        help='set logging level (default: INFO)')

    args = vars(parser.parse_args())
    temp_dir = '%s/tmp' % args['dir']
    makedirs(temp_dir, exist_ok=True)

    logging.basicConfig(level=args['log'].upper())

    client_id = args['client']
    client_secret = args['secret']
    refresh_token = args['refresh']

    auth = 'Basic %s' % (encode.base64('%s:%s' % (
        client_id, client_secret))) if client_id and client_secret else None

    token = refresh.token(
        refresh_token, auth) if refresh_token and auth else args['token']

    def exit_handler():
        rmtree(temp_dir)

    register(exit_handler)

    process.playlist(playlist_id=args['playlist'], dir=args['dir'], token=token,
                     market=args['market'], refresh_token=args['refresh'], auth=auth)


if __name__ == '__main__':
    main()
