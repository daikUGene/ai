from faster_whisper import WhisperModel
import time

model_size = "small"

model = WhisperModel(model_size, device="cpu", compute_type="int8")

start_time = time.time()

segments, info = model.transcribe("audio.mp3", beam_size=5, language="ja", vad_filter=True, without_timestamps=True)

for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))

print("processing time: ", time.time() - start_time)
