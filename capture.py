# http://people.csail.mit.edu/hubert/pyaudio/

import pyaudio
import wave
import play
from math import ceil
from time import sleep

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
PADDING_SECONDS = 1


def stream(dir, uri, duration_ms, token, refresh_token, auth):
    filename = '%s/tmp/stream.wav' % dir
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []

    sleep(PADDING_SECONDS)
    play.track(uri, token, refresh_token, auth)
    for _i in range(0, ceil(RATE / CHUNK * (duration_ms / 1000 + PADDING_SECONDS))):
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    return filename
