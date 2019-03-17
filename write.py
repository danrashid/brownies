def mp3(segment, filename, artist, title, album, cover):
    segment.export(filename,
                   format='mp3',
                   bitrate='320k',
                   tags={'album': album,
                         'artist': artist,
                         'title': title},
                   cover=cover)
