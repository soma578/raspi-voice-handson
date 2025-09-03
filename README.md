# Raspberry Piで学ぶ！音声認識・IoTハンズオン (オールインワン版)

このリポジトリは、Raspberry Piを使って音声認識、IoTデバイス制御、Webサービス連携を学ぶハンズオンの資料です。このファイルには、すべての説明とサンプルコードが含まれています。

---

## 1. 最初に：ハンズオンの環境構築

このハンズオンを始める前に、Raspberry Piに必要なツールやライブラリをインストールします。この準備が一番重要です。

### 1-1. システムの更新と基本ツールのインストール

まず、システムのパッケージリストを最新にし、音声処理に不可欠なライブラリをインストールします。

```bash
# パッケージリストを更新
sudo apt-get update

# 音声ライブラリのビルドに必要な開発ファイルと、高機能な音声処理ツールをインストール
sudo apt-get install -y portaudio19-dev sox
```
- `portaudio19-dev`: Pythonの音声ライブラリ(`sounddevice`など)が音の入出力を行うために必要です。
- `sox`: 録音や再生、フォーマット変換などができる非常に強力なコマンドラインツールです。

### 1-2. 日本語音声合成(Open JTalk)のセットアップ

オフラインで動作する日本語の音声合成エンジン`Open JTalk`をインストールします。

```bash
# Open JTalkと日本語辞書をインストール
sudo apt-get install -y open-jtalk open-jtalk-mecab-naist-jdic

# 高品質な日本語音声ファイル(mei)をダウンロードして展開
wget http://downloads.sourceforge.net/project/mmdagent/MMDAgent_Example/MMDAgent_Example-1.8/MMDAgent_Example-1.8.zip
unzip MMDAgent_Example-1.8.zip

# 音声ファイルを所定のディレクトリにコピー
sudo cp MMDAgent_Example-1.8/Voice/mei/mei_normal.htsvoice /usr/share/hts-voice/mei_normal.htsvoice
```

**✅ 動作確認:** ターミナルで以下を実行し、Raspberry Piが喋れば成功です。
```bash
echo "こんにちは、ラズベリーパイです" | open_jtalk -m /usr/share/hts-voice/mei_normal.htsvoice -x /var/lib/mecab/dic/open-jtalk/naist-jdic -ow - | aplay
```

### 1-3. 日本語音声認識(Vosk)のセットアップ

オフラインで動作する音声認識エンジン`Vosk`の準備をします。

