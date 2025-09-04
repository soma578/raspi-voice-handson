# practice_5_tts.py (高機能版)
import pyopenjtalk
import sounddevice as sd
import os
import glob

# --- 設定 ---
VOICES_DIR = "./voices"  # .htsvoiceファイルが格納されているディレクトリ
text = "こんにちは。好きな声を選んで、私に喋らせてみてください。"

# --- 利用可能なボイスを探す ---
# voicesディレクトリから.htsvoiceファイルをすべて検索
voice_files = glob.glob(os.path.join(VOICES_DIR, "*.htsvoice"))

# 選択肢のリストを作成 (0番はデフォルトボイス)
available_voices = ["0: デフォルト"]
for i, voice_file in enumerate(voice_files):
    # ファイル名からボイス名を取得 (例: mei_normal.htsvoice -> mei_normal)
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

print(f"\n声: {voice_name_for_display}")
print(f"テキスト: 「{text}」")

# voice引数を指定して音声合成（選択されなかった場合はNoneが渡され、デフォルトボイスになる）
audio_data, FS = pyopenjtalk.tts(text, voice=selected_voice_path)

# --- 再生 ---
print("再生します...")
sd.play(audio_data, FS)
sd.wait()
print("再生完了。")