from pydub import AudioSegment
import capture
import fetch
import write
from glob import glob
import logging


def playlist(playlist_id, dir, token, refresh_token, auth):

    tracks = fetch.tracks(playlist_id=playlist_id, token=token,
                          refresh_token=refresh_token, auth=auth)

    for track in tracks:

        id = track['id']
        artist = track['artist']
        title = track['title']
        artist_title_id = ('%s - %s - %s' % (artist, title, id)
                           ).replace('/', '_').replace('|', '_')
        filename = '%s/%s.mp3' % (dir, artist_title_id)

        if (len(glob('%s/*%s*.mp3' % (dir, id))) > 0):
            logging.debug('Already processed: %s' % artist_title_id)
        else:
            logging.info('Processing: %s' % artist_title_id)
            cover = fetch.cover(dir, track['cover'])

            try:
                wav = capture.stream(
                    dir=dir, uri=track['uri'], duration_ms=track['duration_ms'], token=token, refresh_token=refresh_token, auth=auth)
                segment = AudioSegment.from_wav(wav)

                write.mp3(segment=segment, filename=filename, artist=artist,
                          title=title, album=track['album'], cover=cover)
            except RuntimeError as e:
                logging.warning('Skipping %s: %s' % (artist_title_id, e))
