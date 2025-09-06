# practice_6_stt.py
import sounddevice as sd
import numpy as np
from vosk import Model, KaldiRecognizer
import json
import os

MODEL_DIR = "models/vosk/ja-0.22"
FS = 16000  # 日本語モデルは16000Hzを推奨
DURATION = 5

if not os.path.exists(MODEL_DIR):
    print("Voskモデルが見つかりません。")
    exit()

print(f"{DURATION}秒間、話してください...")
myrecording = sd.rec(int(DURATION * FS), samplerate=FS, channels=1, dtype='float32')
sd.wait()
print("認識中...")

model = Model(MODEL_DIR)
recognizer = KaldiRecognizer(model, FS)

# データ形式を変換して認識
data = (myrecording * 32767).astype(np.int16).tobytes()
recognizer.AcceptWaveform(data)

result = json.loads(recognizer.FinalResult())
print("--- 認識結果 ---")
print(result['text'])
