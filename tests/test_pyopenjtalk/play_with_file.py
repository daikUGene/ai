import pyopenjtalk
import numpy as np
from scipy.io import wavfile
from pydub import AudioSegment
from pydub.playback import play

x, sr = pyopenjtalk.tts("おめでとうございます")
wavfile.write("test.wav", sr, x.astype(np.int16))
sound = AudioSegment.from_file("test.wav", "wav")
play(sound)
