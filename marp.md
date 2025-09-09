---
marp: true
theme: default
size: 16:9
paginate: true
header: 'PCで学ぶ！Python音声処理入門'
footer: '© Your Name or Organization'
---

# PCで学ぶ！Python音声処理入門
## 【完全版】

---

## 1. はじめに

### この講座のゴール
特別なハードウェアを使わず、お手元のPCとPythonだけで**音声処理の基本**をマスターします。

- マイクからの**録音** 🎤
- スピーカーでの**再生** 🔊
- 録音した音声データの**加工・分析** 🧪

これら一連の流れを、理論と実践を交えながら体験していきましょう！

---

## 本日の流れ

1.  **環境構築**: 開発環境を整えよう
2.  **理論編**: 音声データの正体を知ろう
3.  **実践編**: Pythonで音を操ろう
    - 録音・再生・可視化・保存
    - 音声合成 (Text to Speech)
    - 音声認識 (Speech to Text)
    - 音声加工 (ボイスチェンジ)
4.  **まとめ**

---

## 2. 環境構築
### 手順1: リポジトリのクローン

まずは、本日の教材をダウンロードします。

```bash
# あなたのリポジトリURLに書き換えてください
git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)

cd your-repository-name
手順2: 必要なツールのインストール (Ubuntuの場合)
音声処理に必要なライブラリやツールをシステムにインストールします。

Bash

sudo apt update
sudo apt install -y \
  build-essential \
  cmake \
  python3-pip \
  python3-venv \
  libportaudio2 \
  portaudio19-dev \
  open-jtalk \
  open-jtalk-mecab-naist-jdic \
  ffmpeg \
  wget \
  unzip
手順3: Python環境のセットアップ
プロジェクト専用のPython環境（仮想環境）を構築し、必要なライブラリをインストールします。

Bash

# 仮想環境の作成
python3 -m venv venv

# 仮想環境のアクティベート
source venv/bin/activate

# 必要なPythonライブラリをインストール
pip install -r requirements.txt
手順4: 音声認識モデルのダウンロード (Vosk)
オフライン音声認識で使用するVoskの日本語モデルをダウンロード・配置します。

Bash

# モデルをダウンロード
wget [https://alphacephei.com/vosk/models/vosk-model-ja-0.22.zip](https://alphacephei.com/vosk/models/vosk-model-ja-0.22.zip)

# 解凍して所定の場所に配置
unzip -o vosk-model-ja-0.22.zip -d models/vosk/
mv models/vosk/vosk-model-ja-0.22 models/vosk/ja-0.22

# 不要になったzipファイルを削除
rm vosk-model-ja-0.22.zip
これで準備完了です！