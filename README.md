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
