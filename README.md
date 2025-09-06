# PCで学ぶ！Python音声処理入門【完全版】

## 1. はじめに

このドキュメントは、特別なハードウェアを使わず、お手元のPCとPythonを使って音声処理の基本を学ぶための入門ガイドです。マイクからの録音、スピーカーでの再生、そして録音した音声データの加工といった一連の流れを、理論と実践を交えながら体験することを目指します。

このガイドは、各章で登場する技術やライブラリを、実際に使いながらその都度詳しく学んでいく「実践中心」の構成になっています。

---

## 2. 環境構築

### 手順1: リポジトリのクローン
```bash
# このリポジトリのURLに置き換えてください
git clone https://github.com/your-username/your-repository-name.git
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
```bash
wget https://alphacephei.com/vosk/models/vosk-model-ja-0.22.zip
unzip -o vosk-model-ja-0.22.zip -d models/vosk/
mv models/vosk/vosk-model-ja-0.22 models/vosk/ja-0.22
rm vosk-model-ja-0.22.zip
```
これにより、`models/vosk/ja-0.22` というディレクトリにモデルが配置されます。

---
セットアップは以上です。各`practice_..._.py`ファイルを実行して、音声処理を試してみてください。

---

## 3. 音声データの基本（理論編）

音は空気の振動、つまり連続的な波（アナログ信号）です。しかし、コンピュータは0と1の集まり（デジタル信号）しか扱えません。音声処理の第一歩は、このアナログな音の波を、コンピュータが理解できる数値の列に変換する「**アナログ-デジタル変換 (A/D変換)**」です。

この変換は、主に2つのステップで行われます。

1.  **サンプリング（標本化）**: 時間軸のデジタル化
2.  **量子化**: 振幅軸のデジタル化

![Analog to Digital Conversion](https://i.imgur.com/5JjUqGj.png)
*（イメージ図: 滑らかなアナログ波(左)から、カクカクしたデジタル波(右)へ変換される様子）*

### サンプリング周波数 (Sample Rate)

サンプリングとは、音の波を**一定の時間間隔で区切り、その瞬間の波の高さ（振幅）を記録していく**作業です。この「1秒間に何回記録するか」という頻度を**サンプリング周波数**（単位: Hz）と呼びます。

-   **例**: 44100 Hz（CD音質）は、1秒間の音を44,100個の点として記録することを意味します。

この数値が高いほど、元の音の波形をより忠実に再現でき、高音質なデータになります。逆に低すぎると、カクカクした粗い音になります。

### 量子化ビット深度 (Bit Depth)

量子化とは、サンプリングで記録した各点の**波の高さ（振幅）を、どれだけ細かい段階で表現するか**を決める作業です。この細かさの度合いを**量子化ビット深度**（単位: bit）と呼びます。

-   **例**: 16 bitの場合、音の振幅を $2^{16}$ = 65,536段階の数値で表現できます。

ビット深度が大きいほど、小さな音から大きな音までのダイナミックレンジが広がり、より表現力豊かで繊細な音になります。

### チャンネル数 (Channels)

-   **モノラル (1ch)**: 1つのマイクで録音した単一の音声データです。Numpy配列では1次元配列（`[1, 2, 3, ...]`）または N行1列の2次元配列で表現されます。
-   **ステレオ (2ch)**: 左右2つのマイクで録音した音声データです。左右のスピーカーから異なる音を出すことで、立体感や臨場感が生まれます。Numpy配列ではN行2列の2次元配列（`[[L1, R1], [L2, R2], ...]`）で表現されます。

### PCMとWAV形式

このようにしてサンプリング・量子化された、加工されていない生のデジタル音声データを **PCM (Pulse-Code Modulation)** と呼びます。このプロジェクトで扱う音声データは、すべてこのPCM形式です。

そして、**WAVファイル**とは、このPCMデータに「サンプリング周波数: 44100Hz」「ビット深度: 16bit」「チャンネル数: 1」といったメタ情報（ヘッダ）を付け加えて、一つのファイルとして保存したものです。

### なぜNumpy配列なのか？

Pythonで音声データを扱う際、`sounddevice`や`scipy`などのライブラリは、音声データを**Numpy配列**という特殊なデータ形式でやり取りします。これは、Numpy配列が巨大な数値のリスト（まさにPCMデータ）を高速かつ効率的に計算（エフェクト処理、分析など）するのに非常に優れているためです。

このハンズオンでは、**「WAVファイル → Numpy配列 → 加工 → Numpy配列 → WAVファイル/再生」** という一連の流れを体験していきます。

---

## 4. 実践スクリプト一覧

各スクリプトは、コマンドライン引数を指定することで、録音の代わりに既存のWAVファイルを処理できます。引数の詳細は `-h` または `--help` で確認してください。

### **practice_1_record_playback.py**: 録音と再生
引数なしで実行すると音声を録音し、すぐに再生します。
```bash
# 5秒間録音して再生
python practice_1_record_playback.py
```
`-f`オプションでWAVファイルを指定すると、そのファイルを再生します。
```bash
# stage_clear.wav を再生
python practice_1_record_playback.py -f stage_clear.wav
```

### **practice_2_visualize.py**: 波形の可視化
録音した音声、または指定したWAVファイルの波形をグラフで表示します。
```bash
# 録音した音声の波形を表示
python practice_2_visualize.py

