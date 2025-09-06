# practice_1_record_playback.py
import sounddevice as sd
import numpy as np
import argparse
import soundfile as sf

# --- 説明 ---
# このスクリプトは、音声を録音して再生するか、指定されたWAVファイルを再生します。
# コマンドラインから -f (または --file) オプションでWAVファイルを指定できます。
# 例: python practice_1_record_playback.py -f my_voice.wav
# 引数なしで実行すると、5秒間の録音を行います。
# 詳細は -h オプションで確認してください。
# ----------

# コマンドライン引数の設定
parser = argparse.ArgumentParser(description="Record audio or play a WAV file.")
parser.add_argument("-f", "--file", type=str, help="Path to the WAV file to play.")
args = parser.parse_args()

# パラメータ設定
FS = 44100  # サンプリング周波数
DURATION = 5  # 録音時間 (秒)

if args.file:
    # WAVファイルを読み込む
    try:
        myrecording, FS = sf.read(args.file, dtype='float32')
        print(f"WAVファイル '{args.file}' を読み込みました。")
    except FileNotFoundError:
        print(f"エラー: ファイル '{args.file}' が見つかりません。")
        exit()
    except Exception as e:
        print(f"エラー: ファイル '{args.file}' を読み込めません。 - {e}")
        exit()
else:
    # デバイス一覧を表示して確認
    # print(sd.query_devices())

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
