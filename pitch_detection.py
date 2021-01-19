import numpy as np
from aubio import pitch


def setup(buffer_size, sample_rate):
    """ Sets up the pitch detection object """
    pitch_object = pitch("yin", 4096, buffer_size, sample_rate)
    pitch_object.set_unit("Hz")
    pitch_object.set_tolerance(.8)
    return pitch_object


def get_frequency(pitch_object, audio_sample, buffer_size):
    """ Returns the pitch in hertz of an audio sample """

    # Gets raw audio data
    data = audio_sample.read(buffer_size)
    sample = np.frombuffer(data, dtype=np.float32)

    # Gets the frequencies and pitch confidence from the raw audio data
    frequency = round(pitch_object(sample)[0], 2)
    confidence = pitch_object.get_confidence()

    if confidence > 0.85 and (150 < frequency < 700):
        return frequency
