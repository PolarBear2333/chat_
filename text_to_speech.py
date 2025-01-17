# text_to_speech.py

import requests
import json
import pyaudio
import os
from config import TEMP_FOLDER, TTS_ENGINE
import subprocess
import pyttsx3  # 导入 pyttsx3 模块
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import io
import time

class TextToSpeech:
    def __init__(self):
        self.session = requests.Session()

        # 确保临时文件夹存在
        os.makedirs(TEMP_FOLDER, exist_ok=True)

    def speak(self, text):
        print(f"AI回复: {text}")
        print(f"语音生成模型：{TTS_ENGINE}")
        if TTS_ENGINE == "pyttsx3":
        # 使用 pyttsx3 进行语音合成
            from config import TTS_pyttsx3_RATE, TTS_pyttsx3_VOLUME, TTS_pyttsx3_LANGUAGE
            engine = pyttsx3.init()
            engine.setProperty('rate', TTS_pyttsx3_RATE)  # 语速
            engine.setProperty('volume', TTS_pyttsx3_VOLUME)  # 音量

            # 获取可用语音
            voices = engine.getProperty('voices')
            for voice in voices:
                print(f"Voice: {voice.name}")

            # 设置语音（例如中文）
            engine.setProperty('voice', TTS_pyttsx3_LANGUAGE)  # 设置中文语音

            engine.say(text)
            engine.runAndWait()
        if TTS_ENGINE == "cosyvoice":
        # 使用 DeepSeek API 进行语音合成
            from config import TTS_cosyvoice_SPEAKER, TTS_cosyvoice_STREAMING, TTS_cosyvoice_PORT

            headers = {'Content-Type': 'application/json'}
            gpt = {"text": text, "speaker": TTS_cosyvoice_SPEAKER, "streaming": TTS_cosyvoice_STREAMING}
            url = f"http://localhost:{TTS_cosyvoice_PORT}/"  # 使用端口号

            p = pyaudio.PyAudio()
            stream = p.open(
                format=pyaudio.paInt16,
                channels=1,
                rate=22050,
                output=True
            )

            if TTS_cosyvoice_STREAMING:
                # 流式输出
                response = self.session.post(url, data=json.dumps(gpt), headers=headers, stream=True)
                try:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            stream.write(chunk)
                    time.sleep(0.5)
                except Exception as e:
                    print(f"播放音频时出错: {e}")
                stream.stop_stream()
                stream.close()
                p.terminate()
                        
            else:
                # 非流式输出
                response = self.session.post(url, data=json.dumps(gpt), headers=headers)
                if response.status_code == 200:
                    # 使用 ffmpeg 转换格式并播放
                    process = subprocess.Popen(
                        ["ffmpeg", "-i", "pipe:0", "-f", "wav", "pipe:1"],
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE
                    )
                    pcm_data, _ = process.communicate(input=response.content)
                    # 播放 PCM 数据
                    stream.write(pcm_data)
                else:
                    print(f"请求失败，状态码: {response.status_code}")
        if TTS_ENGINE == "gtts":
            from config import TTS_gtts_SPEED, TTS_gtts_LANGUAGE
            tts = gTTS(text=text, lang=TTS_gtts_LANGUAGE)
            audio_data = io.BytesIO()
            tts.write_to_fp(audio_data)  # 将音频数据写入内存
            audio_data.seek(0)  # 将指针重置到文件开头
            # 从内存中加载音频数据
            sound = AudioSegment.from_mp3(audio_data)

            # 调整音频速度
            self.speed = TTS_gtts_SPEED
            if self.speed != 1.0:
                sound = sound.speedup(playback_speed=self.speed)

            # 播放音频
            play(sound)