# practice_3_effects.py
import sounddevice as sd
import numpy as np

FS = 44100
DURATION = 3

print(f"{DURATION}秒間録音します...")
myrecording = sd.rec(int(DURATION * FS), samplerate=FS, channels=1)
sd.wait()
print("録音終了。")

# 1. 音量UP
print("音量を2倍にして再生")
sd.play(myrecording * 2, FS); sd.wait()

# 2. 逆再生
print("逆再生")
sd.play(myrecording[::-1], FS); sd.wait()

# 3. 結合
print("1秒の無音を挟んで2回再生")
one_sec_silence = np.zeros((FS * 1, 1), dtype=myrecording.dtype)
combined_audio = np.concatenate([myrecording, one_sec_silence, myrecording])
sd.play(combined_audio, FS); sd.wait()
