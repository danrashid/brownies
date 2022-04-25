#!/usr/bin/env python3

import os
from pydub import AudioSegment
import argparse
import eyed3
from mp3 import write


def main():

    parser = argparse.ArgumentParser(description='Normalize a directory')

    requiredNamed = parser.add_argument_group('required named arguments')
    requiredNamed.add_argument('-d', '--dir', required=True,
                               help='set directory of files')
    requiredNamed.add_argument('-g', '--gain', required=True,
                               help='set gain')

    args = vars(parser.parse_args())
    gain = float(args['gain'])

    for root, _dirs, files in os.walk(args['dir']):
        for file in files:
            filename = root + file
            print('Normalizing %s...' % filename)
            segment = AudioSegment.from_file(filename)
            segment = segment.apply_gain(gain - segment.max_dBFS)
            cover = "/tmp/cover.jpg"
            id3 = eyed3.load(filename)
            with open(cover, "wb") as f:
                f.write(id3.tag.images[0].data)
            write(segment=segment, filename=filename, artist=id3.tag.artist,
                  title=id3.tag.title, album=id3.tag.album, cover=cover, id=id3.tag.comments[0].text)


if __name__ == '__main__':
    main()
