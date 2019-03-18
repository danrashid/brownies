from requests import put, HTTPError
import refresh


def track(uri, token, refresh_token, auth, retries=0):
    r = put('https://api.spotify.com/v1/me/player/play',
            json={
                'uris': [uri]
            },
            headers={
                'Authorization': 'Bearer %s' % token
            })

    try:
        r.raise_for_status()
    except HTTPError:
        if (r.status_code == 401 and retries == 0):
            token = refresh.token(refresh_token, auth)
            track(uri, token, refresh_token, auth, 1)
        else:
            raise
