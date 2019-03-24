from urllib.request import urlretrieve

from auth import request
import config


def fetch_cover(url):
    filename = '%s/tmp/cover.jpg' % config.dir
    urlretrieve(url, filename)
    return filename


def play(uri, retries=0):
    request('PUT', 'https://api.spotify.com/v1/me/player/play', json={
        'uris': [uri]
    })


def parse(item):
    track = item['track']
    album = track['album']

    return {
        'artist': album['artists'][0]['name'],
        'album': album['name'],
        'cover': album['images'][0]['url'],
        'duration_ms': track['duration_ms'],
        'id': track['id'],
        'title': track['name'],
        'uri': track['uri']
    }
