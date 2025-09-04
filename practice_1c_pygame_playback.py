# practice_1c_pygame_playback.py
import pygame.mixer as m
import pygame.time
import sys
import os

FILENAME = "converted_audio.mp3" # practice_7_converter.pyで作成したMP3ファイル

print(f"{FILENAME} をPyGameで再生します。")

if not os.path.exists(FILENAME):
    print(f"エラー: {FILENAME} が見つかりません。")
    print("先に practice_7_converter.py を実行して、再生するMP3ファイルを作成してください。")
    sys.exit()

try:
    m.init()
    m.music.load(FILENAME)
except m.error as e:
    print(f"エラー: ファイルの読み込みに失敗しました。 {e}")
    sys.exit()

m.music.play()
while m.music.get_busy():
    pygame.time.delay(100)
m.music.stop()
print(f"{FILENAME} の再生が完了しました。")
