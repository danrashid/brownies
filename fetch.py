from urllib.request import urlretrieve
from requests import get
import parse
import logging


def cover(out_dir, url):
    filename = '%s/tmp/cover.jpg' % (out_dir)
    urlretrieve(url, filename)
    return filename


def tracks(playlist_id, token, market):
    tracks = []

    def by_market(item):
        try:
            item['track']['available_markets'].index(market)
            return True
        except:
            track = parse.item(item)
            logging.warn('Unavailable in %s market: %s - %s' % (
                market, track['artist'], track['title']
            ))
            return False

    def fetch(url):
        r = get(url, headers={
            'Authorization': 'Bearer %s' % token
        })

        r.raise_for_status()
        json = r.json()

        available_items = filter(by_market, json['items'])
        parsed_tracks = map(parse.item, available_items)
        tracks.extend(parsed_tracks)

        next = json['next']
        if (next):
            fetch(next)

    fetch('https://api.spotify.com/v1/playlists/%s/tracks' % playlist_id)

    return tracks
