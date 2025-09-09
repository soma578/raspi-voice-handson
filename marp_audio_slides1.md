---
marp: true
theme: 
paginate: true
size: 4:3
style: |
  :root {
    --color-primary: #a2b1f6ff;
    --color-secondary: #764ba2;
    --color-accent: #6365f6ff;
    --color-success: #11cd5fff;
    --color-warning: #f39c12;
    --color-danger: #e74c3c;
    --color-dark: #2c3e50;
    --color-light: #ecf0f1;
  }

  section {
    background: linear-gradient(135deg, var(--color-primary) 0%, var(--color-secondary) 100%);
    color: white;
    font-family: "メイリオ", "Meiryo", sans-serif, sans-serif;
    font-size: 24px;
    line-height: 1.6;
    padding: 60px;
    justify-content: flex-start;
  }
  
  section.lead {
    text-align: center;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }
  
  section.content {
    background: white;
    color: var(--color-dark);
    text-align: left;
    justify-content: flex-start;
  }
  
  section.big-text {
  font-size: 1.8em;
  line-height: 2;
  }

  section .marp-pagination {
    font-size: 28px !important;
    color: #000000 !important;
    font-family: "メイリオ", "Meiryo", sans-serif !important;
  }

  h1 {
    color: white;
    font-size: 3.5em;
    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    margin-bottom: 0.5em;
  }
  
  h2 {
    color: var(--color-primary);
    font-size: 2.5em;
    border-left: 6px solid var(--color-primary);
    padding-left: 20px;
    margin-bottom: 1em;
  }
  
  h3 {
    color: var(--color-accent);
    font-size: 1.8em;
    margin: 1em 0 0.5em 0;
  }
  
  section.content h1,
  section.content h2,
  section.content h3 {
    color: var(--color-dark);
  }
  
  p, li {
    font-size: 1.1em;
    margin-bottom: 0.8em;
  }
  
  ul, ol {
    margin-left: 2em;
  }
  
  li {
    margin-bottom: 0.6em;
  }
  
  strong {
    color: var(--color-accent);
    font-weight: bold;
  }
  
  code {
    background: var(--color-dark);
    color: var(--color-light);
    padding: 0.2em 0.4em;
    border-radius: 4px;
    font-family: "メイリオ", "Meiryo", sans-serif, monospace;
    font-size: 1em;
  }
  
  pre {
    background: var(--color-dark);
    color: var(--color-light);
    padding: 1.5em;
    border-radius: 10px;
    font-family: "メイリオ", "Meiryo", sans-serif, monospace;
    font-size: 0.85em;
    line-height: 1.4;
    margin: 1em 0;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  }
  
  pre code {
    background: none;
    color: var(--color-light);
    padding: 0;
  }
  
  .highlight {
    background: linear-gradient(135deg, var(--color-accent), #9bb7d3ff);
    color: white;
    padding: 0.5em;
    border-radius: 10px;
    margin: 1em 0;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  }
  
  .warning {
    background: linear-gradient(135deg, var(--color-warning), #fdcb6e);
    color: white;
    padding: 1.5em;
    border-radius: 10px;
    margin: 1em 0;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  }
  
  .info {
    background: linear-gradient(135deg, #b8b3ffff, #2f1bcdff);
    color: white;
    padding: 1.5em;
    border-radius: 10px;
    margin: 1em 0;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0;
    background: white;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 4px 8px rgba(0,0,0,0.1);
  }
  
  th {
    background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
    color: white;
    padding: 1em;
    text-align: left;
    font-weight: bold;
  }
  
  td {
    padding: 0.8em 1em;
    border-bottom: 1px solid #eee;
    color: var(--color-dark);
  }
  
  tr:nth-child(even) td {
    background: #f8f9fa;
  }
  
  .grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 1.5em;
    margin: 1.5em 0;
  }
  
  .card {
    background: rgba(255,255,255,0.1);
    padding: 0.8em;
    border-radius: 10px;
    border-left: 4px solid var(--color-accent);
  }
  
  section.content .card {
    background: #f8f9fa;
    color: var(--color-dark);
    border-left: 4px solid var(--color-primary);
  }
  
  .flow {
    display: flex;
    justify-content: space-around;
    align-items: center;
    margin: 2em 0;
    flex-wrap: wrap;
  }
  
  .flow-item {
    background: rgba(255,255,255,0.2);
    padding: 1em;
    border-radius: 50%;
    min-width: 120px;
    min-height: 100px;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    font-weight: bold;
    margin: 0.5em;
  }
  
  section.content .flow-item {
    background: var(--color-accent);
    color: white;
  }
  
  .arrow {
    font-size: 2em;
    color: rgba(255,255,255,0.7);
    margin: 0 1em;
  }
  
  section.content .arrow {
    color: var(--color-primary);
  }
  
  /* スライドサイズを16:9に最適化 */
  section {
    width: 100%;
    height: 100%;
  }
  
  /* フォントサイズの調整 */
  @media (max-width: 1200px) {
    section { font-size: 17px; }
    h1 { font-size: 2.5em; }
    h2 { font-size: 1.6em; }
    h3 { font-size: 1.2em; }
  }
  
  /* 改良版コードハイライト - より見やすく美しい配色 */
  .hljs-comment { 
    color: #95a5a6; 
    font-style: italic; 
    opacity: 0.8;
  }
  
  .hljs-keyword { 
    color: #e74c3c; 
    font-weight: bold; 
  }
  
  .hljs-built_in { 
    color: #3498db; 
    font-weight: 600; 
  }
  
  .hljs-title { 
    color: #f1c40f; 
    font-weight: bold; 
  }
  
  .hljs-function { 
    color: #f1c40f; 
    font-weight: bold; 
  }
  
  .hljs-string { 
    color: #2ecc71; 
    font-weight: 500; 
  }
  
  .hljs-number { 
    color: #f39c12; 
    font-weight: bold; 
  }
  
  .hljs-operator { 
    color: #ecf0f1; 
    font-weight: bold; 
  }
  
  .hljs-property { 
    color: #9b59b6; 
    font-weight: 600; 
  }
  
  .hljs-variable { 
    color: #ecf0f1; 
  }
  
  .hljs-params { 
    color: #e67e22; 
    font-style: italic; 
  }
  
  .hljs-literal { 
    color: #e74c3c; 
    font-weight: bold; 
  }
  
  .hljs-meta { 
    color: #7f8c8d; 
    font-style: italic; 
  }
  
  .hljs-attr { 
    color: #16a085; 
    font-weight: 600; 
  }
  
  .hljs-type { 
    color: #3498db; 
    font-weight: bold; 
  }
  
  .hljs-name { 
    color: #f1c40f; 
  }
  
  .hljs-symbol { 
    color: #9b59b6; 
  }
  
  .hljs-bullet { 
    color: #e74c3c; 
  }
  
  .hljs-subst { 
    color: #ecf0f1; 
  }
  
  .hljs-tag { 
    color: #3498db; 
  }
  
  .hljs-regexp { 
    color: #2ecc71; 
  }
  
  .hljs-selector-id { 
    color: #f1c40f; 
    font-weight: bold; 
  }
  
  .hljs-selector-class { 
    color: #e67e22; 
    font-weight: bold; 
  }
  
  .light-text {
    color: var(--color-light) !important;
  }

---
---

<!-- _class: lead -->

# PCで学ぶ！Python音声処理入門


---

<!-- _class: content big-text -->
## 本日の内容

- **音声データの基本理論**（アナログ→デジタル変換）
- **主要ライブラリの役割と特徴**  
- **実践：録音・再生・可視化**
- **音声エフェクトの実装**
- **WAVファイルの扱い方**
- **高度な音声処理（合成・認識・加工）**

---

<!-- _class: content -->

## 1. 音声データの基本（理論編）

### 音とコンピュータの根本的な違い

<div class="grid">
<div class="card">
<strong>音</strong>: 空気中を伝わる<strong>連続的な圧力変化</strong>
<br>（アナログ信号）
</div>
<div class="card">
<strong>コンピュータ</strong>: <strong>0と1のデジタル信号</strong>
<br>のみ理解可能
</div>
</div>

<div class="warning">
<strong>課題</strong>: 連続的な波をどうやって離散的な数値に変換するか？
</div>

### 解決策：アナログ-デジタル変換（A/D変換）

<div class="flow">
<div class="flow-item">サンプリング<br>（標本化）<br>時間を細かく刻む</div>
<div class="arrow">→</div>
<div class="flow-item">量子化<br>各時点での音の<br>強さを数値化</div>
</div>

---

<!-- _class: content -->

## サンプリング周波数の深い理解

### 基本概念
音の波を**一定間隔で測定**して数値化  
**1秒間の測定回数** = サンプリング周波数（Hz）

### 具体例で理解

```python
# 44100Hzの場合
1秒 ÷ 44100 = 約0.0000227秒 = 約0.023ミリ秒間隔で測定
```

### 周波数別の特徴

| 周波数 | 用途・特徴 |
|--------|-----------|
| 8000 Hz | 電話品質（人の声が聞き取れる最低限） |
| 16000 Hz | 音声認識でよく使用（処理効率重視） |
| 44100 Hz | CD音質（音楽再生の標準） |
| 48000 Hz | プロ音響（放送・映像業界標準） |
| 96000 Hz | ハイレゾ音源（超高音質） |

---

<!-- _class: content -->

## ナイキスト定理と実用的意味

<div class="highlight">

### <span class="light-text">ナイキスト定理
**<span class="light-text">「サンプリング周波数の半分までの周波数しか正確に記録できない」</span>**

</div>

### 実例
- 44100Hz → 22050Hzまで記録可能
- 人間の可聴域：20Hz〜20000Hz  
- なぜ44100Hz？ → 20000Hz × 2 + 余裕 = 約44000Hz

### 実用的な選択指針
```python
# 用途別推奨サンプリング周波数
音声認識・合成: 16000Hz  # 効率重視
音楽再生: 44100Hz        # 品質と容量のバランス  
音楽制作: 48000Hz〜96000Hz  # 最高品質
```

---

<!-- _class: content -->

## 量子化ビット深度の実践的理解

### 量子化とは
各サンプル点での**音の強弱を何段階で表現するか**

### ビット数と表現可能範囲
```python
8 bit:  2^8  = 256段階         # 古いゲーム音源レベル
16 bit: 2^16 = 65,536段階      # CD音質
24 bit: 2^24 = 16,777,216段階  # プロ用途
32 bit: 2^32 = 約42億段階      # 計算処理用
```

### 実際の音質への影響

<div class="grid">
<div class="card"><strong>16bit</strong>: 一般リスナーには充分な品質</div>
<div class="card"><strong>24bit</strong>: 録音・編集時のノイズマージンが大きい</div>
<div class="card"><strong>32bit</strong>: 数値計算処理で精度劣化を防ぐ</div>
</div>

---

<!-- _class: content -->

## チャンネル数とステレオの仕組み

### チャンネルの概念
```python
モノラル（1ch）: [左右同じ音] 
               → データ量少、音源方向不明

ステレオ（2ch）: [左の音, 右の音]
               → 立体感、楽器の定位表現可能

マルチチャンネル: 5.1ch, 7.1ch など
                → 映画館のような包囲音響
```

### データ構造の違い
```python
# モノラル: 1次元配列
mono_data = [0.1, -0.2, 0.3, -0.1, ...]

# ステレオ: 2次元配列（各行が1サンプル）
stereo_data = [[0.1, 0.0],   # 左チャンネル, 右チャンネル
               [-0.2, 0.1],
               [0.3, -0.1], ...]
```

---

<!-- _class: content -->

## PCM（パルス符号変調）とは

<div class="highlight">

### <span class="light-text">PCMの定義
**<span class="light-text">「サンプリング・量子化された生のデジタル音声データ」</span>**

</div>

### 圧縮との違い
```python
PCM(WAV):    [生データ] → ファイルサイズ大、音質劣化なし
MP3:         [圧縮データ] → ファイルサイズ小、音質多少劣化  
FLAC:        [可逆圧縮] → サイズ中、完全復元可能
```


### WAVファイルの構造
```
WAVファイル = [ヘッダ情報] + [PCMデータ]
            ↑               ↑
      (44byte程度)      (実際の音声波形)
      
ヘッダ情報の内容:
- サンプリング周波数、ビット深度、チャンネル数、データサイズ等
```


---

<!-- _class: content -->

## なぜPythonでNumpy配列なのか？

<div class="highlight">

### <span class="light-text">音声データの本質
**<span class="light-text">「音声 = 時系列に並んだ膨大な数値の集合」</span>**

</div>

```python
# 5秒間の44100Hz音声の場合
total_samples = 5 * 44100 = 220,500個の数値
```

### Numpy配列の強力さ
```python
import numpy as np
# 全サンプルを一括で2倍（音量UP）
louder_audio = audio_data * 2
# 全サンプルに0.5を加算（DCオフセット調整）  
offset_audio = audio_data + 0.5
# 配列同士の演算（エコー効果）
echo_audio = audio_data + audio_data * 0.5
# このような操作がC言語並みの速度で実行される！
```

---

<!-- _class: content -->

## Numpyが音声処理に最適な理由

### 1. ベクトル化演算
```python
# 遅い方法（Pythonループ）
result = []
for sample in audio_data:
    result.append(sample * 2)

# 高速方法（Numpy）  
result = audio_data * 2  # 数百倍〜数千倍高速！
```

### 2. メモリ効率 & 3. ライブラリ親和性
<div class="grid">
<div class="card">
<strong>連続メモリ領域</strong><br>
Pythonリストと違いメモリを効率的に使用
</div>
<div class="card">  
<strong>標準データ形式</strong><br>
ほぼ全ての音声ライブラリがNumpy配列でやり取り
</div>
</div>

---

<!-- _class: content -->

## データ型の使い分け

### よく使われるデータ型
```python
np.int16:    [-32768 ~ 32767] 
             → WAVファイル保存、整数計算

np.float32:  [-1.0 ~ 1.0 (通常)]
             → リアルタイム処理、メモリ節約

np.float64:  [-1.0 ~ 1.0 (より高精度)]
             → 高品質音声分析、PyWorld等
```

### 型変換の実例
```python
# 録音データ（sounddevice） → float32
recording = sd.rec(...)  # shape: (samples,), dtype: float32

# WAV保存用に変換
wav_data = (recording * 32767).astype(np.int16)

# 分析用に変換  
analysis_data = recording.astype(np.float64)
```

---

<!-- _class: content -->

## 主要ライブラリの役割分担-1

### 音声I/O（入出力）レイヤー
<div class="grid">
<div class="card"><strong>sounddevice</strong><br>リアルタイム録音・再生（低遅延）</div>
<div class="card"><strong>soundfile</strong><br>多様な音声ファイル読み書き</div>
<div class="card"><strong>scipy.io.wavfile</strong><br>WAVファイル専用、軽量</div>
</div>

### 数値計算・処理レイヤー  
<div class="grid">
<div class="card"><strong>numpy</strong><br>基本配列演算、エフェクト処理</div>
<div class="card"><strong>scipy</strong><br>高度な信号処理、フィルタ処理</div>
<div class="card"><strong>matplotlib</strong><br>波形・スペクトログラム可視化</div>
</div>

---
<!-- _class: content -->

## 主要ライブラリの役割分担-2

### AI・高度処理レイヤー
<div class="grid">
<div class="card"><strong>pyopenjtalk</strong><br>オフライン日本語音声合成</div>
<div class="card"><strong>vosk</strong><br>オフライン音声認識</div>
<div class="card"><strong>pyworld</strong><br>音声分析・変調（ボコーダー）</div>
</div>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>
<br>

---

<!-- _class: content -->

## 2. 最初の実践：録音と再生

### practice_1_record_playback.py の設計思想
- **シンプルさ**: 最小限のコードで音声処理を体験
- **柔軟性**: コマンドライン引数でファイル指定可能  
- **拡張性**: 他のスクリプトのベースとして機能
- **教育効果**: sounddeviceとNumpy配列の関係を理解

### 処理の流れ
<div class="flow">
<div class="flow-item" style="min-width: 50px; min-height: 50px; font-size: 1em; margin:0 3em;">引数チェック</div>

<div class="arrow" style="margin: 1em; font-size: 1em;">→</div>

<div class="flow-item" style="min-width: 50px; min-height: 50px; font-size: 1em; margin: 0 3em;">ファイル読込<br>or 録音</div>

<div class="arrow" style="margin: 1em; font-size: 1em;">→</div>

<div class="flow-item" style="min-width: 50px; min-height: 50px; font-size: 1em; margin: 0 3em;">データ<br>確認</div>

<div class="arrow" style="margin: 1em; font-size: 1em;">→</div>

<div class="flow-item" style="min-width: 50px; min-height: 50px; font-size: 1em; margin: 0 3em;">再生</div>
</div>

---

<!-- _class: content -->

## sounddeviceの核心機能

### sd.rec()の詳細パラメータ
```python
recording = sd.rec(
    frames=int(DURATION * FS),  # 録音サンプル数
    samplerate=FS,              # サンプリング周波数  
    channels=1,                 # チャンネル数
    dtype='float32'             # データ型（省略時の推奨）
)
```

### 戻り値の特徴
```python
print(f"データ型: {recording.dtype}")      # float32
print(f"形状: {recording.shape}")           # (220500,) または (220500, 1)
print(f"値の範囲: [{recording.min():.3f}, {recording.max():.3f}]")
```
<br>
<br>
<br>
<br>
<br>
<br>

---

<!-- _class: content -->

## sd.wait()の重要性

<div class="warning">

### 非同期処理の制御
```python
# 録音開始（非ブロッキング）
recording = sd.rec(int(DURATION * FS), samplerate=FS, channels=1)
print("録音中...")  # すぐに実行される

# 録音完了まで待機（ブロッキング）
sd.wait()
print("録音完了")  # 録音終了後に実行される
```

### wait()を忘れた場合の問題
```python
recording = sd.rec(...)
# sd.wait() なし
sd.play(recording, FS)  # まだ録音中のデータを再生 → ノイズ！
```

</div>

---

<!-- _class: content -->

## soundfileの詳細機能

### 対応フォーマット
```python
# 読み込み可能な主要フォーマット
WAV, FLAC, OGG, AIFF, AU, RAW, HTK, SDS, WAVEX, SD2, CAF, WVE

# 使用例
data, sr = sf.read('input.flac')      # FLACファイル読み込み
sf.write('output.wav', data, sr)      # WAVファイル書き込み
```

### dtype指定の重要性
```python
# sounddeviceと合わせるため、float32を明示
myrecording, FS = sf.read(args.file, dtype='float32')

# 指定しない場合、ファイルによってはfloat64になることがある
# → sounddeviceとのデータ型不整合でエラーの可能性
```

---

<!-- _class: content -->

## 実行パターンと活用法

### 基本実行
```bash
# 5秒録音して即座に再生
python practice_1_record_playback.py
```

### ファイル再生
```bash  
# 指定ファイルを再生
python practice_1_record_playback.py -f my_voice.wav
python practice_1_record_playback.py --file background_music.flac
```

### デバッグ・検証での活用
```bash
# 他のスクリプトで生成したファイルの確認
python practice_4_wav.py -o test.wav           # ファイル生成
python practice_1_record_playback.py -f test.wav  # 生成結果確認
```

<div class="info">
<strong>活用のポイント</strong>: このスクリプトは他の処理スクリプトの動作確認にも使える万能ツール
</div>

---

<!-- _class: content -->

## データ形状の理解

### モノラルの場合
```python
# 形状: (samples,)
myrecording.shape  # (220500,)
myrecording.ndim   # 1

# アクセス方法
first_sample = myrecording[0]      # スカラー値
```

### ステレオの場合  
```python
# 形状: (samples, channels)
stereo_data.shape  # (220500, 2)
stereo_data.ndim   # 2

# アクセス方法
left_channel = stereo_data[:, 0]   # 左チャンネル全体
right_channel = stereo_data[:, 1]  # 右チャンネル全体
first_frame = stereo_data[0, :]    # 最初のステレオフレーム [L, R]
```
---

<!-- _class: content -->

## 第1部まとめ

### 習得した基礎知識

<div class="grid">
<div class="card">
<strong>音声デジタル化</strong><br>サンプリング・量子化の仕組み
</div>
<div class="card">
<strong>ライブラリ構成</strong><br>sounddevice, soundfile, numpyの役割
</div>
<div class="card">
<strong>データ構造</strong><br>モノラル・ステレオの配列形状
</div>
<div class="card">
<strong>実践スキル</strong><br>録音・再生・ファイル操作
</div>
</div>

### 重要なポイント
- **44100Hz = CD音質**: ナイキスト定理による理論的根拠
- **Numpy配列**: 音声処理における標準データ形式
- **float32 vs int16**: 用途に応じたデータ型選択
- **非同期処理**: sd.wait()の重要性
