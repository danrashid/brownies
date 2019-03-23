from urllib.request import urlretrieve
from requests import get, HTTPError
import parse
import logging
import refresh


def cover(dir, url):
    filename = '%s/tmp/cover.jpg' % dir
    urlretrieve(url, filename)
    return filename


def tracks(playlist_id, token, market, refresh_token, auth):
    tracks = []

    def by_market(item):
        try:
            item['track']['available_markets'].index(market)
            return True
        except:
            track = parse.item(item)
            logging.warn('Unavailable in %s market: %s - %s - %s' % (
                market, track['artist'], track['title'], track['id']
            ))
            return False

    def fetch(url, token=token, retries=0):
        r = get(url, headers={
            'Authorization': 'Bearer %s' % token
        })

        try:
            r.raise_for_status()

            json = r.json()

            available_items = filter(by_market, json['items'])
            parsed_tracks = map(parse.item, available_items)
            tracks.extend(parsed_tracks)

            next = json['next']
            if (next):
                fetch(next, token)
        except HTTPError:
            if (r.status_code == 401 and retries == 0):
                token = refresh.token(refresh_token, auth)
                fetch(url, token, retries + 1)
            else:
                raise

    fetch('https://api.spotify.com/v1/playlists/%s/tracks' % playlist_id)

    return tracks
