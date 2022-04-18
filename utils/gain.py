#!/usr/bin/env python3

import os
from math import floor
from pydub import AudioSegment
import argparse

def main():

    parser = argparse.ArgumentParser(description='Find the lowest gain in a directory')

    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('-d', '--dir', required=True,
                               help='read directory of files')

    args = vars(parser.parse_args())

    for root, _dirs, files in os.walk(args['dir']):
        gain = 0.0
        track = ''
        progress = -1

        for i, file in enumerate(files):
            segment = AudioSegment.from_file(root + file)

            if segment.max_dBFS < gain:
                gain = segment.max_dBFS
                track = file

            _progress = floor(((int(i) + 1) / len(files)) * 100)
            if (_progress % 10 == 0 and _progress > progress):
                progress = _progress
                print('%d%%' % progress, end='..', flush=True)      

        print('\nLowest gain is %f dB set by %s' % (gain, track))

if __name__ == '__main__':
    main()
