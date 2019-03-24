from pydub import AudioSegment
import logging

import mp3
from auth import request
import config
from track import fetch_cover, parse
from wav import capture


def _fetch_tracks():
    tracks = []

    def fetch(url):
        r = request('GET', url)
        json = r.json()
        parsed_tracks = map(parse, json['items'])
        tracks.extend(parsed_tracks)

        next = json['next']
        if (next):
            fetch(next)

    fetch('https://api.spotify.com/v1/playlists/%s/tracks' % config.playlist)

    logging.info('Found %d tracks in playlist' % len(tracks))

    return tracks


def process():

    tracks = _fetch_tracks()

    for track in tracks:

        id = track['id']
        artist = track['artist']
        title = track['title']
        artist_title_id = ('%s - %s - %s' % (artist, title, id)
                           ).replace('/', '_').replace('|', '_')
        filename = '%s/%s.mp3' % (config.dir, artist_title_id)

        if (mp3.file_exists(id)):
            logging.debug('Already processed: %s' % artist_title_id)

        else:
            logging.info('Processing: %s' % artist_title_id)
            cover = fetch_cover(track['cover'])

            try:
                wav = capture(
                    uri=track['uri'], duration_ms=track['duration_ms'])
                segment = AudioSegment.from_wav(wav)

                mp3.write(segment=segment, filename=filename, artist=artist,
                          title=title, album=track['album'], cover=cover)

            except RuntimeError as e:
                logging.warning('Skipping %s: %s' % (artist_title_id, e))