# 指定したWAVファイルの波形を表示
python practice_2_visualize.py -f stage_clear.wav
```

### **practice_2b_spectrogram.py**: スペクトログラムの可視化
WAVファイルのスペクトログラム（声紋）を表示します。
```bash
# デフォルトの my_voice.wav のスペクトログラムを表示
python practice_2b_spectrogram.py

# stage_clear.wav のスペクトログラムを表示
python practice_2b_spectrogram.py -f stage_clear.wav
```

### **practice_3_effects.py**: 音声エフェクト
録音または指定したWAVファイルに、音量変更、逆再生、やまびこなどのエフェクトをかけて再生します。
```bash
# 録音した音声にエフェクト
python practice_3_effects.py

# 指定したWAVファイルにエフェクト
python practice_3_effects.py -f stage_clear.wav
```

### **practice_4_wav.py**: WAVファイルへの保存
録音した音声をWAVファイルとして保存します。`-o`オプションで出力ファイル名を指定できます。
```bash
# my_voice.wav という名前で保存
python practice_4_wav.py

# custom_name.wav という名前で保存
python practice_4_wav.py -o custom_name.wav
```

### **practice_5_tts.py**: テキスト読み上げ (Open JTalk)
`pyopenjtalk`を使い、テキストを音声に変換して再生します。複数の話者から声を選択できます。
```bash
python practice_5_tts.py
```

### **practice_6_stt.py**: 音声認識 (Vosk)
録音または指定したWAVファイルをテキストに変換します。
```bash
# 録音して音声認識
python practice_6_stt.py

# WAVファイルを指定して音声認識
python practice_6_stt.py -f my_voice.wav
```

### **practice_7_converter.py**: フォーマット変換
`ffmpeg`を使い、WAVファイルをMP3に変換します。
```bash
python practice_7_converter.py
```

### **practice_8_gtts.py**: テキスト読み上げ (Google)
`gTTS`を使い、GoogleのAPI経由でテキストを自然な音声に変換し、MP3として保存・再生します。
```bash
python practice_8_gtts.py
```

### **practice_9_pyworld_voicemod.py**: ボイスチェンジャー
`PyWorld`を使い、WAVファイルのピッチ（声の高さ）を変更します。
```bash
# デフォルト設定で実行 (my_voice.wav -> my_voice_mod.wav)
python practice_9_pyworld_voicemod.py

# ファイルとピッチを指定して実行
python practice_9_pyworld_voicemod.py -i stage_clear.wav -o high_pitch.wav --f0_rate 2.0
```

---
### (補足) その他の再生スクリプト

`sounddevice`以外を使った再生方法のサンプルです。これらは主にWAVファイルを直接再生します。

- **practice_1b_pyaudio_playback.py**: `PyAudio`ライブラリを使った再生
- **practice_1c_pygame_playback.py**: `PyGame`ライブラリを使った再生
