# PCで学ぶ！Python音声処理入門

## 1. はじめに

このドキュメントは、特別なハードウェアを使わず、お手元のPC（Windows）とPythonを使って音声処理の基本を学ぶための入門ガイドです。マイクからの録音、スピーカーでの再生、そして録音した音声データの加工といった一連の流れを、理論と実践を交えながら体験することを目指します。

### このガイドで学べること
- 音声がデジタルデータになる仕組み（サンプリング、PCM）
- Pythonを使ったPCの音声入出力（録音・再生）
- 音声データの正体である「NumPy配列」の操作
- 音声の視覚化（波形表示）
- 音声の加工（音量調整、逆再生、速度変更）
- テキストからの音声合成と、音声のテキスト化（音声認識）

---

## 2. Windows向け環境構築

まず、このガイドで必要になるツールをすべてPCにセットアップします。この章の手順を完了させれば、あとの実践パートをスムーズに進めることができます。

### 2-1. Pythonライブラリのインストール

最初に、音声処理で使うPythonライブラリを`pip`コマンドで一括インストールします。
以下のコマンドを、お使いのPCのターミナル（コマンドプロンプトやPowerShell）にコピー＆ペーストして実行してください。

```bash
pip install sounddevice numpy matplotlib scipy pyopenjtalk vosk
```

#### 各ライブラリの詳細な役割

インストールした各ライブラリが、それぞれどのような役割を担っているのかを解説します。

- **`sounddevice`**: PCの音声入出力を担う「窓口」
  - PythonプログラムとPCのハードウェア（マイク、スピーカー）との間の橋渡しをします。`sounddevice`のおかげで、複雑なハードウェアの違いを意識することなく、簡単に録音や再生ができます。

- **`numpy`**: 音声データを格納・計算する「魔法の箱」
  - 音声データは、実際には膨大な数の数値の集まりです。`numpy`は、この数値データを「配列(Array)」という形で効率的に扱い、高速に計算するためのライブラリです。音声の加工は、このNumPy配列を操作することそのものです。

- **`matplotlib`**: 音声データを視覚化する「グラフ描画ツール」
  - ただの数値の羅列である音声データを、人間が直感的に理解できる「波形グラフ」として表示するために使います。

- **`scipy`**: 科学技術計算ライブラリ
  - 非常に多機能なライブラリですが、このガイドでは主に、録音した音声をWAVファイルとして保存したり、既存のWAVファイルを読み込んだりするために`scipy.io.wavfile`という機能を利用します。

- **`pyopenjtalk`**: 日本語の音声合成エンジン
  - `Open JTalk`という、オフラインで動作するフリーの日本語音声合成エンジンをPythonから簡単に使えるようにしたものです。これを使うと、プログラムに任意の日本語テキストを喋らせることができます。

- **`vosk`**: オフラインで使える音声認識エンジン
  - マイクから入力された人間の声を、テキストに変換するために使います。オフラインで動作するため、インターネット接続がなくても利用できるのが大きな特徴です。

### 2-2. 外部ツール `ffmpeg` のインストール

`ffmpeg`は、音声や動画のフォーマットを変換したり、編集したりするための非常に強力なコマンドラインツールです。例えば、録音したWAVファイルをMP3ファイルに変換する、といった用途で使います。これはPythonライブラリではないため、手動でPCにインストールする必要があります。

#### インストール手順

