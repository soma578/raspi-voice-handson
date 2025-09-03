# 2_vosk_recognition.py
from vosk import Model, KaldiRecognizer
import sys
import wave
import json

# 事前に録音した "rec.wav" を開く
# ターミナルで以下のコマンドを実行して録音できます
# arecord -D plughw:1,0 -f S16_LE -r 16000 rec.wav
# ※ -D plughw:1,0 の数字は環境によって変わります。arecord -lで確認してください。
try:
    wf = wave.open("rec.wav", "rb")
except FileNotFoundError:
    print("エラー: rec.wav ファイルが見つかりません。")
    print("arecordコマンドでマイクから音声を録音してください。")
    sys.exit(1)


# 日本語モデルを読み込む (事前にモデルのダウンロードが必要)
# https://alphacephei.com/vosk/models から "vosk-model-ja-0.22" をダウンロード・解凍
try:
    model = Model("vosk-model-ja-0.22")
except Exception as e:
    print(f"エラー: Voskモデルの読み込みに失敗しました。 {e}")
    print("モデルが正しく配置されているか確認してください。")
    sys.exit(1)

rec = KaldiRecognizer(model, wf.getframerate())
rec.SetWords(True) # 単語単位での認識結果も取得する設定

# ファイル全体を読み込んで認識
while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    rec.AcceptWaveform(data)

# 最終的な認識結果をJSON形式で表示
result = json.loads(rec.FinalResult())
print("--- JSON形式の認識結果 ---")
print(result)

# テキストだけを取り出して表示
print("
--- 認識されたテキスト ---")
print(result.get('text', 'テキストが認識できませんでした。'))
