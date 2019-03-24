# http://people.csail.mit.edu/hubert/pyaudio/

import pyaudio
from math import ceil
from time import sleep
from functools import reduce

import config
import wave
import track

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
PADDING_SECONDS = 1


def _max(a, bytes):
    return max(a, max(bytes))


def capture(uri, duration_ms):
    filename = '%s/tmp/stream.wav' % config.dir
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    def kill():
        stream.stop_stream()
        stream.close()
        p.terminate()

    frames = []

    sleep(PADDING_SECONDS)
    track.play(uri)
    for _i in range(0, ceil(RATE / CHUNK * (duration_ms / 1000 + PADDING_SECONDS))):
        data = stream.read(CHUNK)
        frames.append(data)
        if (_i == CHUNK and reduce(_max, frames, 0) == 0):
            kill()
            raise RuntimeError(
                'Only silence was received after %s frames' % CHUNK)

    kill()

    wf = wave.open(filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    return filename
