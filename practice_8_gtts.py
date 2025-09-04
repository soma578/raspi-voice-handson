# practice_8_gtts.py
from gtts import gTTS
import pygame.mixer as m
import os

mytext = "こんにちは。こちらは、グーグルのオンライン音声合成サービスです。インターネット経由で音声を生成しています。"
FILENAME = "gtts_hello.mp3"

print("gTTSで音声ファイルを生成します...")
try:
    tts = gTTS(text=mytext, lang='ja')
    tts.save(FILENAME)
    print(f"{FILENAME} を保存しました。")
except Exception as e:
    print(f"エラー: 音声の生成に失敗しました。インターネット接続を確認してください。 {e}")
    exit()

print("PyGameで再生します...")
m.init()
m.music.load(FILENAME)
m.music.play()
while m.music.get_busy():
    continue
m.music.stop()
print("再生完了。")
