from pydub import AudioSegment
import capture
import fetch
import write
from os import path
import logging


def playlist(out_dir, id, token, market):
    tracks = fetch.tracks(id, token, market)

    for track in tracks:

        artist = track['artist']
        title = track['title']
        artist_title = '%s - %s' % (artist, title)
        filename = '%s/%s.mp3' % (out_dir, artist_title)

        if (path.isfile(filename)):
            logging.debug('Already processed: %s' % artist_title)
        else:
            logging.info('Processing: %s' % artist_title)
            cover = fetch.cover(out_dir, track['cover'])
            wav = capture.stream(
                out_dir, track['uri'], track['duration_ms'], token)
            segment = AudioSegment.from_wav(wav)

            write.mp3(segment, filename, artist, title, track['album'], cover)
