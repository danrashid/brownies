import atexit
import parse
from os import makedirs
import argparse
import process
from atexit import register
from shutil import rmtree

parser = argparse.ArgumentParser(description='Make some brownies')
parser.add_argument('-i', '--id', required=True,
                    help='Playlist ID')
parser.add_argument('-d', '--dir', required=True,
                    help='Directory where MP3s should be stored')
parser.add_argument('-t', '--token', required=True,
                    help='OAuth token')
parser.add_argument('-m', '--market', default='US',
                    help='Market (default: US)')

args = vars(parser.parse_args())
temp_dir = '%s/tmp' % args['dir']
makedirs(temp_dir, exist_ok=True)


def exit_handler():
    rmtree(temp_dir)


register(exit_handler)

process.playlist(args['dir'], args['id'], args['token'], args['market'])
