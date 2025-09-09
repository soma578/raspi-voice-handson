# Python音声処理スクリプト コード解説ガイド

このドキュメントは、「PCで学ぶ！Python音声処理入門」の各Pythonスクリプトのソースコードと、その詳細な解説を記載します。

メインの `README.md` と合わせて参照することで、理論から実践的なコードまで、より深く理解することができます。

---

## `practice_1_record_playback.py`

### 役割
音声を録音して再生する、または、指定されたWAVファイルを再生する、最も基本的なスクリプトです。

### コード全文
```python
# practice_1_record_playback.py
import sounddevice as sd
import numpy as np
import argparse
import soundfile as sf

parser = argparse.ArgumentParser(description="Record audio or play a WAV file.")
parser.add_argument("-f", "--file", type=str, help="Path to the WAV file to play.")
args = parser.parse_args()

FS = 44100
DURATION = 5

if args.file:
    try:
        myrecording, FS = sf.read(args.file, dtype='float32')
        print(f"WAVファイル '{args.file}' を読み込みました。")
    except Exception as e:
        exit(f"エラー: ファイルを読み込めません。 {e}")
else:
    print(f"{DURATION}秒間、録音します...")
    myrecording = sd.rec(int(DURATION * FS), samplerate=FS, channels=1)
    sd.wait()
    print("録音終了。")

print("再生します...")
sd.play(myrecording, FS)
sd.wait()
print("再生完了。")
```

### 解説
1.  **`argparse`**: コマンドラインで `-f` オプションを受け付けます。
2.  **`args.file`のチェック**: ファイルが指定されていれば `soundfile.read()` で読み込み、なければ `sounddevice.rec()` で録音します。
3.  **`sd.play()`**: Numpy配列として格納された音声データを再生します。

---

## `practice_1b_pyaudio_playback.py`

### 役割
`PyAudio`ライブラリを使ったWAVファイルの再生方法を示します。ストリーミング再生の基本的な考え方を理解できます。

### コード全文
```python
# practice_1b_pyaudio_playback.py
import wave
import pyaudio
import sys

FILENAME = "my_voice.wav"

try:
    wf=wave.open(FILENAME, "r")
except FileNotFoundError:
    exit(f"エラー: {FILENAME} が見つかりません。先に practice_4_wav.py を実行してください。")

p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)
chunk = 1024
data = wf.readframes(chunk)
while data != b'':
    stream.write(data)
    data = wf.readframes(chunk)
stream.close()
p.terminate()
print(f"{FILENAME} の再生が完了しました。")
```

### 解説
1.  **`pyaudio.PyAudio()`**: PyAudioのインスタンスを生成します。
2.  **`p.open(...)`**: WAVファイルのパラメータ（チャンネル数、サンプリング周波数など）を元に、音声出力用の「ストリーム」を開きます。
3.  **`wf.readframes(chunk)`**: WAVファイルから `chunk` サイズ（ここでは1024サンプル）ずつ、データを少しずつ読み込みます。
4.  **`stream.write(data)`**: 読み込んだデータをストリームに書き込むことで、音声が再生されます。ファイルが終わるまでこれを繰り返します。

---

## `practice_1c_pygame_playback.py`

### 役割
ゲームライブラリ `PyGame` の音声機能 `mixer` を使った再生方法を示します。MP3など多様な形式を簡単に扱えるのが特徴です。

### コード全文
```python
# practice_1c_pygame_playback.py
import pygame.mixer as m
import pygame.time
import sys, os

FILENAME = "converted_audio.mp3"

if not os.path.exists(FILENAME):
    exit(f"エラー: {FILENAME} が見つかりません。先に practice_7_converter.py を実行してください。")

m.init()
m.music.load(FILENAME)
m.music.play()
while m.music.get_busy():
    pygame.time.delay(100)
m.music.stop()
print(f"{FILENAME} の再生が完了しました。")
```

### 解説
1.  **`m.init()`**: `pygame.mixer` を初期化します。
2.  **`m.music.load()`**: 再生したい音声ファイルを読み込みます。
3.  **`m.music.play()`**: 再生を開始します。再生はバックグラウンドで行われます。
4.  **`while m.music.get_busy()`**: `get_busy()` が `True` の間（＝再生中）、ループを続けることで、再生が終わるまでプログラムが終了しないように待機します。

