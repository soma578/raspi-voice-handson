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
