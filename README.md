# PCで学ぶ！Python音声処理入門

## 1. はじめに

このドキュメントは、特別なハードウェアを使わず、お手元のPCとPythonを使って音声処理の基本を学ぶための入門ガイドです。マイクからの録音、スピーカーでの再生、そして録音した音声データの加工といった一連の流れを、理論と実践を交えながら体験することを目指します。

### このガイドで学べること
- 音声がデジタルデータになる仕組み（サンプリング、PCM）
- Pythonを使ったPCの音声入出力（録音・再生）
- 音声データの正体である「NumPy配列」の操作
- 音声の視覚化（波形表示）
- 音声の加工（音量調整、逆再生、速度変更）

---

## 2. 音声データの基本（理論編）

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
- **16 bit**: 波の高さを $2^{16}$ = 65,536段階で表現します。非常に一般的で十分な品質です。
- **24 bit / 32 bit**: より高い解像度を持ち、プロのレコーディングなどで使われます。
- **float32**: このガイドで使うデータ型。-1.0から1.0までの浮動小数点数で高さを表現し、非常に扱いやすい形式です。

### チャンネル (Channels)
音源の数を指します。
- **1 (モノラル)**: すべての音が1つのチャンネルにまとめられています。
- **2 (ステレオ)**: 左右2つのチャンネルを持ち、音の広がりや定位を表現できます。

### PCM (Pulse-Code Modulation)
上記の一連の処理（サンプリング→量子化）を経て作られた、**生のデジタル音声データ**のことを**PCMデータ**と呼びます。私たちがこれからPythonで扱うのは、まさにこのPCMデータです。

---

## 3. 環境構築

PCで音声処理を始めるために、必要なPythonライブラリをインストールします。

```bash
pip install sounddevice numpy matplotlib
```
上記のコマンドをターミナル（WindowsならコマンドプロンプトやPowerShell）で実行してください。

---

## 4. ライブラリの詳細な役割

今回インストールした3つのライブラリが、それぞれどのような役割を担っているのかを解説します。

### `sounddevice`: PCの音声入出力を担う「窓口」
このライブラリは、PythonプログラムとPCのハードウェア（マイク、スピーカー）との間の橋渡しをします。
- **主な機能**:
    - `sd.rec()`: マイクからの録音を開始します。
    - `sd.play()`: 音声データをスピーカーで再生します。
    - `sd.wait()`: 録音や再生が終わるまでプログラムを待ちます。
    - `sd.query_devices()`: PCに接続されている音声デバイスの一覧を表示します。

### `numpy`: 音声データを格納・計算する「魔法の箱」
`sounddevice`で録音されたPCMデータは、`numpy`の**配列（Array）**という特殊な形式でプログラムに渡されます。
- **なぜNumPyか？**:
    - **高速**: 大量の数値データを非常に高速に計算できます。音声データは数万〜数百万個の数値の集まりなので、これは非常に重要です。
    - **便利**: 配列全体に対して一度に計算（足し算、掛け算など）を適用したり、スライス機能で一部分を切り出したり、逆順にしたりといった操作が非常に簡単です。音声加工は、まさにこのNumPy配列の操作そのものです。

### `matplotlib`: 音声データを視覚化する「グラフ描画ツール」
NumPy配列はただの数値の羅列なので、人間にはそれがどんな音なのか直感的に分かりません。`matplotlib`を使えば、この数値の配列を波形グラフとしてプロットし、視覚的に確認できます。

---

## 5. 実践1: 録音と再生

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
# sd.rec()は、録音が完了するのを待たずに次の行に進む（ノンブロッキング）
# 戻り値は、音声データを格納するNumPy配列
myrecording = sd.rec(int(duration * fs), samplerate=fs, channels=CHANNELS, dtype='float32')

# sd.wait()を呼ぶことで、録音が完了するまでここで待機する
sd.wait()

print("録音終了。")
print(f"録音データの形式: {type(myrecording)}")
print(f"データ型: {myrecording.dtype}")
print(f"形状: {myrecording.shape}") # (サンプル数, チャンネル数) が表示される

# --- 再生 ---
print("録音した音声を再生します...")
sd.play(myrecording, fs)

# 再生が完了するまで待機
sd.wait()

print("再生終了。")
```

---

## 6. 実践2: 音声の可視化（波形表示）

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
# np.linspace(開始, 終了, 要素数)
time = np.linspace(0., duration, myrecording.shape[0])

# matplotlibでグラフを描画
plt.figure(figsize=(10, 4)) # グラフのサイズを指定
plt.plot(time, myrecording)
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.title("Waveform")
plt.grid(True) # グリッド線を表示
plt.show() # グラフを表示
```
このコードを実行すると、横軸が時間、縦軸が音の振幅（波の高さ）のグラフが表示されます。大きな声を出した部分では、波の振れ幅が大きくなっているのが確認できるはずです。

