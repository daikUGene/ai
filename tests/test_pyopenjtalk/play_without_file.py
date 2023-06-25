import pyopenjtalk
import numpy as np
from pydub import AudioSegment
from pydub.playback import play

x, sr = pyopenjtalk.tts("おめでとうございます")
sound = AudioSegment(
    data = x.astype(np.int16).tobytes(),
    sample_width = 2,
    frame_rate = sr,
    channels = 1
)
play(sound)
