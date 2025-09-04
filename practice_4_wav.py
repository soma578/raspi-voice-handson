# practice_4_wav.py
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write, read

FS = 44100
DURATION = 5
FILENAME = "my_voice.wav"

# 録音してWAVファイルに保存
print(f"録音開始... ({FILENAME}に保存)")
recording = sd.rec(int(DURATION * FS), samplerate=FS, channels=1)
sd.wait()
write(FILENAME, FS, recording)
print("保存完了。")

# WAVファイルを読み込んで再生
print(f"{FILENAME}を読み込んで再生します...")
samplerate, data = read(FILENAME)
print(f"読み込んだファイルの周波数: {samplerate} Hz")
sd.play(data, samplerate)
sd.wait()
print("再生完了。")
