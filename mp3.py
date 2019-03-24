from glob import glob

import config


def write(segment, filename, artist, title, album, cover):
    segment.export(filename,
                   format='mp3',
                   bitrate='320k',
                   tags={'album': album,
                         'artist': artist,
                         'title': title},
                   cover=cover)


def file_exists(id):
    return len(glob('%s/*%s*.mp3' % (config.dir, id))) > 0
