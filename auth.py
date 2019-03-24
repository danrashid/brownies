from requests import HTTPError, Request, Session, post
from requests.auth import HTTPBasicAuth
import logging

import config


def refresh_token():
    logging.info('Refreshing access token')

    r = post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'refresh_token', 'refresh_token': config.refresh
    }, auth=HTTPBasicAuth(config.client, config.secret))

    r.raise_for_status()

    config.token = r.json()['access_token']


def request(method, url, json=None, retries=0):
    s = Session()

    req = Request(method, url, json=json)
    prepped = req.prepare()
    prepped.headers['Authorization'] = 'Bearer %s' % config.token

    resp = s.send(prepped)

    try:
        resp.raise_for_status()
        return resp
    except HTTPError:
        if (resp.status_code == 401 and retries == 0):
            refresh_token()
            request(method, url, json=json, retries=retries + 1)
        else:
            raise
