# practice_5_tts.py
import sounddevice as sd
import os
import glob
import subprocess
import soundfile as sf

# --- 設定 ---
VOICES_DIR = "./voices"  # .htsvoiceファイルが格納されているディレクトリ
JNICT_DIC_PATH = "/var/lib/mecab/dic/open-jtalk/naist-jdic" # Open JTalkの辞書パス
OUTPUT_WAV_PATH = "output/tts_output.wav" # 生成されるWAVファイルの一時的な置き場所
text = "こんにちは。好きな声を選んで、私に喋らせてみてください。"

# --- 利用可能なボイスを探す ---
# voicesディレクトリとサブディレクトリから.htsvoiceファイルを再帰的に検索
voice_files = glob.glob(os.path.join(VOICES_DIR, "**", "*.htsvoice"), recursive=True)

# 選択肢のリストを作成 (0番はデフォルトボイス)
available_voices = ["0: デフォルト"]
for i, voice_file in enumerate(voice_files):
    voice_name = os.path.splitext(os.path.basename(voice_file))[0]
    available_voices.append(f"{i+1}: {voice_name}")

# --- ユーザーにボイスを選択させる ---
print("利用可能なボイス:")
for v in available_voices:
    print(f"  {v}")

selected_voice_path = None
while True:
    try:
        choice = int(input(f"使用するボイスの番号を入力してください (0-{len(available_voices)-1}): "))
        if 0 <= choice < len(available_voices):
            if choice > 0:
                selected_voice_path = voice_files[choice - 1]
            break
        else:
            print("無効な番号です。")
    except ValueError:
        print("数値を入力してください。")

# --- 音声合成 ---
voice_name_for_display = "デフォルト"
if selected_voice_path:
    voice_name_for_display = os.path.splitext(os.path.basename(selected_voice_path))[0]

print(f"""
声: {voice_name_for_display}""")
print(f"テキスト: 「{text}」")

# open_jtalkコマンドを構築
command = ["open_jtalk"]
command += ["-x", JNICT_DIC_PATH]
if selected_voice_path:
    command += ["-m", selected_voice_path]
command += ["-ow", OUTPUT_WAV_PATH]

# 出力ディレクトリがなければ作成
os.makedirs(os.path.dirname(OUTPUT_WAV_PATH), exist_ok=True)

print("\nopen_jtalkコマンドを実行して音声を生成します...")
try:
    # コマンドを実行。テキストは標準入力経由で渡す。
    subprocess.run(command, input=text, encoding='utf-8', check=True, stderr=subprocess.PIPE)

    # 生成されたWAVファイルを読み込む
    audio_data, FS = sf.read(OUTPUT_WAV_PATH)

    # --- 再生 ---
    print("再生します...")
    sd.play(audio_data, FS)
    sd.wait()
    print("再生完了。")

except FileNotFoundError:
    print("エラー: 'open_jtalk'コマンドが見つかりません。aptでインストールされているか確認してください。")
except subprocess.CalledProcessError as e:
    print("open_jtalkの実行中にエラーが発生しました。")
    print("ボイスファイルや辞書のパスが正しいか確認してください。")
    print(e.stderr.decode())