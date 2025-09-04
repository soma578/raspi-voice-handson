# PCで学ぶ！Python音声処理入門【完全版】

## 1. はじめに

このドキュメントは、特別なハードウェアを使わず、お手元のPC（Windows）とPythonを使って音声処理の基本を学ぶための入門ガイドです。マイクからの録音、スピーカーでの再生、そして録音した音声データの加工といった一連の流れを、理論と実践を交えながら体験することを目指します。

このガイドは、各章で登場する技術やライブラリを、実際に使いながらその都度詳しく学んでいく「実践中心」の構成になっています。

---

## 2. クイックスタート: 環境構築

まず、このガイドで必要になるツールをすべてPCにセットアップします。ここでの詳しい説明は各実践の章に譲り、ひとまずインストール作業を完了させましょう。

### 手順1: Pythonライブラリの一括インストール

このプロジェクトに必要なライブラリは`requirements.txt`にまとめてあります。
以下のコマンドを、お使いのPCのターミナル（コマンドプロンプトやPowerShell）で実行してください。`requirements.txt`ファイルにリストされたライブラリが自動的に一括でインストールされます。

```bash
pip install -r requirements.txt
```

### 手順2: 外部ツール `ffmpeg` のインストール

`ffmpeg`は、音声や動画のフォーマットを変換するための非常に強力な外部ツールです。後の章でWAVファイルをMP3に変換する際に使います。

