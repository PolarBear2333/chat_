# audio_recorder.py

import sounddevice as sd
import numpy as np
import wave
import os
from config import SAMPLE_RATE, CHANNELS, AUDIO_FORMAT, TEMP_AUDIO_FILE, TEMP_FOLDER

class AudioRecorder:
    def __init__(self):
        self.is_recording = False
        self.frames = []
        self.recording = None

        # 确保临时文件夹存在
        os.makedirs(TEMP_FOLDER, exist_ok=True)

    def start_recording(self):
        self.is_recording = True
        self.frames = []
        try:
            self.recording = sd.InputStream(
                samplerate=SAMPLE_RATE,
                channels=CHANNELS,
                dtype=AUDIO_FORMAT,
                callback=self.audio_callback)
            self.recording.start()
        except Exception as e:
            print(f"录音启动失败: {str(e)}")
            self.is_recording = False

    def stop_recording(self):
        try:
            if self.recording:
                self.recording.stop()
                self.recording.close()
            self.is_recording = False
            audio_data = np.concatenate(self.frames, axis=0)
            self.save_wav(audio_data)
        except Exception as e:
            print(f"录音停止失败: {str(e)}")

    def audio_callback(self, indata, frames, time, status):
        if self.is_recording:
            self.frames.append(indata.copy())

    def save_wav(self, audio_data):
        scaled = np.int16(audio_data * 32767)
        try:
            with wave.open(TEMP_AUDIO_FILE, 'wb') as f:
                f.setnchannels(CHANNELS)
                f.setsampwidth(2)
                f.setframerate(SAMPLE_RATE)
                f.writeframes(scaled.tobytes())
        except Exception as e:
            print(f"保存音频文件失败: {str(e)}")