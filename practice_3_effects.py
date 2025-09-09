# practice_3_effects.py
import sounddevice as sd
import numpy as np
import argparse
import soundfile as sf

# --- 説明 ---
# このスクリプトは、録音した音声または指定されたWAVファイルにエフェクトをかけて再生します。
# コマンドラインから -f (または --file) オプションでWAVファイルを指定できます。
# 例: python practice_3_effects.py -f my_voice.wav
# 引数なしで実行すると、3秒間の録音を行います。
# 詳細は -h オプションで確認してください。
# ----------

# コマンドライン引数の設定
parser = argparse.ArgumentParser(description="Apply effects to audio from recording or a WAV file.")
parser.add_argument("-f", "--file", type=str, help="Path to the WAV file to process.")
args = parser.parse_args()

FS = 44100
DURATION = 3

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
    print(f"{DURATION}秒間録音します...")
    myrecording = sd.rec(int(DURATION * FS), samplerate=FS, channels=1)
    sd.wait()
    print("録音終了。")

# 1. 音量UP
print("音量を2倍にして再生")
sd.play(myrecording * 2, FS); sd.wait()

# 2. 逆再生
print("逆再生")
sd.play(myrecording[::-1], FS); sd.wait()

# 3. 結合
print("1秒の無音を挟んで2回再生")
# 入力音声のチャンネル数に合わせて無音配列の形状を決定する
if myrecording.ndim == 1:
    # 1D配列（モノラル）の場合
    one_sec_silence = np.zeros(FS * 1, dtype=myrecording.dtype)
else:
    # 2D配列（モノラルまたはステレオ）の場合
    num_channels = myrecording.shape[1]
    one_sec_silence = np.zeros((FS * 1, num_channels), dtype=myrecording.dtype)

combined_audio = np.concatenate([myrecording, one_sec_silence, myrecording])
sd.play(combined_audio, FS); sd.wait()


# 4. やまびこ
print("やまびこ")
delay_sec = 0.3
delay_samples = int(delay_sec * FS)
echo_audio = np.copy(myrecording)
if myrecording.ndim == 1:
    echo_audio[delay_samples:] += myrecording[:-delay_samples] * 0.5
else:
    echo_audio[delay_samples:, :] += myrecording[:-delay_samples, :] * 0.5
sd.play(echo_audio, FS); sd.wait()

print("完了。")
