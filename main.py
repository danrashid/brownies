#!/usr/bin/env python3

from os import getenv, makedirs
from atexit import register
from dotenv import load_dotenv
from shutil import rmtree
import argparse
import logging

from auth import refresh_token, request
import playlist
import config


def main():
    load_dotenv()
    config.client = getenv("CLIENT")
    config.secret = getenv("SECRET")

    parser = argparse.ArgumentParser(description="Make some brownies")

    parser.add_argument("-p", "--playlist", help="playlist ID (default: Liked Songs)")
    parser.add_argument(
        "-l", "--log", default="INFO", help="logging level (default: INFO)"
    )
    parser.add_argument("refresh", help="refresh token")
    parser.add_argument("dir", help="where to store the MP3s")

    args = vars(parser.parse_args(namespace=config))

    temp_dir = "%s/tmp" % args["dir"]
    makedirs(temp_dir, exist_ok=True)

    logging.basicConfig(level=args["log"].upper())

    def exit_handler():
        rmtree(temp_dir)
        request("PUT", "https://api.spotify.com/v1/me/player/pause")

    register(exit_handler)

    refresh_token()
    playlist.process()


if __name__ == "__main__":
    main()
