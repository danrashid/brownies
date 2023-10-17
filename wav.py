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
    filename = "%s/tmp/stream.wav" % config.dir
    portaudio = pyaudio.PyAudio()

    stream = portaudio.open(
        format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK
    )

    def kill():
        stream.stop_stream()
        stream.close()
        portaudio.terminate()

    frames = []

    sleep(PADDING_SECONDS)
    track.play(uri)
    for _i in range(0, ceil(RATE / CHUNK * (duration_ms / 1000 + PADDING_SECONDS))):
        data = stream.read(CHUNK)
        frames.append(data)
        if _i == CHUNK and reduce(_max, frames, 0) == 0:
            kill()
            raise RuntimeError("Only silence was received after %s frames" % CHUNK)

    kill()

    waveform = wave.open(filename, "wb")
    waveform.setnchannels(CHANNELS)
    waveform.setsampwidth(portaudio.get_sample_size(FORMAT))
    waveform.setframerate(RATE)
    waveform.writeframes(b"".join(frames))
    waveform.close()

    return filename
