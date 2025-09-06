# practice_6_stt.py
import sounddevice as sd
import numpy as np
from vosk import Model, KaldiRecognizer
import json
import os
import argparse
import soundfile as sf

# --- 説明 ---
# このスクリプトは、録音した音声または指定されたWAVファイルを日本語テキストに変換します。
# コマンドラインから -f (または --file) オプションでWAVファイルを指定できます。
# 例: python practice_6_stt.py -f my_voice.wav
# 引数なしで実行すると、5秒間の録音を行います。
# 注意: 音声認識モデル(models/vosk/ja-0.22)が必要です。
# 詳細は -h オプションで確認してください。
# ----------

MODEL_DIR = "models/vosk/ja-0.22"
FS = 16000  # 日本語モデルは16000Hzを推奨
DURATION = 5

# コマンドライン引数の設定
parser = argparse.ArgumentParser(description="Perform speech-to-text from recording or a WAV file.")
parser.add_argument("-f", "--file", type=str, help="Path to the WAV file for STT.")
args = parser.parse_args()

if not os.path.exists(MODEL_DIR):
    print("Voskモデルが見つかりません。")
    exit()

if args.file:
    try:
        myrecording, FS = sf.read(args.file, dtype='float32')
        print(f"WAVファイル '{args.file}' を読み込みました。サンプリングレート: {FS} Hz")
    except FileNotFoundError:
        print(f"エラー: ファイル '{args.file}' が見つかりません。")
        exit()
    except Exception as e:
        print(f"エラー: ファイル '{args.file}' を読み込めません。 - {e}")
        exit()
else:
    print(f"{DURATION}秒間、話してください... (サンプリングレート: {FS} Hz)")
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