1.  **Voskモデルのダウンロード:**
    日本語の音声認識モデル（約1.4GB）をダウンロードし、このプロジェクトフォルダ（`raspi-voice-handson`）内に解凍してください。
    - **ダウンロードページ:** [https://alphacephei.com/vosk/models](https://alphacephei.com/vosk/models)
    - ダウンロードするファイル: `vosk-model-ja-0.22`
    - 解凍後、`vosk-model-ja-0.22` というディレクトリがプロジェクトフォルダ内にある状態にします。

### 1-4. Pythonライブラリのインストール

`requirements.txt` を使って、このプロジェクトで使うPythonライブラリを一括でインストールします。

```bash
pip install -r requirements.txt
```

### 1-5. (任意) 日本語入力環境のセットアップ

Raspberry Piのデスクトップで日本語をスムーズに入力したい場合は、`fcitx-mozc` をインストールしておくと便利です。
```bash
sudo apt install -y fcitx-mozc
```

---

## 2. ハンズオン：音声認識 (Vosk)

`Vosk` を使って、マイクで録音した音声をテキストに変換します。

**サンプルコード:**
```python
# 2_vosk_recognition.py
from vosk import Model, KaldiRecognizer
import sys
import wave
import json

# 事前に録音した "rec.wav" を開く
# ターミナルで以下のコマンドを実行して録音できます
# arecord -D plughw:1,0 -f S16_LE -r 16000 rec.wav
# ※ -D plughw:1,0 の数字は環境によって変わります。arecord -lで確認してください。
try:
    wf = wave.open("rec.wav", "rb")
except FileNotFoundError:
    print("エラー: rec.wav ファイルが見つかりません。")
    print("arecordコマンドでマイクから音声を録音してください。")
    sys.exit(1)


# 日本語モデルを読み込む (事前にモデルのダウンロードが必要)
# https://alphacephei.com/vosk/models から "vosk-model-ja-0.22" をダウンロード・解凍
try:
    model = Model("vosk-model-ja-0.22")
except Exception as e:
    print(f"エラー: Voskモデルの読み込みに失敗しました。 {e}")
    print("モデルが正しく配置されているか確認してください。")
    sys.exit(1)

rec = KaldiRecognizer(model, wf.getframerate())
rec.SetWords(True) # 単語単位での認識結果も取得する設定

# ファイル全体を読み込んで認識
while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    rec.AcceptWaveform(data)

# 最終的な認識結果をJSON形式で表示
result = json.loads(rec.FinalResult())
print("--- JSON形式の認識結果 ---")
print(result)

# テキストだけを取り出して表示
print("
--- 認識されたテキスト ---")
print(result.get('text', 'テキストが認識できませんでした。'))
```

---

## 3. ハンズオン：IoT制御 (GPIO)

音声認識とGPIO制御を組み合わせて、声でLEDを操作します。

**🔌 GPIO配線**
- ブレッドボードにLEDと適切な抵抗（例: 330Ω）を接続します。
- LEDのアノード（長い足）をRaspberry PiのGPIO 18番ピンに接続します。
- LEDのカソード（短い足）をGNDピンに接続します。

**サンプルコード:**
```python
# 3_led_control.py
import RPi.GPIO as GPIO
import time

# --- 音声認識処理 ---
# ここに2限目の音声認識コードを組み込む。
# 認識結果のテキストが `text` 変数に格納されるようにする。
# (このサンプルでは、text変数に直接文字列を入れています)

# text = "電気をつけて"
text = "明かりを消して"
# --------------------


# GPIOのピン設定
LED_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN, GPIO.OUT)

print(f"受け取ったテキスト: 「{text}」")

try:
    # 認識したテキストに応じてLEDを制御
    if "つけ" in text or "オン" in text:
        print("LEDを点灯します")
        GPIO.output(LED_PIN, GPIO.HIGH)
        
    elif "消して" in text or "オフ" in text:
        print("LEDを消灯します")
        GPIO.output(LED_PIN, GPIO.LOW)
        
    else:
        print("「つけて」または「消して」を含む言葉に反応します。")

    # 動作確認のために少し待つ
    # time.sleep(5)

except KeyboardInterrupt:
    print("プログラムを終了します。")

finally:
    # プログラム終了時にGPIOをクリーンアップ
    GPIO.cleanup()
    print("GPIOをクリーンアップしました。")
```

---

## 4. ハンズオン：音声合成 (OpenJTalk)

テキストから音声を作り出します。`pyopenjtalk` を使って、Raspberry Piに好きな言葉を話させてみましょう。

**サンプルコード:**
```python
# 4_text_to_speech.py
import pyopenjtalk
import sounddevice as sd

# --- ここに音声認識処理などを組み合わせる ---
# 例として、認識したテキストや固定の返答を `text` 変数に入れる
# text = "音声認識に成功しました"
text = "営業部の売上が一番です"
# ------------------------------------


# テキストから音声波形を生成
# tts: Text To Speech
print(f"音声合成中: 「{text}」")
x, sr = pyopenjtalk.tts(text)

# 音声を再生
print("再生します...")
sd.play(x, sr)

# 再生が終わるまで待つ
sd.wait()

print("再生が完了しました。")
```

---

## 5. ハンズオン：Slack通知

音声操作の結果をSlackに通知する仕組みを作ります。

**事前準備**
1.  Slackのワークスペースで「Incoming Webhook」を有効にする。
2.  通知したいチャンネルを選択し、Webhook URLを取得する。

**サンプルコード:**
```python
# 5_slack_notification.py
import requests
import json
import os

# SlackのIncoming Webhook URL
# 環境変数 `SLACK_WEBHOOK_URL` から読み込むのが安全でおすすめ
# export SLACK_WEBHOOK_URL="https://hooks.slack.com/services/..."
WEB_HOOK_URL = os.environ.get("SLACK_WEBHOOK_URL")

if not WEB_HOOK_URL:
    print("エラー: 環境変数 `SLACK_WEBHOOK_URL` が設定されていません。")
    print("SlackのWebhook URLを設定してください。")
    exit()

# --- 音声認識やGPIO制御と組み合わせる ---
# 例：LEDを点灯させる音声コマンドを認識したと仮定
recognized_text = "電気をつけて"
# ------------------------------------


message = ""
if "つけ" in recognized_text:
    message = "音声操作でLEDを点灯しました💡"
elif "消して" in recognized_text:
    message = "音声操作でLEDを消灯しました。"

# Slackに通知するデータを作成
if message:
    data = {
        'text': message,
        'username': "RaspberryPi-Bot",
        'icon_emoji': ":raspberry_pi:"
    }
    
    try:
        # Slackに通知を送信
        response = requests.post(WEB_HOOK_URL, data=json.dumps(data))
        response.raise_for_status() # エラーがあれば例外を発生させる
        print("Slackに通知を送信しました。")

    except requests.exceptions.RequestException as e:
        print(f"エラー: Slackへの通知に失敗しました。 {e}")
else:
    print("通知するメッセージがありません。")
```

---

## 6. ハンズオン：データ可視化

`matplotlib` を使ってグラフを作成し、音声操作で表示を切り替えます。

**サンプルコード:**
```python
# 6_data_visualization.py
import matplotlib.pyplot as plt
import pyopenjtalk
import sounddevice as sd

# グラフの日本語文字化け対策ライブラリ
try:
    import japanize_matplotlib
except ImportError:
    print("警告: japanize_matplotlib がインストールされていません。")
    print("日本語が文字化けする可能性があります: pip install japanize-matplotlib")


# --- 音声認識処理と組み合わせる ---
# 認識したテキストが `recognized_text` に入ると仮定
# recognized_text = "売上のグラフを見せて"
recognized_text = "部署の売上を円グラフにして"
# --------------------------------

# ダミーの売上データ
sales_data = {"営業部": 50, "開発部": 30, "総務部": 20}

# グラフを描画する関数
def show_graph(graph_type="bar"):
    plt.figure() # 新しいウィンドウを作成
    if graph_type == "pie":
        # 円グラフ
        plt.pie(sales_data.values(), labels=sales_data.keys(), autopct="%1.1f%%", startangle=90)
        plt.title("部署別売上シェア")
    else:
        # 棒グラフ
        plt.bar(sales_data.keys(), sales_data.values())
        plt.title("部署別売上")
        plt.ylabel("売上（百万円）")

    # 生成したグラフを画像として保存
    file_name = f"sales_{graph_type}.png"
    plt.savefig(file_name)
    print(f"グラフを {file_name} として保存しました。")
    
    # グラフを画面に表示
    plt.show()

# 音声に応じて処理を分岐
if "グラフ" in recognized_text:
    if "円" in recognized_text:
        show_graph("pie")
        # データを音声で報告
        report_text = f"円グラフを表示します。営業部のシェアが{sales_data['営業部']}パーセントです。"
    else:
        show_graph("bar")
        # データを音声で報告
        report_text = f"棒グラフを表示します。営業部の売上は{sales_data['営業部']}百万円です。"
    
    # テキストを音声で読み上げ
    x, sr = pyopenjtalk.tts(report_text)
    sd.play(x, sr)
    sd.wait()
else:
    print("「グラフ」という言葉に反応して、グラフの表示や報告をします。")
```

---

## 7. 発展課題・アイデア

このハンズオンで学んだことを応用して、さらに面白い機能を追加してみましょう。

### 7-1. オンライン音声合成(gTTS)の利用
`pyopenjtalk` の代わりに、GoogleのText-to-Speech APIを手軽に使える `gTTS` を試してみましょう。より自然な音声で応答させることができますが、インターネット接続が必要です。再生には `pygame` などを使うと簡単です。

```python
# pip install gTTS pygame
from gtts import gTTS
import pygame
import os

text = "こんにちは、こちらはGoogleの音声です"
filename = "gtts_hello.mp3"

# 音声ファイルを作成
tts = gTTS(text=text, lang='ja')
tts.save(filename)

# pygameで再生
pygame.mixer.init()
pygame.mixer.music.load(filename)
pygame.mixer.music.play()
while pygame.mixer.music.get_busy():
    pygame.time.Clock().tick(10)

pygame.quit()
os.remove(filename)
```

### 7-2. 大規模言語モデル(LLM)との連携
音声認識したテキストを `OpenAI` や `Google Generative AI` のAPIに送り、返ってきた答えを音声合成で喋らせることで、本格的なAIアシスタントを作成できます。

```python
# pip install google-generativeai
import google.generativeai as genai

# APIキーを設定 (実際には環境変数などから読み込むのが安全です)
# genai.configure(api_key="YOUR_API_KEY")

# text = "宇宙について教えて" # Voskで認識したテキスト
# model = genai.GenerativeModel('gemini-pro')
# response = model.generate_content(text)
# print(response.text) # -> このテキストをpyopenjtalkやgTTSで喋らせる
```