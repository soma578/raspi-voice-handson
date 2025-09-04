# practice_5_tts.py
import pyopenjtalk
import sounddevice as sd

text = "こんにちは。こちらは、オープンソースの日本語音声合成エンジン、オープンＪトークです。"

print(f"音声合成中...: 「{text}」")
audio_data, FS = pyopenjtalk.tts(text)

print(f"再生します... (周波数: {FS} Hz)")
sd.play(audio_data, FS)
sd.wait()
print("再生完了。")
