from urllib.request import urlretrieve
from requests import get, HTTPError
import parse
import logging
import refresh


def cover(dir, url):
    filename = '%s/tmp/cover.jpg' % dir
    urlretrieve(url, filename)
    return filename


def tracks(playlist_id, token, refresh_token, auth):
    tracks = []

    def fetch(url, token=token, retries=0):
        r = get(url, headers={
            'Authorization': 'Bearer %s' % token
        })

        try:
            r.raise_for_status()

            json = r.json()

            parsed_tracks = map(parse.item, json['items'])
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
