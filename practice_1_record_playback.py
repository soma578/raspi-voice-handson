# practice_1_record_playback.py
import sounddevice as sd
import numpy as np

# デバイス一覧を表示して確認
# print(sd.query_devices())

# パラメータ設定
FS = 44100  # サンプリング周波数
DURATION = 5  # 録音時間 (秒)

print(f"{DURATION}秒間、録音します...")

# 録音
myrecording = sd.rec(int(DURATION * FS), samplerate=FS, channels=1)
sd.wait()  # 録音終了まで待機

print("録音終了。")
print(f"データ型: {myrecording.dtype}, 形状: {myrecording.shape}")

# 再生
print("再生します...")
sd.play(myrecording, FS)
sd.wait()  # 再生終了まで待機

print("再生完了。")
