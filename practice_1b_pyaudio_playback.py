# practice_1b_pyaudio_playback.py
import wave
import pyaudio
import sys

FILENAME = "my_voice.wav" # practice_4_wav.pyなどで作成したファイル

print(f"{FILENAME} をPyAudioで再生します。")

try:
    wf=wave.open(FILENAME, "r")
except FileNotFoundError:
    print(f"エラー: {FILENAME} が見つかりません。")
    print("先に practice_4_wav.py などを実行して、再生するWAVファイルを作成してください。")
    sys.exit()

p = pyaudio.PyAudio()
stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)
chunk = 1024
data = wf.readframes(chunk)
while data != b'':
    stream.write(data)
    data = wf.readframes(chunk)
stream.close()
p.terminate()
print(f"{FILENAME} の再生が完了しました。")
