# practice_4_wav.py
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write, read
import argparse

# --- 説明 ---
# このスクリプトは、5秒間音声を録音し、WAVファイルとして保存します。
# コマンドラインから -o (または --output) オプションで出力ファイル名を指定できます。
# 例: python practice_4_wav.py -o new_voice.wav
# 引数なしで実行すると、デフォルトで "my_voice.wav" という名前で保存します。
# 詳細は -h オプションで確認してください。
# ----------

# コマンドライン引数の設定
parser = argparse.ArgumentParser(description="Record audio and save it to a WAV file.")
parser.add_argument("-o", "--output", type=str, default="my_voice.wav", help="Filename for the output WAV file. Defaults to my_voice.wav.")
args = parser.parse_args()

FS = 44100
DURATION = 5
FILENAME = args.output

# 録音してWAVファイルに保存
print(f"録音開始... ({FILENAME}に保存)")
recording = sd.rec(int(DURATION * FS), samplerate=FS, channels=1)
sd.wait()

# float32からint16へ変換し、互換性の高い形式で保存
print("ファイル形式を変換して保存中...")
recording_int16 = np.int16(recording * 32767)
write(FILENAME, FS, recording_int16)

print("保存完了。")

# WAVファイルを読み込んで再生
print(f"{FILENAME}を読み込んで再生します...")
samplerate, data = read(FILENAME)
print(f"読み込んだファイルの周波数: {samplerate} Hz")
sd.play(data, samplerate)
sd.wait()
print("再生完了。")
