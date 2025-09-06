# PCで学ぶ！Python音声処理入門【完全版】

## 1. はじめに

このドキュメントは、特別なハードウェアを使わず、お手元のPCとPythonを使って音声処理の基本を学ぶための入門ガイドです。マイクからの録音、スピーカーでの再生、そして録音した音声データの加工といった一連の流れを、理論と実践を交えながら体験することを目指します。

---

## 2. 環境構築

### 手順1: リポジトリのクローン
```bash
git clone https://github.com/your-username/your-repository-name.git # あなたのリポジトリURLに書き換えてください
cd your-repository-name
```

### 手順2: 必要なツールのインストール (Ubuntuの場合)
```bash
sudo apt update
sudo apt install -y build-essential cmake python3-pip python3-venv libportaudio2 portaudio19-dev open-jtalk open-jtalk-mecab-naist-jdic ffmpeg wget unzip
```

### 手順3: Python環境のセットアップ
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 手順4: 音声モデルのダウンロード (Vosk)
音声認識に使用するVoskの日本語モデルをダウンロードします。
```bash
wget https://alphacephei.com/vosk/models/vosk-model-ja-0.22.zip
unzip -o vosk-model-ja-0.22.zip -d models/vosk/
mv models/vosk/vosk-model-ja-0.22 models/vosk/ja-0.22
rm vosk-model-ja-0.22.zip
```

---

## 3. 音声データの基本（理論編）

音は空気の振動、つまり連続的な波（アナログ信号）です。しかし、コンピュータは0と1の集まり（デジタル信号）しか扱えません。音声処理の第一歩は、このアナログな音の波を、コンピュータが理解できる数値の列に変換する「**アナログ-デジタル変換 (A/D変換)**」です。

この変換は、主に2つのステップで行われます。

1.  **サンプリング（標本化）**: 時間軸のデジタル化
2.  **量子化**: 振幅軸のデジタル化

*（イメージ: 滑らかなアナログ波から、カクカクしたデジタル波へ変換される様子）*

### サンプリング周波数 (Sample Rate)
サンプリングとは、音の波を**一定の時間間隔で区切り、その瞬間の波の高さ（振幅）を記録していく**作業です。この「1秒間に何回記録するか」という頻度を**サンプリング周波数**（単位: Hz）と呼びます。
-   **例**: 44100 Hz（CD音質）は、1秒間の音を44,100個の点として記録することを意味します。

### 量子化ビット深度 (Bit Depth)
量子化とは、サンプリングで記録した各点の**波の高さ（振幅）を、どれだけ細かい段階で表現するか**を決める作業です。この細かさの度合いを**量子化ビット深度**（単位: bit）と呼びます。
-   **例**: 16 bitの場合、音の振幅を $2^{16}$ = 65,536段階の数値で表現できます。

### チャンネル数 (Channels)
-   **モノラル (1ch)**: 1つのマイクで録音した単一の音声データです。
-   **ステレオ (2ch)**: 左右2つのマイクで録音した音声データで、立体感が生まれます。

### PCMとWAV形式
このようにしてサンプリング・量子化された、加工されていない生のデジタル音声データを **PCM (Pulse-Code Modulation)** と呼びます。
そして、**WAVファイル**とは、このPCMデータに「サンプリング周波数: 44100Hz」などのメタ情報（ヘッダ）を付け加えて、一つのファイルとして保存したものです。

### なぜNumpy配列なのか？
Pythonの音声処理ライブラリは、音声データを**Numpy配列**という形式でやり取りします。これは、Numpy配列が巨大な数値のリスト（まさにPCMデータ）を高速かつ効率的に計算（エフェクト処理、分析など）するのに非常に優れているためです。

---

## 4. 実践スクリプト解説

各スクリプトの目的と、主要なライブラリの役割について解説します。

- **各ライブラリやツールの詳細**: [`LIBRARIES_GUIDE.md`](./LIBRARIES_GUIDE.md) を参照してください。
- **各スクリプトのコード全文と詳細な解説**: [`CODE_GUIDE.md`](./CODE_GUIDE.md) を参照してください。

