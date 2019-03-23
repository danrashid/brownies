import json


def item(item):
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
