import pyaudio
import pitch_detection

# Sets up PyAudio to start recording
p = pyaudio.PyAudio()
BUFFER_SIZE = 1024
SAMPLE_RATE = 44100
stream = p.open(format=pyaudio.paFloat32, channels=1, rate=SAMPLE_RATE, input=True, frames_per_buffer=BUFFER_SIZE)

all_frequencies = []
pitch_object = pitch_detection.setup(BUFFER_SIZE, SAMPLE_RATE)

while True:
    frequency = pitch_detection.get_frequency(pitch_object, stream, BUFFER_SIZE)

    if frequency is not None:
        all_frequencies.append(frequency)
        average_pitch = round(sum(all_frequencies) / len(all_frequencies), 2)
        print('\r' + str(average_pitch), end='')
