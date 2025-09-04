# practice_2_visualize.py
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt

FS = 44100
DURATION = 5

print("5秒間録音します...")
myrecording = sd.rec(int(DURATION * FS), samplerate=FS, channels=1)
sd.wait()
print("録音終了。")

# 時間軸を作成
time = np.arange(0, DURATION, 1/FS)

# グラフを描画
plt.figure(figsize=(12, 4))
plt.plot(time, myrecording)
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.title("Waveform")
plt.grid()
plt.show()
