from whispercpp import Whisper
import time

w = Whisper.from_pretrained("small")
print("モデル読込完了")

start_time = time.time()
result = w.transcribe_from_file("./test_16khz.wav")
print("認識結果：", result)
print("処理時間：", time.time() - start_time)
