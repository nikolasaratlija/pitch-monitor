import pyaudio
import numpy as np
from aubio import pitch

# Sets up PyAudio to start recording
p = pyaudio.PyAudio()
BUFFER_SIZE = 1024
SAMPLE_RATE = 44100
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=SAMPLE_RATE, input=True, frames_per_buffer=BUFFER_SIZE)

# Sets up Aubio.pitch function which calculates the pitch from an audio stream
HOP_SIZE = 4096
pitch_o = pitch("yin", HOP_SIZE, BUFFER_SIZE, SAMPLE_RATE)
pitch_o.set_unit("Hz")
pitch_o.set_tolerance(.8)

all_pitches = []

while True:
    # Gets raw audio data
    data = stream.read(BUFFER_SIZE)
    sample = np.frombuffer(data, dtype=np.float32)

    # Gets the pitch and pitch confidence from the raw audio data
    pitch = pitch_o(sample)[0]
    confidence = pitch_o.get_confidence()

    if confidence > 0.85 and (150 < pitch < 700):
        # Pitches get appended to a list to then calculate the average pitch
        all_pitches.append(pitch)
        average_pitch = round(sum(all_pitches) / len(all_pitches), 2)
        print('\r' + str(average_pitch), end='')
