# voice_assistant.py

import time
import pygame
from pynput import keyboard
from audio_recorder import AudioRecorder
from audio_processor import AudioProcessor
from deepseek_client import DeepseekClient
from text_to_speech import TextToSpeech
from utils import safe_remove
from config import TEMP_AUDIO_FILE, TEMP_FOLDER

class VoiceAssistant:
    def __init__(self):
        self.recorder = AudioRecorder()
        self.processor = AudioProcessor()
        self.deepseek = DeepseekClient()
        self.tts = TextToSpeech()
        self.is_recording = False
        
        pygame.init()
        pygame.mixer.init()
        
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)
        self.listener.start()

    def on_press(self, key):
        try:
            if key == keyboard.Key.f8 and not self.is_recording:
                print("开始录音...")
                self.recorder.start_recording()
                self.is_recording = True
        except AttributeError:
            pass

    def on_release(self, key):
        try:
            if key == keyboard.Key.f8 and self.is_recording:
                print("停止录音...")
                self.recorder.stop_recording()
                self.is_recording = False
                self.process_audio()
        except AttributeError:
            pass

    def process_audio(self):
        text = self.processor.process_audio()
        if text.strip():
            response = self.deepseek.call_deepseek(text)
            if response:
                self.tts.speak(response)
        else:
            print("未检测到有效语音")
        safe_remove(TEMP_AUDIO_FILE)
        print("等待下一次按键...")

    def run(self):
        print("语音助手已启动，按F8键开始对话...")
        try:
            while True:
                time.sleep(0.1)
        except KeyboardInterrupt:
            pass
        finally:
            pygame.quit()

if __name__ == "__main__":
    assistant = VoiceAssistant()
    assistant.run()