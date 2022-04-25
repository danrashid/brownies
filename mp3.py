from glob import glob
import eyed3

import config


def write(segment, filename, artist, title, album, cover, id):
    segment.export(filename,
                   format='mp3',
                   bitrate='320k',
                   tags={'artist': artist,
                         'title': title,
                         'album': album, },
                   cover=cover)

    id3 = eyed3.load(filename)
    id3.tag.comments.set(id)
    id3.tag.save()


def existing_ids():
    return list(map(lambda filename: eyed3.load(filename).tag.comments[0].text, glob("%s/*.mp3" % config.dir)))