1.  **公式サイトからファイルをダウンロード**
    - [ffmpeg.orgのダウンロードページ](https://ffmpeg.org/download.html)にアクセスします。
    - Windowsのロゴアイコンにマウスを合わせ、表示されるリンク（例: `gyan.dev` や `BtbN`）のどちらかをクリックします。
    - `gyan.dev`の場合、「release builds」の中から `ffmpeg-release-full.7z` のような名前のファイルをダウンロードします。（`.7z`はzipと同様の圧縮ファイルです。展開できない場合は[7-Zip](https://www.7-zip.org/)などをインストールしてください）

2.  **ファイルを解凍して配置**
    - ダウンロードした圧縮ファイルを解凍します。
    - 解凍して出てきたフォルダ（例: `ffmpeg-6.0-full_build`）を、`C:\`ドライブ直下など、分かりやすい場所に移動させます。ここでは例として `C:\ffmpeg` にフォルダ名を変更して配置したとします。
    - `C:\ffmpeg` の中には `bin`, `doc`, `presets` といったフォルダがあるはずです。重要なのは **`bin`** フォルダです。

3.  **環境変数「PATH」を設定**
    - `ffmpeg`をコマンドプロンプトのどこからでも呼び出せるように、`bin`フォルダの場所をWindowsに教えてあげる必要があります。
    - Windowsの検索バーで「**環境変数を編集**」と入力し、「システム環境変数の編集」を開きます。
    - 「環境変数」ボタンをクリックします。
    - 「システム環境変数」のリストから `Path` という変数を見つけて選択し、「編集」ボタンをクリックします。
    - 「新規」ボタンを押し、先ほど配置した`ffmpeg`の`bin`フォルダへのフルパス（例: `C:\ffmpeg\bin`）を入力し、「OK」をすべてのウィンドウで押して閉じます。

4.  **インストールの確認**
    - **新しい**コマンドプロンプトを開き（既に開いているものはダメ）、以下のコマンドを実行します。
      ```bash
      ffmpeg -version
      ```
    - `ffmpeg version ...` というようにバージョン情報が表示されれば、インストールは成功です。

### 2-3. 音声認識モデル `Vosk` の準備

`vosk`ライブラリはそれ単体では音声を認識できません。「どの言語を認識するのか」を定義した**モデルファイル**が別途必要になります。

1.  **モデルのダウンロード**: 
    以下の公式サイトから、日本語モデルをダウンロードします。
    - **Vosk Models Page**: [https://alphacephei.com/vosk/models](https://alphacephei.com/vosk/models)
    - `vosk-model-ja-0.22` のような、日本語用のモデル（zipファイル）を見つけてダウンロードしてください。（ファイルサイズが1GB以上あるので注意してください）

2.  **モデルの配置**: 
    ダウンロードしたzipファイルを解凍し、出てきたフォルダ（例: `vosk-model-ja-0.22`）を、これから作成するPythonスクリプトと同じ階層（プロジェクトフォルダ）に置いてください。

これで、すべての環境構築が完了しました。

---

## 3. 音声データの基本（理論編）

まず、コンピュータがどのように「音」を扱っているのか、その裏側にある理論を少しだけ覗いてみましょう。ここを理解すると、プログラミングがより面白くなります。

### アナログからデジタルへ
私たちの周りにある音は、空気の振動（疎密波）です。これは連続的な波であり、「アナログ信号」と呼ばれます。一方、コンピュータは「0」と「1」の集まりである「デジタル信号」しか扱えません。

音声処理とは、この**アナログ信号をデジタル信号に変換（A/D変換）**し、加工した後に、再び**アナログ信号に戻す（D/A変換）**プロセスです。

![Analog to Digital Conversion](https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Pcm.svg/450px-Pcm.svg.png)
*(出典: Wikipedia, Public Domain)*

この変換プロセスには、主に3つの重要なステップがあります。

### サンプリング（標本化）
アナログの滑らかな波を、一定の時間間隔で区切り、その瞬間の波の高さを測る（標本を採る）作業です。この「時間間隔」を細かくすればするほど、元の波形をより忠実に再現できます。

### サンプリング周波数 (Sampling Frequency)
**1秒間に何回サンプリングを行うか**を示す値です。単位はHz（ヘルツ）で表現されます。
- **44100 Hz (44.1 kHz)**: 音楽CDで使われている標準的な値。1秒間に44,100回も波の高さを測定しており、人間の耳には非常に滑らかに聞こえます。
- **16000 Hz (16 kHz)**: 音声認識や通話などでよく使われる値。人間の声の帯域は十分にカバーできますが、音楽には少し物足りなく感じるかもしれません。

### 量子化 (Quantization) と ビット深度 (Bit Depth)
サンプリングで測った波の「高さ」を、具体的な数値に置き換える作業が量子化です。この数値をどれだけ細かく表現できるかが**ビット深度**です。
- **16 bit**: 波の高さを $2^{16}$ = 65,536段階で表現します。
- **float32**: このガイドで使うデータ型。-1.0から1.0までの浮動小数点数で高さを表現し、非常に扱いやすい形式です。

### チャンネル (Channels)
音源の数を指します。
- **1 (モノラル)**: すべての音が1つのチャンネルにまとめられています。
- **2 (ステレオ)**: 左右2つのチャンネルを持ち、音の広がりや定位を表現できます。

### PCM (Pulse-Code Modulation)
上記の一連の処理（サンプリング→量子化）を経て作られた、**生のデジタル音声データ**のことを**PCMデータ**と呼びます。私たちがこれからPythonで扱うのは、まさにこのPCMデータです。

---

## 4. 実践1: 録音と再生

理論とツールの役割が分かったところで、いよいよ実践です。マイクから5秒間録音し、すぐに再生するプログラムを作成します。

**サンプルコード:**
```python
# practice_1_record_playback.py
import sounddevice as sd
import numpy as np

# --- パラメータ設定 ---
fs = 44100  # サンプリング周波数 (Hz)
duration = 5  # 録音時間 (秒)
CHANNELS = 1 # チャンネル数 (1: モノラル)

print("録音を開始します...")

# --- 録音 ---
myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=CHANNELS, dtype='float32')
sd.wait() # 録音が完了するまで待機

print("録音終了。")

# --- 再生 ---
print("録音した音声を再生します...")
sd.play(myrecording, fs)
sd.wait() # 再生が完了するまで待機

print("再生終了。")
```

---

## 5. 実践2: 音声の可視化（波形表示）

録音した`myrecording`の中身がどうなっているのか、グラフで見てみましょう。

**サンプルコード:**
```python
# practice_2_visualize.py
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt

# --- 録音 (実践1と同じ) ---
fs = 44100
duration = 5
print("5秒間録音します...")
myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
sd.wait()
print("録音終了。")

# --- 可視化 ---
# 時間軸のNumPy配列を作成
time = np.linspace(0., duration, myrecording.shape[0])

# matplotlibでグラフを描画
plt.figure(figsize=(10, 4))
plt.plot(time, myrecording)
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.title("Waveform")
plt.grid(True)
plt.show()
```

---

## 6. 実践3: 音声データの加工

録音したNumPy配列を直接操作して、音にエフェクトをかけてみましょう。

**サンプルコード:**
```python
# practice_3_effects.py
import sounddevice as sd
import numpy as np

# --- 録音 ---
fs = 44100
duration = 5
print(f"{duration}秒間、何か話してみてください...")
myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='float32')
sd.wait()
print("録音終了。")