---

## `practice_2_visualize.py`

### 役割
音声データを時間軸の波形としてグラフにプロットし、画像ファイルとして保存します。

### コード全文
```python
# practice_2_visualize.py
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import argparse
import soundfile as sf

# (argparse部分は practice_1 と同様)
parser = argparse.ArgumentParser(description="Visualize audio from recording or a WAV file.")
parser.add_argument("-f", "--file", type=str, help="Path to the WAV file to visualize.")
args = parser.parse_args()

FS = 44100
DURATION = 5

if args.file:
    # ... (ファイル読み込み)
else:
    # ... (録音)

# 時間軸を作成
time = np.arange(0, len(myrecording)) / FS

# グラフを描画
plt.figure(figsize=(12, 4))
plt.plot(time, myrecording)
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.title("Waveform")
plt.grid()

# グラフをファイルに保存
output_filename = "waveform.png"
plt.savefig(output_filename)
print(f"グラフを {output_filename} として保存しました。")
```

### 解説
1.  **`np.arange(...) / FS`**: グラフのX軸（時間軸）を作成します。
2.  **`plt.plot(...)`**: `matplotlib`を使い、X軸を時間、Y軸を音声データの振幅として線グラフをプロットします。
3.  **`plt.savefig(...)`**: プロットしたグラフを、ウィンドウで表示する代わりに画像ファイルとして保存します。

---

## `practice_3_effects.py`

### 役割
Numpy配列の強力な数値計算機能を使い、音声データに様々なエフェクトを適用します。

### コード全文
```python
# practice_3_effects.py
import sounddevice as sd
import numpy as np
import argparse
import soundfile as sf

# (argparse部分は practice_1 と同様)
# ...

# 1. 音量UP
print("音量を2倍にして再生")
sd.play(myrecording * 2, FS); sd.wait()

# 2. 逆再生
print("逆再生")
sd.play(myrecording[::-1], FS); sd.wait()

# 3. 結合
# ... (チャンネル数を合わせて無音配列を作成)

# 4. やまびこ
# ... (配列をずらして足し合わせる)
```

### 解説
- **音量UP**: Numpy配列全体を `* 2` で2倍します。
- **逆再生**: `[::-1]` は、Numpy配列の要素を逆順にするスライス表記です。
- **結合**: `np.zeros()` で無音の配列を生成し、`np.concatenate()` で連結します。
- **やまびこ**: 配列をコピーし、一定時間ずらした音声を、音量を半分にして足し合わせています。

---

## `practice_4_wav.py`

### 役割
録音した音声データを、互換性の高い16bit整数形式のWAVファイルとして保存します。

### コード全文
```python
# practice_4_wav.py
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import argparse

# (argparseで出力ファイル名を指定)
# ...

# 録音
recording = sd.rec(int(DURATION * FS), samplerate=FS, channels=1)
sd.wait()

# float32からint16へ変換し、互換性の高い形式で保存
recording_int16 = np.int16(recording * 32767)
write(FILENAME, FS, recording_int16)
print("保存完了。")
```

### 解説
- **`np.int16(recording * 32767)`**: `sounddevice`が返す-1.0〜1.0のfloat型配列を、16bit整数の範囲 (-32768〜32767) の値に変換します。
- **`write(FILENAME, FS, recording_int16)`**: 変換後の整数配列をWAVファイルとして書き出します。

---

## `practice_5_tts.py`

### 役割
`open_jtalk`というコマンドラインツールを直接呼び出して、安定したテキスト読み上げを実現します。

### コード全文
```python
# practice_5_tts.py
import sounddevice as sd
import os, glob, subprocess, soundfile as sf

# (各種パス設定、ボイス選択UI部分は省略)
# ...

# open_jtalkコマンドを構築
command = ["open_jtalk"]
command += ["-x", JNICT_DIC_PATH]
if selected_voice_path:
    command += ["-m", selected_voice_path]
command += ["-ow", OUTPUT_WAV_PATH]

# コマンドを実行
try:
    subprocess.run(command, input=text, encoding='utf-8', check=True, stderr=subprocess.PIPE)
    audio_data, FS = sf.read(OUTPUT_WAV_PATH)
    sd.play(audio_data, FS)
    sd.wait()
except Exception as e:
    # ... (エラー処理)
```