### **practice_1_record_playback.py**: 基本的な録音と再生
`sounddevice`ライブラリを使用し、音声の録音と再生を行います。`sounddevice`はNumpy配列を直接扱え、遅延も少ないため、このハンズオンの基本となります。

**実行方法:**
```bash
# 5秒間録音して再生
python practice_1_record_playback.py

# WAVファイルを指定して再生
python practice_1_record_playback.py -f stage_clear.wav
```

### **practice_2_visualize.py / practice_2b_spectrogram.py**: 音声の可視化
`matplotlib`を使い、音声波形やスペクトログラム（声紋）を画像として表示します。これにより、音声がどのような特徴を持っているかを視覚的に確認できます。

**実行方法:**
```bash
# 録音した音声の「波形」を表示
python practice_2_visualize.py

# WAVファイルの「スペクトログラム」を表示
python practice_2b_spectrogram.py -f my_voice.wav
```

### **practice_3_effects.py**: 音声エフェクト
Numpy配列の数値計算機能を使って、音声データに直接エフェクトをかけます。配列の値を2倍すれば音量が上がり、配列の順序を逆にすれば逆再生になります。

**実行方法:**
```bash
# 録音した音声にエフェクトを適用
python practice_3_effects.py

# WAVファイルを指定してエフェクトを適用
python practice_3_effects.py -f stage_clear.wav
```

### **practice_4_wav.py**: WAVファイルへの保存
`scipy.io.wavfile.write`を使い、録音したPCMデータ（Numpy配列）にヘッダ情報を付与して、WAVファイルとして保存します。

**実行方法:**
```bash
# 録音して my_voice.wav に保存
python practice_4_wav.py

# 録音して a.wav に保存
python practice_4_wav.py -o a.wav
```

### **practice_5_tts.py**: テキスト読み上げ (Open JTalk)
`pyopenjtalk`は、日本語のテキストを音声に変換するオフラインの音声合成ライブラリです。PC上で完結するため高速に動作し、複数の話者（ボイスフォント）を切り替えることができます。

**実行方法:**
```bash
python practice_5_tts.py
```

### **practice_6_stt.py**: 音声認識 (Vosk)
`vosk`は、オフラインで動作する音声認識ライブラリです。ダウンロードした言語モデルを使い、マイク入力や音声ファイルから日本語のテキストを生成します。

**実行方法:**
```bash
# 録音して音声認識
python practice_6_stt.py

# WAVファイルを指定して音声認識
python practice_6_stt.py -f my_voice.wav
```

### **practice_7_converter.py**: フォーマット変換 (ffmpeg)
`ffmpeg`は、動画や音声のフォーマットを変換するための非常に強力なコマンドラインツールです。Pythonの`subprocess`モジュールから`ffmpeg`を呼び出し、WAVファイルをMP3に変換します。

**実行方法:**
```bash
python practice_7_converter.py
```

### **practice_8_gtts.py**: テキスト読み上げ (Google)
`gTTS`は、Googleのオンライン音声合成APIを利用するためのライブラリです。インターネット接続が必要ですが、非常に自然で高品質な音声を生成できます。

**実行方法:**
```bash
python practice_8_gtts.py
```

### **practice_9_pyworld_voicemod.py**: ボイスチェンジャー (PyWorld)
`PyWorld`は、音声を「声の高さ(F0)」「声色（スペクトル包絡）」「息遣い（非周期性指標）」の3要素に分解し、それらを再合成できる強力な音声分析・合成ライブラリです。ここではF0を直接操作することで、声のピッチを自在に変更します。

**実行方法:**
```bash
# my_voice.wav のピッチを1.5倍にして my_voice_mod.wav に保存
python practice_9_pyworld_voicemod.py

# ファイルとピッチを指定して実行
python practice_9_pyworld_voicemod.py -i stage_clear.wav -o high_pitch.wav --f0_rate 0.8
```