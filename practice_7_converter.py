# practice_7_converter.py
import subprocess
from scipy.io.wavfile import write
import numpy as np

# まずはダミーのWAVファイルを作成
FS = 44100
dummy_audio = (np.sin(np.arange(FS * 3) * 440 * 2 * np.pi / FS) * 0.5).astype(np.float32)
INPUT_WAV = "temp_for_ffmpeg.wav"
OUTPUT_MP3 = "converted_audio.mp3"
write(INPUT_WAV, FS, dummy_audio)

print(f"{INPUT_WAV}を{OUTPUT_MP3}に変換します...")

# ffmpegを呼び出すコマンドをリストで作成
command = [
    "ffmpeg",
    "-i", INPUT_WAV,      # 入力ファイル
    "-y",                 # 出力ファイルが既に存在する場合、確認なしで上書き
    "-b:a", "192k",       # 音声ビットレートを192kbpsに設定
    OUTPUT_MP3            # 出力ファイル
]

# subprocessでffmpegを実行
try:
    subprocess.run(command, check=True, capture_output=True, text=True)
    print("変換成功！")
except FileNotFoundError:
    print("エラー: ffmpegが見つかりません。PATHが正しく設定されているか確認してください。")
except subprocess.CalledProcessError as e:
    print("ffmpegの実行中にエラーが発生しました。")
    print(e.stderr) # ffmpegからのエラー出力を表示