### 解説
1.  **`command = [...]`**: `open_jtalk` コマンドに渡す引数をリスト形式で組み立てます。
2.  **`subprocess.run(...)`**: 組み立てたコマンドを実行します。`input=text`で読み上げるテキストを渡します。
3.  **`sf.read(...)`**: `open_jtalk`が生成したWAVファイルを`soundfile`で読み込み、再生します。

---

## `practice_7_converter.py`

### 役割
`ffmpeg`コマンドを呼び出し、WAVファイルをMP3ファイルに変換します。

### コード全文
```python
# practice_7_converter.py
import subprocess, os

INPUT_WAV = "my_voice.wav"
OUTPUT_MP3 = "converted_audio.mp3"

if not os.path.exists(INPUT_WAV):
    exit(f"エラー: {INPUT_WAV} が見つかりません。 practice_4_wav.py で作成してください。")

command = ["ffmpeg", "-i", INPUT_WAV, "-y", "-b:a", "192k", OUTPUT_MP3]

try:
    subprocess.run(command, check=True, capture_output=True, text=True)
    print("変換成功！")
except FileNotFoundError:
    print("エラー: ffmpegが見つかりません。PATHを確認してください。")
except subprocess.CalledProcessError as e:
    print(f"ffmpegエラー: {e.stderr}")
```

### 解説
- **`command = [...]`**: `ffmpeg`コマンドと、そのオプション（`-i`=入力, `-y`=上書き許可, `-b:a`=ビットレート）をリストで定義します。
- **`subprocess.run(...)`**: `ffmpeg`を実行します。`check=True`で、コマンドが失敗した場合にエラーを発生させます。

---

## `practice_8_gtts.py`

### 役割
Googleのオンラインサービスを使い、高品質な自然音声を生成します。

### コード全文
```python
# practice_8_gtts.py
from gtts import gTTS
import pygame.mixer as m

mytext = "こんにちは。こちらは、グーグルのオンライン音声合成サービスです。"
FILENAME = "gtts_hello.mp3"

try:
    tts = gTTS(text=mytext, lang='ja')
    tts.save(FILENAME)
except Exception as e:
    exit(f"エラー: 音声の生成に失敗しました。インターネット接続を確認してください。 {e}")

m.init()
m.music.load(FILENAME)
m.music.play()
while m.music.get_busy():
    continue
```

### 解説
1.  **`gTTS(text=mytext, lang='ja')`**: 読み上げるテキストと言語（`ja`=日本語）を指定して、`gTTS`オブジェクトを作成します。
2.  **`tts.save(FILENAME)`**: Googleのサーバーと通信し、生成された音声データをMP3ファイルとして保存します。
3.  **`pygame.mixer`**: 保存されたMP3ファイルを`pygame`で再生します。

---

## `practice_9_pyworld_voicemod.py`

### 役割
`PyWorld`ライブラリを使い、声の高さ（ピッチ）を変更するボイスチェンジャーを実現します。

### コード全文
```python
# practice_9_pyworld_voicemod.py
import soundfile as sf
import pyworld as pw
import numpy as np
import sounddevice as sd
import argparse

# (argparse部分は省略)
# ...

x, fs = sf.read(INPUT_FILE)
x = x.astype(np.float64)

f0, t = pw.dio(x, fs)
sp = pw.cheaptrick(x, f0, t, fs)
ap = pw.d4c(x, f0, t, fs)

modified_f0 = f0 * f0_rate

synthesized = pw.synthesize(modified_f0, sp, ap, fs)

sd.play(synthesized.astype(np.float32), fs)
sd.wait()

sf.write(OUTPUT_FILE, synthesized, fs)
```

### 解説
1.  **`pw.dio`, `pw.cheaptrick`, `pw.d4c`**: 音声`x`を、声の高さの元となる`f0`（基本周波数）、声色を決める`sp`（スペクトル包絡）、息遣いなどの成分である`ap`（非周期性指標）の3つのパラメータに分解します。
2.  **`modified_f0 = f0 * f0_rate`**: F0（基本周波数）の配列全体を一定倍率で変更します。
3.  **`pw.synthesize(...)`**: 加工したパラメータを元に、音声を再合成します。