# --- 元の音声を再生 ---
print("\n[1] 元の音声を再生します。")
sd.play(myrecording, fs)
sd.wait()

# --- 加工1: 音量を変更する ---
louder_audio = myrecording * 2.0
quieter_audio = myrecording * 0.5

print("\n[2] 音量を大きくして再生します。")
sd.play(louder_audio, fs)
sd.wait()

print("\n[3] 音量を小さくして再生します。")
sd.play(quieter_audio, fs)
sd.wait()

# --- 加工2: 逆再生 ---
reversed_audio = myrecording[::-1]

print("\n[4] 逆再生します。")
sd.play(reversed_audio, fs)
sd.wait()

# --- 加工3: 速度を変更する ---
speed_factor_fast = 1.5
speed_factor_slow = 0.7

print(f"\n[5] {speed_factor_fast}倍速で再生します。（音が高くなる）")
sd.play(myrecording, int(fs * speed_factor_fast))
sd.wait()

print(f"\n[6] {speed_factor_slow}倍速で再生します。（音が低くなる）")
sd.play(myrecording, int(fs * speed_factor_slow))
sd.wait()

print("\nすべての再生が完了しました。")
```

---

## 7. 実践4: テキストからの音声合成 (pyopenjtalk)

テキストを音声に変換する**音声合成（Text-To-Speech, TTS）**を扱います。

**サンプルコード:**
```python
# practice_4_tts.py
import pyopenjtalk
import sounddevice as sd

text = "こんにちは。今日はPythonで音声合成を試しています。"

print(f"音声合成中: 「{text}」")
audio_data, sampling_rate = pyopenjtalk.tts(text)

print(f"生成された音声のサンプリング周波数: {sampling_rate} Hz")

print("再生します...")
sd.play(audio_data, sampling_rate)
sd.wait()
print("再生完了。")
```

---

## 8. 実践5: 音声認識 (Vosk)

マイクで話した言葉をコンピュータに理解させる**音声認識（Speech-To-Text, STT）**に挑戦します。

**サンプルコード:**
```python
# practice_5_stt.py
import sounddevice as sd
import numpy as np
from vosk import Model, KaldiRecognizer
import json
import os

MODEL_DIR = "vosk-model-ja-0.22"
FS = 16000
DURATION = 5

if not os.path.exists(MODEL_DIR):
    print(f"エラー: Voskモデルのディレクトリ '{MODEL_DIR}' が見つかりません。")
    exit()

print(f"{DURATION}秒間、何か話してください...")
myrecording = sd.rec(int(DURATION * FS), samplerate=FS, channels=1, dtype='float32')
sd.wait()
print("録音終了。")

model = Model(MODEL_DIR)
recognizer = KaldiRecognizer(model, FS)

data = (myrecording * 32767).astype(np.int16).tobytes()

if recognizer.AcceptWaveform(data):
    result = json.loads(recognizer.Result())
    print(f"\n--- 認識結果 ---\n{result.get('text', '（認識できませんでした）')}")
```

---

## 9. 次のステップへ

このガイドで学んだことを応用して、さらに面白い機能を追加してみましょう。

- **WAVファイルへの保存と読み込み**:
  `scipy`ライブラリを使えば、録音した音声をWAVファイルとして保存したり、既存のWAVファイルを読み込んで加工したりできます。
  ```python
  from scipy.io.wavfile import write, read
  # write("output.wav", fs, myrecording)
  # samplerate, data = read("input.wav")
  ```

- **MP3への変換**:
  環境構築でインストールした`ffmpeg`をPythonから呼び出して、WAVファイルをMP3に変換できます。
  ```python
  import subprocess
  # subprocess.run(["ffmpeg", "-i", "input.wav", "output.mp3"])
  ```

- **周波数分析 (FFT)**:
  `numpy.fft`モジュールを使うと、音を周波数成分に分解できます。これにより、「ドレミ」のような音の高さ（ピッチ）を検出したり、特定の周波数帯を強調／抑制するイコライザーのようなエフェクトを実装したりできます。