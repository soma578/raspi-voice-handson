# PCで学ぶ！Python音声処理入門【決定版】

## 1. はじめに

このドキュメントは、特別なハードウェアを使わず、お手元のPC（Windows）とPythonを使って音声処理の基本を学ぶための入門ガイドです。マイクからの録音、スピーカーでの再生、そして録音した音声データの加工といった一連の流れを、理論と実践を交えながら体験することを目指します。

このガイドは、各章で登場する技術やライブラリを、実際に使いながらその都度詳しく学んでいく「実践中心」の構成になっています。

---

## 2. クイックスタート: 環境構築

まず、このガイドで必要になるツールをすべてPCにセットアップします。ここでの詳しい説明は各実践の章に譲り、ひとまずインストール作業を完了させましょう。

### 手順1: Pythonライブラリの一括インストール

以下のコマンドを、お使いのPCのターミナル（コマンドプロンプトやPowerShell）にコピー＆ペーストして実行してください。

```bash
pip install sounddevice numpy matplotlib scipy pyopenjtalk vosk
```

### 手順2: 外部ツール `ffmpeg` のインストール

`ffmpeg`は、音声や動画のフォーマットを変換するための非常に強力な外部ツールです。後の章でWAVファイルをMP3に変換する際に使います。

1.  **ダウンロード**: [ffmpeg.orgのダウンロードページ](https://ffmpeg.org/download.html)にアクセスし、Windowsロゴからリンクされている`gyan.dev`などのサイトから、`release`ビルドの`full`版（例: `ffmpeg-release-full.7z`）をダウンロードします。
2.  **配置**: ダウンロードした圧縮ファイルを解凍し、中身のフォルダを`C:\ffmpeg`のような分かりやすい場所に配置します。
3.  **環境変数「PATH」の設定**: Windowsの検索バーで「**環境変数を編集**」と検索し、「システム環境変数の編集」を開きます。「環境変数」→「システム環境変数」の`Path`を選択→「編集」→「新規」と進み、`ffmpeg`の`bin`フォルダのパス（例: `C:\ffmpeg\bin`）を追加します。
4.  **確認**: **新しい**コマンドプロンプトを開き`ffmpeg -version`と入力し、バージョン情報が表示されれば成功です。

### 手順3: 音声認識モデル `Vosk` の準備

`Vosk`で音声認識を行うには、言語ごとの「モデル」ファイルが必要です。

1.  **ダウンロード**: [Vosk Models Page](https://alphacephei.com/vosk/models)にアクセスし、日本語モデル（`vosk-model-ja-0.22`など）をダウンロードします。
2.  **配置**: ダウンロードしたzipファイルを解凍し、出てきたフォルダを、この先のPythonスクリプトを保存する予定のプロジェクトフォルダ内に配置してください。

---

## 3. 音声データの基本（理論編）

（この章は、音声処理の背景にある普遍的な理論を扱います。一度目を通しておくと、実践パートの理解が深まります。）

音は空気の振動（アナログ信号）ですが、コンピュータは数値（デジタル信号）しか扱えません。この変換プロセスが「**A/D変換**」であり、その核心が**サンプリング（標本化）**と**量子化**です。

- **サンプリング周波数 (Hz)**: 1秒間に音を何回サンプリング（測定）するか。数値が大きいほど高音質になります。(例: CDは44100 Hz)
- **ビット深度 (bit)**: 1回のサンプリングで得た音の大きさ（振幅）を、どれくらいの細かさで数値化するか。数値が大きいほど表現豊かな音になります。(例: 16 bitなら$2^{16}$=65,536段階)
- **チャンネル数**: モノラル(1)かステレオ(2)か。

このプロセスを経て生成された、生の音声データが **PCM (Pulse-Code Modulation)** データです。私たちがPythonで扱うのは、このPCMデータを`numpy`配列という形式にしたものです。

---

## 4. 実践1: 録音と再生

最初の実践として、PCのマイクから音を録音し、スピーカーで再生してみましょう。

### この実践で使うモジュール

#### `sounddevice` 詳解
- **役割**: PythonとPCの音声入出力デバイス（マイク、スピーカー）を繋ぐためのライブラリです。内部的には**PortAudio**という、様々なOSで音声処理を行うための標準的なライブラリを呼び出しています。これにより、私たちはOSやハードウェアの違いを気にせず、同じコードで音声を扱うことができます。
- **主要な関数**:
    - `rec(フレーム数, samplerate, channels)`: 録音を開始します。この関数は「ノンブロッキング」で、録音が完了するのを待たずに即座に次の処理へ進みます。戻り値として、録音データを格納するためのNumPy配列を返します。
    - `play(データ, samplerate)`: NumPy配列のデータを再生します。これもノンブロッキングです。
    - `wait()`: `rec`や`play`といった処理が完了するのを待つための「ブロッキング」関数です。これを呼ばないと、録音や再生が終わる前にプログラムが終了してしまいます。
    - `query_devices()`: PCに接続されている音声デバイスの一覧と情報を表示します。どのマイクやスピーカーが何番のデバイスとして認識されているかを確認するのに便利です。

#### `numpy` 詳解
- **役割**: 数値計算を効率的に行うためのライブラリで、PythonにおけるデータサイエンスやAI分野の根幹をなす存在です。音声データは「数値の配列」そのものであるため、`numpy`の配列（`ndarray`）として扱うのが最も効率的です。
- **なぜNumPyか？**: Python標準のリストに比べて、`numpy`の配列はメモリ効率が良く、配列全体に対する計算（**ベクトル化演算**）が非常に高速です。例えば、音声データ全体の音量を2倍にする場合、リストならループ処理が必要ですが、`numpy`なら配列に`* 2`と書くだけで、最適化されたC言語レベルの速度で実行されます。
- **重要な属性**:
    - `.shape`: 配列の形状。(サンプル数, チャンネル数)の形で格納されています。
    - `.dtype`: 配列のデータ型。`float32`（-1.0〜1.0の浮動小数点数）や`int16`（-32768〜32767の整数）などがよく使われます。

### サンプルコード

```python
# practice_1_record_playback.py
import sounddevice as sd
import numpy as np

# デバイス一覧を表示して確認
# print(sd.query_devices())

# パラメータ設定
FS = 44100  # サンプリング周波数
DURATION = 5  # 録音時間 (秒)

print(f"{DURATION}秒間、録音します...")

# 録音
myrecording = sd.rec(int(DURATION * FS), samplerate=FS, channels=1)
sd.wait()  # 録音終了まで待機

print("録音終了。")
print(f"データ型: {myrecording.dtype}, 形状: {myrecording.shape}")

# 再生
print("再生します...")
sd.play(myrecording, FS)
sd.wait()  # 再生終了まで待機

print("再生完了。")
```

---

## 5. 実践2: 音声の可視化

録音した音声データがどんな形をしているのか、グラフにして見てみましょう。

### この実践で使うモジュール

#### `matplotlib` 詳解
- **役割**: `numpy`配列などのデータを、グラフや画像として可視化するための標準的なライブラリです。
- **基本要素**: `matplotlib`のグラフは、大きな画用紙である`Figure`と、その上に描かれる個々のグラフ領域である`Axes`（軸）から構成されます。`plt.plot()`のようなシンプルな関数は、内部で自動的にこれらを作成して描画しています。
- **音声波形プロット**: 横軸を「時間」、縦軸を`numpy`配列の各値（音の振幅）としてプロットすることで、音声の波形を描画できます。これにより、どこで音が大きくなり、どこが無音なのかを視覚的に把握できます。

### サンプルコード

```python
# practice_2_visualize.py
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt

FS = 44100
DURATION = 5

print("5秒間録音します...")
myrecording = sd.rec(int(DURATION * FS), samplerate=FS, channels=1)
sd.wait()
print("録音終了。")

# 時間軸を作成
time = np.arange(0, DURATION, 1/FS)

# グラフを描画
plt.figure(figsize=(12, 4))
plt.plot(time, myrecording)
plt.xlabel("Time [s]")
plt.ylabel("Amplitude")
plt.title("Waveform")
plt.grid()
plt.show()
```

---

## 6. 実践3: 音声データの加工

`numpy`の配列操作を駆使して、音声に様々なエフェクトをかけてみましょう。

### `numpy`配列操作の深掘り

- **音量変更（要素ごとの乗算）**: 配列全体に数値を掛けるだけで、全サンプルの振幅が変わり、音量が変化します。 `audio * 2` で音量2倍、 `audio * 0.5` で音量半分です。
- **逆再生（スライス）**: `[::-1]`というスライス表記は、配列の要素を逆順にします。これを音声データに適用すると、逆再生になります。
- **音声の結合（`concatenate`）**: `np.concatenate()` を使うと、複数の音声配列を連結できます。例えば、ある音声の後に1秒間の無音を挟んで別の音声を繋ぐ、といった編集が可能です。
- **無音の生成（`zeros`）**: `np.zeros(サンプル数)` で、値がすべて0の配列（＝無音データ）を簡単に作成できます。

### サンプルコード

```python
# practice_3_effects.py
import sounddevice as sd
import numpy as np

FS = 44100
DURATION = 3

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
one_sec_silence = np.zeros((FS * 1, 1), dtype=myrecording.dtype)
combined_audio = np.concatenate([myrecording, one_sec_silence, myrecording])
sd.play(combined_audio, FS); sd.wait()
```

---

## 7. 実践4: ファイルへの保存と読込

録音した音声をWAVファイルとして保存し、またそれを読み込んで再生する方法を学びます。

### この実践で使うモジュール

#### `scipy.io.wavfile` 詳解
- **役割**: `scipy`は科学技術計算全般を扱う巨大なライブラリですが、その中にある`io.wavfile`は、WAVファイルの読み書きに特化したモジュールです。
- **WAVフォーマット**: 非圧縮のPCMデータを格納する標準的な音声ファイル形式です。ファイルの先頭に「サンプリング周波数、ビット深度、チャンネル数」などの情報を持つ**ヘッダ**があり、その後に実際の音声データが続きます。
- **`write(ファイル名, samplerate, データ)`**: サンプリング周波数とNumPy配列データを指定して、WAVファイルを作成します。この際、`float32`のデータは自動的にWAV形式で一般的な`int16`などに変換して書き込んでくれます。
- **`read(ファイル名)`**: WAVファイルを読み込み、ヘッダから取得したサンプリング周波数と、音声データ本体のNumPy配列を返します。

### サンプルコード

```python
# practice_4_wav.py
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write, read

FS = 44100
DURATION = 5
FILENAME = "my_voice.wav"

# 録音してWAVファイルに保存
print(f"録音開始... ({FILENAME}に保存)")
recording = sd.rec(int(DURATION * FS), samplerate=FS, channels=1)
sd.wait()
write(FILENAME, FS, recording)
print("保存完了。")

# WAVファイルを読み込んで再生
print(f"{FILENAME}を読み込んで再生します...")
samplerate, data = read(FILENAME)
print(f"読み込んだファイルの周波数: {samplerate} Hz")
sd.play(data, samplerate)
sd.wait()
print("再生完了。")
```

---

## 8. 実践5: テキストからの音声合成

日本語テキストから音声を生成します。

### この実践で使うモジュール

#### `pyopenjtalk` 詳解
- **役割**: `Open JTalk`という日本語音声合成エンジンをPythonから呼び出すためのライブラリです。
- **`tts(テキスト)`**: `tts`はText-To-Speechの略。与えられた日本語文字列を解析し、対応する音声波形のNumPy配列を生成して返します。戻り値は `(音声データ, サンプリング周波数)` のタプルです。サンプリング周波数が一緒に返されるのは、`Open JTalk`が内部で持つ音声モデルの周波数（例: 48000 Hz）でデータが生成されるため、再生時に正しい周波数を指定する必要があるからです。

### サンプルコード

```python
# practice_5_tts.py
import pyopenjtalk
import sounddevice as sd

text = "こんにちは。こちらは、オープンソースの日本語音声合成エンジン、オープンＪトークです。"

print(f"音声合成中...: 「{text}」")
audio_data, FS = pyopenjtalk.tts(text)

print(f"再生します... (周波数: {FS} Hz)")
sd.play(audio_data, FS)
sd.wait()
print("再生完了。")
```

---

## 9. 実践6: 音声認識

マイクで話した内容をテキストに変換します。

### この実践で使うモジュール

#### `vosk` 詳解
- **役割**: オフラインで動作する音声認識エンジン`Vosk`をPythonから利用するためのライブラリです。
- **主要クラス**:
    - `Model(モデルパス)`: 環境構築で配置した言語モデル（例: `vosk-model-ja-0.22`）を読み込み、認識の準備をします。
    - `KaldiRecognizer(モデル, samplerate)`: 認識処理の本体。どのモデルと、どのサンプリング周波数で音声を解析するかを指定して作成します。
- **データ形式の重要性**: `Vosk`は、-1.0〜1.0の`float32`形式ではなく、-32768〜32767の**`int16`形式のPCMデータをbytes列にしたもの**を要求します。そのため、`sounddevice`で録音した`float32`の配列に対し、`* 32767`で振幅をスケールアップし、`.astype(np.int16)`で整数に変換、`.tobytes()`でbytes列に変換する、という前処理が不可欠です。
- **認識結果(JSON)**: `recognizer.Result()`は、認識結果をJSON形式の文字列で返します。`json.loads()`でパースすると、`'text'`キーに認識された全文が、`'result'`キーには単語ごとの認識結果やタイムスタンプ、信頼度(`'conf'`)などが含まれています。

### サンプルコード

```python
# practice_6_stt.py
import sounddevice as sd
import numpy as np
from vosk import Model, KaldiRecognizer
import json
import os

MODEL_DIR = "vosk-model-ja-0.22"
FS = 16000  # 日本語モデルは16000Hzを推奨
DURATION = 5

if not os.path.exists(MODEL_DIR):
    print("Voskモデルが見つかりません。")
    exit()

print(f"{DURATION}秒間、話してください...")
myrecording = sd.rec(int(DURATION * FS), samplerate=FS, channels=1, dtype='float32')
sd.wait()
print("認識中...")

model = Model(MODEL_DIR)
recognizer = KaldiRecognizer(model, FS)

# データ形式を変換して認識
data = (myrecording * 32767).astype(np.int16).tobytes()
recognizer.AcceptWaveform(data)

result = json.loads(recognizer.FinalResult())
print("--- 認識結果 ---")
print(result['text'])
```

---

## 10. 実践7: フォーマット変換

作成したWAVファイルを、より一般的なMP3ファイルに変換してみましょう。

### 外部ツールとの連携

#### `subprocess`モジュール詳解
- **役割**: Pythonプログラムの中から、OSのコマンド（外部プログラム）を実行するための標準ライブラリです。`ffmpeg.exe`のような、独立したプログラムを呼び出すのに使います。
- **`run(コマンドリスト)`**: 指定されたコマンドを実行します。コマンドと引数は、`["ffmpeg", "-i", "input.wav", "output.mp3"]`のようにリストで渡すのが安全で確実です。

#### `ffmpeg`コマンド詳解
- **役割**: 音声・動画に関するあらゆる変換処理を行える万能ツールです。
- **主要オプション**:
    - `-i <入力ファイル>`: 変換元のファイルを指定します。
    - `<出力ファイル>`: 変換先のファイル名を指定します。拡張子（`.mp3`など）を見るだけで、`ffmpeg`が自動的に適切なフォーマットに変換してくれます。
    - `-b:a <ビットレート>`: 音声のビットレートを指定します。MP3の場合、`192k`（192kbps）あたりが標準的な音質です。

### サンプルコード

```python
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

```

---

## 11. まとめ

このガイドでは、音声処理の基本的な理論から、Pythonを使った録音・再生・加工・ファイル操作、さらには音声合成・認識、フォーマット変換まで、一通りの技術を実践的に学びました。ここで得た知識を組み合わせることで、文字起こしツール、ボイスアシスタント、オーディオエフェクターなど、様々なアプリケーションを作成する基礎ができたはずです。ぜひ、自分だけの音声アプリケーション開発に挑戦してみてください。
