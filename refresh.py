from requests import post
import logging


def token(refresh_token, auth):
    logging.info('Refreshing access token')

    r = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'refresh_token', 'refresh_token': refresh_token
    }, headers={
        'Authorization': auth
    })

    r.raise_for_status()
    return r.json()['access_token']
