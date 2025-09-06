# practice_9_pyworld_voicemod.py
import soundfile as sf
import pyworld as pw
import numpy as np
import sounddevice as sd
import sys
import argparse

# --- 説明 ---
# このスクリプトは、指定されたWAVファイルのピッチ（声の高さ）を変更し、別ファイルとして保存します。
# -i: 入力ファイル (デフォルト: my_voice.wav)
# -o: 出力ファイル (デフォルト: my_voice_mod.wav)
# --f0_rate: 声の高さの倍率 (デフォルト: 1.5)
# 例: python practice_9_pyworld_voicemod.py -i input.wav -o output.wav --f0_rate 2.0
# 詳細は -h オプションで確認してください。
# ----------

# コマンドライン引数の設定
parser = argparse.ArgumentParser(description="Modify voice pitch using PyWorld.")
parser.add_argument("-i", "--input", type=str, default="my_voice.wav", help="Path to the input WAV file. Defaults to my_voice.wav.")
parser.add_argument("-o", "--output", type=str, default="my_voice_mod.wav", help="Path for the output modified WAV file. Defaults to my_voice_mod.wav.")
parser.add_argument("--f0_rate", type=float, default=1.5, help="F0 modification rate. >1 for higher pitch, <1 for lower. Defaults to 1.5.")
args = parser.parse_args()

INPUT_FILE = args.input
OUTPUT_FILE = args.output
f0_rate = args.f0_rate

print(f"{INPUT_FILE} をPyWorldで加工します。")

try:
    x, fs = sf.read(INPUT_FILE)
    x = x.astype(np.float64) # PyWorldはfloat64を要求する
except FileNotFoundError:
    print(f"エラー: {INPUT_FILE} が見つかりません。")
    if INPUT_FILE == "my_voice.wav":
        print("先に practice_4_wav.py を実行して、変換元のWAVファイルを作成してください。")
    sys.exit()

# --- PyWorldによる分析 ---
# F0(基本周波数), sp(スペクトル包絡), ap(非周期性指標)に分解
f0, t = pw.dio(x, fs)
sp = pw.cheaptrick(x, f0, t, fs)
ap = pw.d4c(x, f0, t, fs)

# --- パラメータの加工 ---
# 声の高さを変更
modified_f0 = f0 * f0_rate

# --- PyWorldによる再合成 ---
synthesized = pw.synthesize(modified_f0, sp, ap, fs)

# --- 再生と保存 ---
print("元の音声を再生します...")
sd.play(x.astype(np.float32), fs) # 再生時はfloat32に戻す
sd.wait()

print(f"声のピッチを{f0_rate}倍にした音声を再生します...")
sd.play(synthesized.astype(np.float32), fs)
sd.wait()

# ファイルに保存
sf.write(OUTPUT_FILE, synthesized, fs)
print(f"加工した音声を {OUTPUT_FILE} に保存しました。")
