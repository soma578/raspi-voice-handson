# PCで学ぶ！Python音声処理入門

---

## 自己紹介・はじめに

- このハンズオンの目的:
    - 特別な機材なしに、PCだけで音声処理の基本を体験する
    - Pythonを使って、音の録音、再生、加工、分析、合成、認識まで一通り学ぶ

---

## 本日の流れ

1.  **理論編**: 音声データとは何か？
2.  **環境構築**: 必要なツールを揃える
3.  **ライブラリ紹介**: 何を・何のために使うのか？
4.  **実践編**: スクリプトを実行して動かしてみる
    - 基本: 録音・再生・可視化・保存
    - 応用: 音声合成・音声認識・ボイスチェンジ
5.  **まとめ**

---

## 1. 理論編: 音声データとは？

- **音**: 空気の振動（アナログ信号）
- **コンピュータ**: 0と1の世界（デジタル信号）

音をPCで扱うには、アナログ信号をデジタル信号に変換する**A/D変換**が必要不可欠です。

---

## 1. 理論編: A/D変換の２ステップ

1.  **サンプリング（標本化）**
    - 時間の流れを点で区切る
    - **サンプリング周波数(Hz)**: 1秒間に点を打つ回数 (例: 44100 Hz)

2.  **量子化**
    - 各点の音の大きさ（振幅）を数値化する
    - **量子化ビット深度(bit)**: 数値の細かさ (例: 16 bit = 65,536段階)

---

## 1. 理論編: PCMとWAVとNumpy

- **PCM (Pulse-Code Modulation)**
    - A/D変換された、生の音声データ（＝ただの数値の列）

- **WAVファイル**
    - PCMデータに「サンプリング周波数: 44.1kHz」などの**メタ情報（ヘッダ）**を付けたもの

- **Numpy配列**
    - Pythonでこの「数値の列」を効率的に扱うための形式

**このハンズオンでは、音声をNumpy配列として扱います！**

---

## 2. 環境構築

- **Git, Python, venv** の基本セットアップ
- **外部ツール**のインストール (Ubuntuの場合)
    ```bash
    sudo apt install -y build-essential cmake libportaudio2 portaudio19-dev open-jtalk ffmpeg
    ```
- **Pythonライブラリ**のインストール
    ```bash
    pip install -r requirements.txt
    ```
- **Voskモデル**のダウンロード
    - 音声認識に使用する日本語言語モデル

---

## 3. ライブラリ紹介 (1/3)

- **`sounddevice` / `soundfile`**
    - 音声の録音・再生、ファイル読み書きの基本ツール
- **`numpy`**
    - 音声データ（数値の配列）を高速に計算・加工する心臓部
- **`matplotlib`**
    - 音声データをグラフ（波形・スペクトログラム）で可視化

---

## 3. ライブラリ紹介 (2/3)

- **`pyopenjtalk`**
    - **オフライン**で日本語テキストを音声に変換（音声合成）
- **`gTTS`**
    - Googleの**オンライン**サービスを使い、高品質な音声合成を実現
- **`vosk`**
    - **オフライン**で日本語の音声をテキストに変換（音声認識）

---

## 3. ライブラリ紹介 (3/3)

- **`pyworld`**
    - 声の高さ・声色を分析・再合成するボイスチェンジャーの核
- **`ffmpeg`**
    - WAVとMP3など、音声フォーマットを変換する外部ツール
- **`argparse`**
    - スクリプトにコマンドラインオプションを追加する標準ライブラリ

---

## 4. 実践編(1): 基本のI/O

- **`practice_1_record_playback.py`**
    - マイクから録音し、スピーカーで再生する
    - `python practice_1_record_playback.py`
- **`practice_4_wav.py`**
    - 録音した音声をWAVファイルに保存する
    - `python practice_4_wav.py -o my_voice.wav`

---

## 4. 実践編(2): 可視化と加工

- **`practice_2_visualize.py`**
    - 音声の波形をグラフで表示
    - `python practice_2_visualize.py -f my_voice.wav`
- **`practice_3_effects.py`**
    - Numpy配列の計算でエフェクト（音量UP, 逆再生など）をかける
    - `python practice_3_effects.py -f my_voice.wav`

---

## 4. 実践編(3): 音声合成 (TTS)

- **`practice_5_tts.py` (pyopenjtalk)**
    - オフラインで高速にテキストを読み上げ
    - `python practice_5_tts.py`
- **`practice_8_gtts.py` (gTTS)**
    - オンラインで自然な音声を生成
    - `python practice_8_gtts.py`

---

## 4. 実践編(4): 音声認識 (STT)

- **`practice_6_stt.py` (Vosk)**
    - オフラインで音声をテキストに変換
    - `python practice_6_stt.py -f my_voice.wav`

```json
{
  "text": "こんにちは"
}
```

---

## 4. 実践編(5): ボイスチェンジャー

- **`practice_9_pyworld_voicemod.py`**
    - PyWorldで声の高さ(F0)を分析・加工・再合成
    - `python practice_9_pyworld_voicemod.py -i my_voice.wav -o new_voice.wav --f0_rate 1.5`

---

## 5. まとめ

- 音声データは**Numpy配列**として扱える
- **ライブラリを組み合わせる**ことで、多彩な音声処理が実現可能
    - I/O: `sounddevice`
    - 加工・分析: `numpy`, `scipy`
    - 合成・認識: `pyopenjtalk`, `vosk`
    - 高度な分析: `pyworld`
- 今日は第一歩。ぜひ自分だけの音声アプリ開発へ！

