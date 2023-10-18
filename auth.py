from requests import HTTPError, Request, Session, post
from requests.auth import HTTPBasicAuth
import logging

import config


def refresh_token():
    logging.info("Refreshing access token")

    response = post(
        "https://accounts.spotify.com/api/token",
        data={"grant_type": "refresh_token", "refresh_token": config.refresh},
        auth=HTTPBasicAuth(config.client, config.secret),
    )

    try:
        response.raise_for_status()
        json = response.json()
        config.token = json["access_token"]
        if json["refresh_token"]:
            config.refresh = json["refresh_token"]
    except HTTPError:
        logging.error(response.text)
        raise


def request(method, url, json=None, retries=0):
    session = Session()

    req = Request(method, url, json=json)
    prepped = req.prepare()
    prepped.headers["Authorization"] = "Bearer %s" % config.token

    response = session.send(prepped)

    try:
        response.raise_for_status()
        return response
    except HTTPError:
        if response.status_code == 401 and retries == 0:
            refresh_token()
            request(method, url, json=json, retries=retries + 1)
        else:
            logging.error(response.text)
            raise
