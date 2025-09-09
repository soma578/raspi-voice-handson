# practice_2b_spectrogram.py
import wave
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import spectrogram
import sys
import argparse

# --- 説明 ---
# このスクリプトは、指定されたWAVファイルのスペクトログラム（周波数分析）を表示します。
# コマンドラインから -f (または --file) オプションでWAVファイルを指定できます。
# 例: python practice_2b_spectrogram.py -f my_voice.wav
# 引数なしで実行すると、デフォルトで "my_voice.wav" を読み込みます。
# 詳細は -h オプションで確認してください。
# ----------

# コマンドライン引数の設定
parser = argparse.ArgumentParser(description="Generate and display a spectrogram from a WAV file.")
parser.add_argument("-f", "--file", type=str, default="my_voice.wav", help="Path to the WAV file to analyze. Defaults to my_voice.wav.")
args = parser.parse_args()

FILENAME = args.file

print(f"{FILENAME} のスペクトログラムを描画します。")

try:
    wr = wave.open(FILENAME, "r")
except FileNotFoundError:
    print(f"エラー: {FILENAME} が見つかりません。")
    if FILENAME == "my_voice.wav":
        print("先に practice_4_wav.py を実行して、解析するWAVファイルを作成してください。")
    sys.exit()

# WAVファイルからデータを読み込み
n_channels = wr.getnchannels()
sample_rate = wr.getframerate()
n_frames = wr.getnframes()
data = wr.readframes(n_frames)
wr.close()

# NumPy配列に変換
x = np.frombuffer(data, dtype=np.int16)
if n_channels > 1: # ステレオの場合は片チャンネルに
    x = x[::n_channels]

# スペクトログラムを計算
f, t, Sxx = spectrogram(x, fs=sample_rate)

# プロット
plt.figure(figsize=(12, 5))
plt.pcolormesh(t, f, 10 * np.log10(Sxx + 1e-9), shading='gouraud') # 1e-9を足してlog(0)エラーを回避
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.title(f'Spectrogram of {FILENAME}')
plt.ylim(0, 8000) # 8kHzまで表示
plt.colorbar(label='Intensity [dB]')

# グラフをファイルに保存
output_filename = "spectrogram.png"
plt.savefig(output_filename)
print(f"スペクトログラムを {output_filename} として保存しました。")
# plt.show() # GUI環境がない場合はこちらをコメントアウト