---

## 7. 実践3: 音声データの加工

いよいよ音声加工です。録音したNumPy配列を直接操作して、音にエフェクトをかけてみましょう。

**サンプルコード:**
```python
# practice_3_effects.py
import sounddevice as sd
import numpy as np

# --- 録音 (実践1と同じ) ---
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
# 配列の全要素を2倍することで、振幅が2倍になり、音量が大きくなる
louder_audio = myrecording * 2.0
# 配列の全要素を0.5倍することで、振幅が半分になり、音量が小さくなる
quieter_audio = myrecording * 0.5

print("\n[2] 音量を大きくして再生します。")
sd.play(louder_audio, fs)
sd.wait()

print("\n[3] 音量を小さくして再生します。")
sd.play(quieter_audio, fs)
sd.wait()
# 注意: 音量を大きくしすぎると音割れ（クリッピング）の原因になります。

# --- 加工2: 逆再生 ---
# NumPyのスライス機能 [::-1] を使って配列の順序をすべて逆にする
reversed_audio = myrecording[::-1]

print("\n[4] 逆再生します。")
sd.play(reversed_audio, fs)
sd.wait()

# --- 加工3: 速度を変更する ---
# 再生時のサンプリング周波数を変えることで、再生速度が変わる
speed_factor_fast = 1.5  # 1.5倍速
speed_factor_slow = 0.7  # 0.7倍速

print(f"\n[5] {speed_factor_fast}倍速で再生します。（音が高くなる）")
sd.play(myrecording, int(fs * speed_factor_fast))
sd.wait()

print(f"\n[6] {speed_factor_slow}倍速で再生します。（音が低くなる）")
sd.play(myrecording, int(fs * speed_factor_slow))
sd.wait()

print("\nすべての再生が完了しました。")
```

---

## 8. 次のステップへ

このガイドでは、音声処理の入り口を学びました。ここからさらに発展させるためのアイデアをいくつか紹介します。

- **WAVファイルへの保存と読み込み**:
  `scipy`ライブラリを使えば、録音した音声をWAVファイルとして保存したり、既存のWAVファイルを読み込んで加工したりできます。
  ```python
  # pip install scipy
  from scipy.io.wavfile import write, read

  # 保存
  write("output.wav", fs, myrecording)

  # 読み込み
  samplerate, data = read("input.wav")
  ```

- **周波数分析 (FFT)**:
  `numpy.fft`モジュールを使うと、音を周波数成分に分解できます。これにより、「ドレミ」のような音の高さ（ピッチ）を検出したり、特定の周波数帯を強調／抑制するイコライザーのようなエフェクトを実装したりできます。

- **より高度なエフェクト**:
  ディレイ、リバーブ、コーラスといったエフェクトも、すべてはNumPy配列の巧妙な操作によって実現されています。ぜひ挑戦してみてください。

---

## 9. 実践4: テキストからの音声合成 (pyopenjtalk)

これまではマイクから入力した音声を扱ってきましたが、今度はプログラム自身に喋らせてみましょう。ここでは、テキストを音声に変換する**音声合成（Text-To-Speech, TTS）**を扱います。

### `pyopenjtalk` とは？
`pyopenjtalk`は、`Open JTalk`というオープンソースの日本語音声合成エンジンをPythonから簡単に使えるようにしたライブラリです。最大の特徴は、**インターネット接続が不要（オフライン）**で動作することと、無料で利用できる点です。

### インストール
`pyopenjtalk`は他のライブラリと少し依存関係が複雑なため、以下のコマンドで関連ライブラリごとインストールするのが確実です。

```bash
pip install pyopenjtalk sounddevice
```
*(sounddeviceは既にインストール済みですが、念のため含めています)*

### 使い方
`pyopenjtalk`は、与えられた日本語テキストをPCMデータ（NumPy配列）に変換してくれます。つまり、`sounddevice`で録音したデータと全く同じ形式のデータが、今度はテキストから生成されるわけです。

