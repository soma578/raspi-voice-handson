# practice_2_visualize.py
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import argparse
import soundfile as sf

# --- 説明 ---
# このスクリプトは、録音した音声または指定されたWAVファイルの波形をグラフで表示します。
# コマンドラインから -f (または --file) オプションでWAVファイルを指定できます。
# 例: python practice_2_visualize.py -f my_voice.wav
# 引数なしで実行すると、5秒間の録音を行います。
# 詳細は -h オプションで確認してください。
# ----------

# コマンドライン引数の設定
parser = argparse.ArgumentParser(description="Visualize audio from recording or a WAV file.")
parser.add_argument("-f", "--file", type=str, help="Path to the WAV file to visualize.")
args = parser.parse_args()

FS = 44100
DURATION = 5

if args.file:
    # WAVファイルを読み込む
    try:
        myrecording, FS = sf.read(args.file, dtype='float32')
        DURATION = len(myrecording) / FS
        print(f"WAVファイル '{args.file}' を読み込みました。")
    except FileNotFoundError:
        print(f"エラー: ファイル '{args.file}' が見つかりません。")
        exit()
    except Exception as e:
        print(f"エラー: ファイル '{args.file}' を読み込めません。 - {e}")
        exit()
else:
    print(f"{DURATION}秒間録音します...")
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
