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
