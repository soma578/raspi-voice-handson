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

# --- 説明 ---
# このスクリプトは、音声を録音して再生するか、指定されたWAVファイルを再生します。
# コマンドラインから -f (または --file) オプションでWAVファイルを指定できます。
# 例: python practice_1_record_playback.py -f my_voice.wav
# 引数なしで実行すると、5秒間の録音を行います。
# 詳細は -h オプションで確認してください。
# ----------

# コマンドライン引数の設定
parser = argparse.ArgumentParser(description="Record audio or play a WAV file.")
parser.add_argument("-f", "--file", type=str, help="Path to the WAV file to play.")
args = parser.parse_args()

# パラメータ設定
FS = 44100  # サンプリング周波数
DURATION = 5  # 録音時間 (秒)

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
    # デバイス一覧を表示して確認
    # print(sd.query_devices())

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

### 解説
1.  **`argparse`**: コマンドラインで `-f` オプションを受け付けるために使用します。
2.  **`args.file`のチェック**: `-f` でファイルが指定されていれば、`soundfile.read()` (sf.read) でそのファイルを読み込みます。指定されていなければ、`sounddevice.rec()` (sd.rec) で録音を開始します。
3.  **`sd.rec()`**: `(録音時間 * サンプリング周波数)` で録音する総サンプル数を計算し、録音を実行します。戻り値は音声データをNumpy配列として格納したものです。
4.  **`sd.wait()`**: 録音や再生が完了するまで、プログラムの実行を一時停止します。
5.  **`sd.play()`**: Numpy配列として格納された音声データを、指定されたサンプリング周波数で再生します。

---

## `practice_2_visualize.py`

### 役割
音声データを時間軸の波形としてグラフにプロット（可視化）します。

### コード全文
```python
# practice_2_visualize.py
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt
import argparse
import soundfile as sf

# (argparseによる引数処理部分は practice_1 と同様)
# ...

if args.file:
    # ...
else:
    # ...

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

### 解説
1.  **`np.arange(0, DURATION, 1/FS)`**: グラフのX軸（時間軸）を作成します。`0`秒から`DURATION`秒まで、`1/FS`秒（1サンプルあたりの時間）刻みの配列を生成します。
2.  **`plt.plot(time, myrecording)`**: `matplotlib`を使い、X軸を`time`、Y軸を音声データの振幅`myrecording`として線グラフをプロットします。
3.  **`plt.show()`**: プロットしたグラフを画面に表示します。

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

# (argparseによる引数処理部分は practice_1 と同様)
# ...

# 1. 音量UP
print("音量を2倍にして再生")
sd.play(myrecording * 2, FS); sd.wait()

# 2. 逆再生
print("逆再生")
sd.play(myrecording[::-1], FS); sd.wait()

# 3. 結合
print("1秒の無音を挟んで2回再生")
one_sec_silence = np.zeros((FS * 1, myrecording.ndim), dtype=myrecording.dtype)
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
```

### 解説
- **音量UP**: Numpy配列全体を `* 2` で2倍します。これにより、すべてのサンプルの振幅が2倍になります。
- **逆再生**: `[::-1]` は、Numpy配列の要素を逆順にするスライス表記です。
- **結合**: `np.zeros()` で無音のNumpy配列を生成し、`np.concatenate()` で複数の配列を連結します。
- **やまびこ**: 配列をコピーし、一定時間（`delay_samples`）ずらした元の音声を、音量を半分（`* 0.5`）にして足し合わせています。

---

## `practice_4_wav.py`

### 役割
録音した音声データをWAVファイルとしてディスクに保存します。

### コード全文
```python
# practice_4_wav.py
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write, read
import argparse

# (argparseで出力ファイル名を指定する部分)
# ...

# 録音してWAVファイルに保存
print(f"録音開始... ({FILENAME}に保存)")
recording = sd.rec(int(DURATION * FS), samplerate=FS, channels=1)
sd.wait()
write(FILENAME, FS, recording)
print("保存完了。")
```

### 解説
- **`from scipy.io.wavfile import write`**: WAVファイルの書き込み機能 `write` をインポートします。
- **`write(FILENAME, FS, recording)`**:
    - `FILENAME`: 出力するファイル名
    - `FS`: サンプリング周波数
    - `recording`: 保存するNumpy配列の音声データ
    - この関数が、PCMデータ（Numpy配列）に適切なヘッダ情報を付与してWAVファイルを作成します。

---

## `practice_6_stt.py`

### 役割
オフライン音声認識ライブラリ `Vosk` を使い、音声データを日本語テキストに変換します。

### コード全文
```python
# practice_6_stt.py
import sounddevice as sd
import numpy as np
from vosk import Model, KaldiRecognizer
import json
import os
import argparse
import soundfile as sf

# (argparseによる引数処理部分は同様)
# ...

# Voskモデルの読み込み
model = Model(MODEL_DIR)
recognizer = KaldiRecognizer(model, FS)

# データ形式を変換して認識
data = (myrecording * 32767).astype(np.int16).tobytes()
recognizer.AcceptWaveform(data)

# 認識結果をJSON形式で取得
result = json.loads(recognizer.FinalResult())
print("--- 認識結果 ---")
print(result['text'])
```

### 解説
1.  **`Model(MODEL_DIR)`**: 事前にダウンロードしたVoskの言語モデルを読み込みます。
2.  **`KaldiRecognizer(model, FS)`**: 読み込んだモデルとサンプリング周波数を指定して、認識器（Recognizer）を作成します。
3.  **`astype(np.int16).tobytes()`**: `sounddevice` が返す `float32` 型のNumpy配列を、Voskが要求する `16bit整数` のバイト列に変換します。
4.  **`recognizer.AcceptWaveform(data)`**: バイト列に変換した音声データを認識器に渡します。
5.  **`recognizer.FinalResult()`**: 認識処理を実行し、結果をJSON形式の文字列で返します。
6.  **`json.loads(...)`**: JSON文字列をPythonの辞書オブジェクトに変換し、`'text'`キーで認識結果の文字列を取り出します。

---

## `practice_9_pyworld_voicemod.py`

### 役割
音声分析合成ライブラリ `PyWorld` を使い、声の高さ（ピッチ）を変更するボイスチェンジャーを実現します。

### コード全文
```python
# practice_9_pyworld_voicemod.py
import soundfile as sf
import pyworld as pw
import numpy as np
import sounddevice as sd
# ... (argparse部分は省略)

# --- PyWorldによる分析 ---
# F0(基本周波数), sp(スペクトル包絡), ap(非周期性指標)に分解
f0, t = pw.dio(x, fs)
sp = pw.cheaptrick(x, f0, t, fs)
ap = pw.d4c(x, f0, t, fs)

# --- パラメータの加工 ---
# 声の高さを変更
modified_f0 = f0 * f0_rate

# --- PyWorldによる再合成 ---
synthesized = pw.synthesize(modified_f0, sp, ap, fs)

# --- 再生と保存 ---
# ...
```

### 解説
1.  **`pw.dio`, `pw.cheaptrick`, `pw.d4c`**: PyWorldの分析関数群です。音声`x`を、声の高さの元となる`f0`（基本周波数）、声色を決める`sp`（スペクトル包絡）、息遣いなどの成分である`ap`（非周期性指標）の3つのパラメータに分解します。
2.  **`modified_f0 = f0 * f0_rate`**: F0（基本周波数）の配列全体を一定倍率で変更します。1.0より大きいと声が高く、小さいと低くなります。
3.  **`pw.synthesize(...)`**: 加工したパラメータ（`modified_f0`など）を元に、音声を再合成します。

