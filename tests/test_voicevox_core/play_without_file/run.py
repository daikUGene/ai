import voicevox_core
from voicevox_core import AccelerationMode, AudioQuery, VoicevoxCore

from pydub import AudioSegment
from pydub.playback import play
import time


class VoicevoxCoreSynthesizer:
    def __init__(self):
        acceleration_mode = "AUTO"
        open_jtalk_dict_dir = "./open_jtalk_dic_utf_8-1.11"
        self.speaker_id = 0

        self.core = VoicevoxCore(
            acceleration_mode=acceleration_mode, open_jtalk_dict_dir=open_jtalk_dict_dir
        )
        self.core.load_model(self.speaker_id)      


    def speak(self, text):
        start_time = time.time()

        audio_query = self.core.audio_query(text, self.speaker_id)
        sample_rate = audio_query.output_sampling_rate

        wav = self.core.synthesis(audio_query, self.speaker_id)

        audio = AudioSegment(
            data = wav,
            sample_width=2, # 2byte (16bit)
            frame_rate=sample_rate,
            channels=1  # voicevox_coreのデフォルト出力はモノラル
        )

        print("processing time: ", time.time() - start_time)

        play(audio)


if __name__ == "__main__":
    synthesizer = VoicevoxCoreSynthesizer()
    synthesizer.speak("お誕生日おめでとうございます。今年で何歳ですか？")
