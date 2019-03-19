from pydub import AudioSegment
import capture
import fetch
import write
from os import path
import logging


def playlist(playlist_id, dir, token, market, refresh_token, auth):

    tracks = fetch.tracks(playlist_id=playlist_id, token=token,
                          market=market, refresh_token=refresh_token, auth=auth)

    for track in tracks:

        artist = track['artist']
        title = track['title']
        artist_title = ('%s - %s' % (artist, title)
                        ).replace('/', '_').replace('|', '_')
        filename = '%s/%s.mp3' % (dir, artist_title)

        if (path.isfile(filename)):
            logging.debug('Already processed: %s' % artist_title)
        else:
            logging.info('Processing: %s' % artist_title)
            cover = fetch.cover(dir, track['cover'])
            wav = capture.stream(
                dir=dir, uri=track['uri'], duration_ms=track['duration_ms'], token=token, refresh_token=refresh_token, auth=auth)
            segment = AudioSegment.from_wav(wav)

            write.mp3(segment=segment, filename=filename, artist=artist,
                      title=title, album=track['album'], cover=cover)
