import pyaudio
import numpy as np
from aubio import pitch


p = pyaudio.PyAudio()
BUFFER_SIZE = 1024
SAMPLE_RATE = 44100
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=SAMPLE_RATE, input=True, frames_per_buffer=BUFFER_SIZE)

HOP_SIZE = 4096
pitch_o = pitch("yin", HOP_SIZE, BUFFER_SIZE, SAMPLE_RATE)
pitch_o.set_unit("Hz")
pitch_o.set_tolerance(.8)

all_pitches = []

while True:
    data = stream.read(BUFFER_SIZE)
    sample = np.frombuffer(data, dtype=np.float32)

    confidence = pitch_o.get_confidence()
    pitch = pitch_o(sample)[0]

    if confidence > 0.85 and (150 < pitch < 700):
        all_pitches.append(pitch)
        avg_pitch = round(sum(all_pitches) / len(all_pitches), 2)
        print('\r'+str(avg_pitch), end='')