**サンプルコード:**
```python
# practice_4_tts.py
import pyopenjtalk
import sounddevice as sd

# 合成したい日本語テキスト
text = "こんにちは。今日はPythonで音声合成を試しています。"

print(f"音声合成中: 「{text}」")

# テキストから音声波形 (NumPy配列) を生成
# 戻り値は (音声波形データ, サンプリング周波数)
audio_data, sampling_rate = pyopenjtalk.tts(text)

print(f"生成された音声のサンプリング周波数: {sampling_rate} Hz")

# sounddeviceで再生
print("再生します...")
sd.play(audio_data, sampling_rate)
sd.wait()
print("再生完了。")
```

---

## 10. 実践5: 音声認識 (Vosk)

最後に、このガイドの締めくくりとして、マイクで話した言葉をコンピュータに理解させる**音声認識（Speech-To-Text, STT）**に挑戦します。

### `Vosk` とは？
`Vosk`は、`pyopenjtalk`と同じくオフラインで動作する、高精度なオープンソースの音声認識エンジンです。日本語を含む多くの言語に対応しており、カスタマイズも可能です。

### インストール
`vosk`ライブラリをインストールします。

```bash
pip install vosk
```

### 【重要】音声認識モデルの準備
`Vosk`は、それ単体では音声を認識できません。「どの言語を認識するのか」を定義した**モデルファイル**が別途必要になります。

1.  **モデルのダウンロード**:
    以下の公式サイトから、日本語モデルをダウンロードします。
    - **Vosk Models Page**: [https://alphacephei.com/vosk/models](https://alphacephei.com/vosk/models)
    - `vosk-model-ja-0.22` のような、日本語用のモデル（zipファイル）を見つけてダウンロードしてください。（ファイルサイズが1GB以上あるので注意してください）

2.  **モデルの配置**:
    ダウンロードしたzipファイルを解凍し、出てきたフォルダ（例: `vosk-model-ja-0.22`）を、これから作成するPythonスクリプトと同じ階層に置いてください。

### 使い方
音声認識は、以下のステップで行います。
1.  マイクから音声を録音する。
2.  録音したデータをVoskが要求する形式に変換する。
3.  変換したデータをVoskに渡して、認識結果（テキスト）を受け取る。

**サンプルコード:**
```python
# practice_5_stt.py
import sounddevice as sd
import numpy as np
from vosk import Model, KaldiRecognizer
import json
import os

# --- パラメータ設定 ---
MODEL_DIR = "vosk-model-ja-0.22"  # ★配置したモデルのディレクトリ名
FS = 16000  # サンプリング周波数 (Voskの日本語モデルは16000Hzを推奨)
DURATION = 5  # 録音時間 (秒)
CHANNELS = 1 # チャンネル数

# --- モデルの存在チェック ---
if not os.path.exists(MODEL_DIR):
    print(f"エラー: Voskモデルのディレクトリ '{MODEL_DIR}' が見つかりません。")
    print("公式サイトからモデルをダウンロードし、このスクリプトと同じ階層に配置してください。")
    exit()

# --- 録音 ---
print(f"{DURATION}秒間、何か話してください...")
myrecording = sd.rec(int(DURATION * FS), samplerate=FS, channels=CHANNELS, dtype='float32')
sd.wait()
print("録音終了。")

# --- Voskの準備 ---
model = Model(MODEL_DIR)
recognizer = KaldiRecognizer(model, FS)

# --- データ形式の変換 & 認識 ---
# sounddeviceで録音したfloat32形式のNumPy配列を、
# Voskが要求する16bit整数のbytes形式に変換する
data = (myrecording * 32767).astype(np.int16).tobytes()

if recognizer.AcceptWaveform(data):
    # 最後の認識結果を取得
    result = json.loads(recognizer.Result())
    recognized_text = result.get('text', '')
    print(f"\n--- 認識結果 ---")
    if recognized_text:
        print(recognized_text)
    else:
        print("（何も認識できませんでした）")
else:
    # 部分的な認識結果も表示する場合
    partial_result = json.loads(recognizer.PartialResult())
    print(f"\n--- 部分的な認識結果 ---")
    print(partial_result.get('partial', ''))

```

#### コードのポイント
- **サンプリング周波数**: 音声認識では、一般的に16000Hzが使われます。Voskのモデルも16000Hzで学習されているため、録音時から`FS = 16000`に設定しています。
- **データ形式の変換**: `sounddevice`は-1.0〜1.0の`float32`形式でデータを返しますが、Voskは-32768〜32767の`int16`形式のデータを期待します。そのため、`myrecording * 32767`でスケールを合わせ、`.astype(np.int16)`で型を変換し、`.tobytes()`で最終的にbytesオブジェクトに変換しています。この変換処理が非常に重要です。

これで、音声の入力・加工・出力、そして音声合成・音声認識という一通りの音声処理をPC上で体験することができました。