from pydub import AudioSegment
import capture
import fetch
import write
from os import path


def playlist(out_dir, id, token, market):
    tracks = fetch.tracks(id, token, market)

    for track in tracks:

        artist = track['artist']
        title = track['title']
        filename = '%s/%s - %s.mp3' % (out_dir, artist, title)

        if (path.isfile(filename) == False):

            print('Processing %s - %s' % (artist, title))
            cover = fetch.cover(out_dir, track['cover'])
            wav = capture.stream(
                out_dir, track['uri'], track['duration_ms'], token)
            segment = AudioSegment.from_wav(wav)

            write.mp3(segment, filename, artist, title, track['album'], cover)
