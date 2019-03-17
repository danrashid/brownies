from requests import put


def track(uri, token):
    r = put('https://api.spotify.com/v1/me/player/play',
            json={
                'uris': [uri]
            },
            headers={
                'Authorization': 'Bearer %s' % token
            })

    r.raise_for_status()
