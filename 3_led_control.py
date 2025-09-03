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
