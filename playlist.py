from pydub import AudioSegment
import logging

import mp3
from auth import request
import config
from track import fetch_cover, parse
from wav import capture


def _fetch_tracks():
    tracks = []

    def fetch(url):
        r = request("GET", url)
        json = r.json()
        parsed_tracks = map(parse, json["items"])
        tracks.extend(parsed_tracks)

        next = json["next"]
        if next:
            fetch(next)

    if config.playlist:
        fetch(
            "https://api.spotify.com/v1/playlists/%s/tracks?limit=100" % config.playlist
        )
    else:
        fetch("https://api.spotify.com/v1/me/tracks?limit=50")

    logging.info("Found %d tracks" % len(tracks))

    return tracks


def process():
    tracks = _fetch_tracks()

    existing_ids = mp3.existing_ids()

    for track in tracks:
        id = track["id"]
        artist = track["artist"]
        title = track["title"].split(" - ")[:1][0]
        artist_title = ("%s - %s" % (artist, title)).replace("/", "_").replace("|", "_")

        if id in existing_ids:
            logging.debug("Already processed: %s" % artist_title)

        else:
            logging.info("Processing: %s" % artist_title)
            cover = fetch_cover(track["cover"])

            try:
                wav = capture(uri=track["uri"], duration_ms=track["duration_ms"])
                segment = AudioSegment.from_wav(wav)

                filename = "%s/%s.mp3" % (config.dir, artist_title)
                mp3.write(
                    segment=segment,
                    filename=filename,
                    artist=artist,
                    title=title,
                    album=track["album"],
                    cover=cover,
                    id=id,
                )

            except RuntimeError as e:
                logging.warning("Skipping %s: %s" % (artist_title, e))
