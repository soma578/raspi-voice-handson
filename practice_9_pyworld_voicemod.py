# practice_9_pyworld_voicemod.py
import soundfile as sf
import pyworld as pw
import numpy as np
import sounddevice as sd
import sys

INPUT_FILE = "my_voice.wav" # practice_4で作成したファイル
OUTPUT_FILE = "my_voice_mod.wav"

print(f"{INPUT_FILE} をPyWorldで加工します。")

try:
    x, fs = sf.read(INPUT_FILE)
    x = x.astype(np.float64) # PyWorldはfloat64を要求する
except FileNotFoundError:
    print(f"エラー: {INPUT_FILE} が見つかりません。")
    print("先に practice_4_wav.py を実行して、変換元のWAVファイルを作成してください。")
    sys.exit()

# --- PyWorldによる分析 ---
# F0(基本周波数), sp(スペクトル包絡), ap(非周期性指標)に分解
f0, t = pw.dio(x, fs)
sp = pw.cheaptrick(x, f0, t, fs)
ap = pw.d4c(x, f0, t, fs)

# --- パラメータの加工 ---
# 声の高さを1.5倍にする (1.0が元)
f0_rate = 1.5
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
