# 4_text_to_speech.py
import pyopenjtalk
import sounddevice as sd

# --- ここに音声認識処理などを組み合わせる ---
# 例として、認識したテキストや固定の返答を `text` 変数に入れる
# text = "音声認識に成功しました"
text = "営業部の売上が一番です"
# ------------------------------------

# テキストから音声波形を生成
# tts: Text To Speech
print(f"音声合成中: 「{text}」")
x, sr = pyopenjtalk.tts(text)

# 音声を再生
print("再生します...")
sd.play(x, sr)

# 再生が終わるまで待つ
sd.wait()

print("再生が完了しました。")