1.  **ダウンロード**: [ffmpeg.orgのダウンロードページ](https://ffmpeg.org/download.html)にアクセスし、Windowsロゴからリンクされている`gyan.dev`などのサイトから、`release`ビルドの`full`版（例: `ffmpeg-release-full.7z`）をダウンロードします。
2.  **配置**: ダウンロードした圧縮ファイルを解凍し、中身のフォルダを`C:\ffmpeg`のような分かりやすい場所に配置します。
3.  **環境変数「PATH」の設定**: Windowsの検索バーで「**環境変数を編集**」と検索し、「システム環境変数の編集」を開きます。「環境変数」→「システム環境変数」の`Path`を選択→「編集」→「新規」と進み、`ffmpeg`の`bin`フォルダのパス（例: `C:\ffmpeg\bin`）を追加します。
4.  **確認**: **新しい**コマンドプロンプトを開き`ffmpeg -version`と入力し、バージョン情報が表示されれば成功です。

### 手順3: 音声認識・合成モデルの準備

#### Vosk言語モデル (音声認識用)
1.  **ダウンロード**: [Vosk Models Page](https://alphacephei.com/vosk/models)にアクセスし、日本語モデル（`vosk-model-ja-0.22`など）をダウンロードします。
2.  **配置**: ダウンロードしたzipファイルを解凍し、出てきたフォルダを、このプロジェクトフォルダ（各種`practice_..._.py`を置く場所）内に配置してください。

#### Open JTalkボイスフォント (音声合成用)
1.  **`voices`ディレクトリの作成**: プロジェクトフォルダに`voices`という名前の新しいディレクトリを作成してください。
2.  **ダウンロードと配置**: [MMDAgent & Project-NAIPのSourceForgeページ](https://osdn.net/projects/mmdagent/releases/p12473)から`MMDAgent_Example-1.8.zip`をダウンロードし、解凍します。中にある`Voice`フォルダ内の`mei`や`takumi`といった各フォルダの中から、`.htsvoice`で終わるファイルをすべて探し、先ほど作成した`voices`ディレクトリの中にコピーします。

---

## 3. 音声データの基本（理論編）

音は空気の振動（アナログ信号）ですが、コンピュータは数値（デジタル信号）しか扱えません。この変換プロセスが「**A/D変換**」であり、その核心が**サンプリング（標本化）**と**量子化**です。

- **サンプリング周波数 (Hz)**: 1秒間に音を何回サンプリング（測定）するか。数値が大きいほど高音質になります。(例: CDは44100 Hz)
- **ビット深度 (bit)**: 1回のサンプリングで得た音の大きさ（振幅）を、どれくらいの細かさで数値化するか。数値が大きいほど表現豊かな音になります。(例: 16 bitなら$2^{16}$=65,536段階)

このプロセスを経て生成された、生の音声データが **PCM (Pulse-Code Modulation)** データです。私たちがPythonで扱うのは、このPCMデータを`numpy`配列という形式にしたものです。

---

## 4. 実践1: 音声の再生

まず、音声ファイルを再生するいくつかの方法を見てみましょう。ここでは`scipy`でWAVファイルを読み込み、それを各ライブラリで再生します。

### 4.1 `sounddevice`による再生 (基本)
`sounddevice`は、`numpy`配列を直接扱え、遅延も少なく、録音と再生を同じライブラリで一貫して扱えるため、このガイドの基本とします。

```python
# practice_1_sounddevice_playback.py
from scipy.io.wavfile import read
import sounddevice as sd

FS, data = read("my_voice.wav") # practice_4で作成
sd.play(data, FS)
sd.wait()
```

### 4.2 (別解) `PyAudio`による再生
`PyAudio`は古くから使われているライブラリで、より低レベルなストリーミング処理が可能です。データを小さな「チャンク」に区切って、順次再生していく方式です。

```python
# practice_1b_pyaudio_playback.py
import wave, pyaudio, sys

wf=wave.open("my_voice.wav", "r")
p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()), channels=wf.getnchannels(), rate=wf.getframerate(), output=True)
chunk = 1024
data = wf.readframes(chunk)
while data != b'':
    stream.write(data)
    data = wf.readframes(chunk)
stream.close()
p.terminate()
```

### 4.3 (別解) `PyGame`による再生
`PyGame`はゲーム制作用のライブラリですが、その中の`mixer`モジュールは音声再生機能が強力で、MP3やMIDIなど、WAV以外のフォーマットも簡単に扱えるのが利点です。

```python
# practice_1c_pygame_playback.py
import pygame.mixer as m

m.init()
m.music.load("converted_audio.mp3") # practice_7で作成
m.music.play()
while m.music.get_busy():
    continue
```

---

## 5. 実践2: 録音

`sounddevice`を使ってPCのマイクから音を録音し、`scipy`でWAVファイルに保存します。

```python
# practice_2_record.py (旧practice_4_wav.py)
import sounddevice as sd
from scipy.io.wavfile import write

FS = 44100
DURATION = 5
FILENAME = "my_voice.wav"

print("録音を開始します...")
recording = sd.rec(int(DURATION * FS), samplerate=FS, channels=1)
sd.wait()
write(FILENAME, FS, recording)
print(f"{FILENAME} に録音を保存しました。")
```

---

## 6. 実践3: 音声の可視化

録音した音声がどんな形をしているのか、グラフにして見てみましょう。

### 6.1 波形の描画
横軸を時間、縦軸を振幅とする最も基本的なグラフです。

```python
# practice_3a_waveform.py (旧practice_2_visualize.py)
from scipy.io.wavfile import read
import numpy as np
import matplotlib.pyplot as plt

FS, data = read("my_voice.wav")
time = np.arange(len(data)) / FS

plt.plot(time, data)
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.show()
```

### 6.2 スペクトログラムの描画
波形をさらに分析し、横軸を時間、縦軸を周波数、色の濃淡をその周波数成分の強さで表現したものがスペクトログラムです。声紋分析などにも使われる、より情報量の多いグラフです。

```python
# practice_3b_spectrogram.py (旧practice_2b_spectrogram.py)
from scipy.io.wavfile import read
from scipy.signal import spectrogram
import matplotlib.pyplot as plt

FS, data = read("my_voice.wav")

f, t, Sxx = spectrogram(data, fs=FS)

plt.pcolormesh(t, f, 10 * np.log10(Sxx + 1e-9), shading='gouraud')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [sec]')
plt.ylim(0, 8000)
plt.show()
```

---

## 7. 実践4: 音声データの加工

`numpy`の配列操作を駆使して、音声に様々なエフェクトをかけます。

```python
# practice_4_effects.py (旧practice_3_effects.py)
from scipy.io.wavfile import read, write
import sounddevice as sd
import numpy as np

FS, data = read("my_voice.wav")

# 1. 音量UP
sd.play(data * 2, FS); sd.wait()

# 2. 逆再生
sd.play(data[::-1], FS); sd.wait()

# 3. 結合 (1秒の無音を挟む)
one_sec_silence = np.zeros(FS * 1, dtype=data.dtype)
combined = np.concatenate([data, one_sec_silence, data])
write("combined.wav", FS, combined)
```

---

## 8. 実践5: オフライン音声合成 (Open JTalk)

PCにインストールしたモデルを使って、オフラインで日本語テキストから音声を生成します。`voices`ディレクトリに用意したボイスフォントを選択して使います。

```python
# practice_5_tts.py (高機能版)
import pyopenjtalk, sounddevice as sd, os, glob

VOICES_DIR = "./voices"
text = "こんにちは。好きな声を選んで、私に喋らせてみてください。"

voice_files = glob.glob(os.path.join(VOICES_DIR, "*.htsvoice"))
available_voices = ["0: デフォルト"] + [f"{i+1}: {os.path.splitext(os.path.basename(v))[0]}" for i, v in enumerate(voice_files)]

print("利用可能なボイス:")
for v in available_voices: print(f"  {v}")

selected_voice_path = None
while True:
    try:
        choice = int(input(f"番号を入力 (0-{len(available_voices)-1}): "))
        if 0 <= choice < len(available_voices):
            if choice > 0: selected_voice_path = voice_files[choice - 1]
            break
    except ValueError: pass

audio_data, FS = pyopenjtalk.tts(text, voice=selected_voice_path)
sd.play(audio_data, FS)
sd.wait()
```

---

## 9. 実践6: オンライン音声合成 (gTTS)

Googleのオンラインサービス(gTTS)を使い、より自然な音声を生成します。インターネット接続が必要です。

```python
# practice_6_gtts.py (旧practice_8_gtts.py)
from gtts import gTTS
import pygame.mixer as m

mytext = "こんにちは。こちらは、グーグルのオンライン音声合成サービスです。"
FILENAME = "gtts_hello.mp3"

tts = gTTS(text=mytext, lang='ja')
tts.save(FILENAME)

m.init()
m.music.load(FILENAME)
m.music.play()
while m.music.get_busy(): continue
```

---

## 10. 実践7: 音声認識 (Vosk)

マイクで話した言葉をテキストに変換します。Voskの言語モデルが必要です。

```python
# practice_7_stt.py (旧practice_6_stt.py)
import sounddevice as sd, numpy as np, json, os
from vosk import Model, KaldiRecognizer

MODEL_DIR = "vosk-model-ja-0.22"
FS = 16000
DURATION = 5

if not os.path.exists(MODEL_DIR): exit("Voskモデルが見つかりません。")

print(f"{DURATION}秒間、話してください...")
myrecording = sd.rec(int(DURATION * FS), samplerate=FS, channels=1, dtype='float32')
sd.wait()

model = Model(MODEL_DIR)
recognizer = KaldiRecognizer(model, FS)
recognizer.AcceptWaveform((myrecording * 32767).astype(np.int16).tobytes())
result = json.loads(recognizer.FinalResult())
print(f"認識結果: {result['text']}")
```

---

## 11. 実践8: フォーマット変換 (ffmpeg)

`ffmpeg`をPythonから呼び出し、WAVファイルをMP3に変換します。

```python
# practice_8_converter.py (旧practice_7_converter.py)
import subprocess

INPUT_WAV = "my_voice.wav"
OUTPUT_MP3 = "converted_audio.mp3"

command = ["ffmpeg", "-i", INPUT_WAV, "-y", "-b:a", "192k", OUTPUT_MP3]

try:
    subprocess.run(command, check=True)
    print("変換成功！")
except FileNotFoundError:
    print("エラー: ffmpegが見つかりません。")
```

---

## 12. 最終実践: ボイスチェンジャー (PyWorld)

音声の正体である「基本周波数(F0)」を直接操作し、声のピッチ（高さ）を自在に変えてみましょう。

```python
# practice_9_pyworld_voicemod.py
import soundfile as sf, pyworld as pw, numpy as np, sounddevice as sd

# 声を高くする倍率
PITCH_RATE = 1.5

x, fs = sf.read("my_voice.wav")
x = x.astype(np.float64)

# PyWorldで音声の構成要素に分解
f0, t = pw.dio(x, fs)
sp = pw.cheaptrick(x, f0, t, fs)
ap = pw.d4c(x, f0, t, fs)

# 基本周波数(f0)を加工
modified_f0 = f0 * PITCH_RATE

# 構成要素を再合成
synthesized = pw.synthesize(modified_f0, sp, ap, fs)

# 元の声と再生して比較
print("元の音声を再生します...")
sd.play(x, fs); sd.wait()
print(f"ピッチを{PITCH_RATE}倍にした音声を再生します...")
sd.play(synthesized, fs); sd.wait()

sf.write("my_voice_mod.wav", synthesized, fs)
```

---

## 13. まとめ

このガイドでは、音声処理の基本的な理論から、Pythonを使った録音・再生・加工・ファイル操作、さらには音声合成・認識、フォーマット変換、ボイスチェンジまで、一通りの技術を実践的に学びました。ぜひ、自分だけの音声アプリケーション開発に挑戦してみてください。