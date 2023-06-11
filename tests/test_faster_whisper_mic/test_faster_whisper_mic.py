import io
from pydub import AudioSegment
import speech_recognition as sr
from faster_whisper import WhisperModel
import queue
import tempfile
import os
import threading
import numpy as np


class SpeechRecognizer:
    def __init__(
        self,
        model_size_or_path,
        result_queue,
        device="auto",
        english=False,
        verbose=False,
        energy=300,
        dynamic_energy=False,
        pause=0.8,
        save_file=False
    ):
        self.audio_model = WhisperModel(model_size_or_path=model_size_or_path, device=device, compute_type="int8")
        self.english = english
        self.verbose = verbose
        self.energy = energy
        self.dynamic_energy = dynamic_energy
        self.pause = pause
        self.save_file = save_file
        self.temp_dir = tempfile.mkdtemp() if save_file else None

        self.result_queue = result_queue
        self.audio_queue = queue.Queue()


    def start(self):
        threading.Thread(target=self.record_audio).start()
        threading.Thread(target=self.transcribe_forever).start()


    def record_audio(self):
        #load the speech recognizer and set the initial energy threshold and pause threshold
        r = sr.Recognizer()
        r.energy_threshold = self.energy
        r.pause_threshold = self.pause
        r.dynamic_energy_threshold = self.dynamic_energy

        with sr.Microphone(sample_rate=16000) as source:
            print("Say something!")
            i = 0
            while True:
                #get and save audio to wav file
                audio = r.listen(source)
                if self.save_file:
                    data = io.BytesIO(audio.get_wav_data())
                    audio_clip = AudioSegment.from_file(data)
                    filename = os.path.join(self.temp_dir, f"temp{i}.wav")
                    audio_clip.export(filename, format="wav")
                    audio_data = filename
                else:
                    audio_data = np.frombuffer(audio.get_raw_data(), np.int16).flatten().astype(np.float32) / 32768.0

                self.audio_queue.put_nowait(audio_data)
                i += 1


    def transcribe_forever(self):
        while True:
            audio_data = self.audio_queue.get()
            if self.english:
                segments, info = self.audio_model.transcribe(audio_data, without_timestamps=True, language='en')
                result = list(segments)[0]
            else:
                segments, info = self.audio_model.transcribe(audio_data, without_timestamps=True, language='ja')
                result = list(segments)[0]

            if not self.verbose:
                predicted_text = result.text
                self.result_queue.put_nowait(predicted_text)
            else:
                self.result_queue.put_nowait(result)

            if self.save_file:
                os.remove(audio_data)


if __name__ == "__main__":
    result_queue = queue.Queue()
    recognizer = SpeechRecognizer(model_size_or_path="small", result_queue=result_queue)
    recognizer.start()

    while True:
        print("You said: ", result_queue.get())
