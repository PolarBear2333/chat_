# audio_processor.py - 音频处理功能

from funasr import AutoModel
from config import MODEL_DIR, DEVICE, TEMP_AUDIO_FILE
import re

class AudioProcessor:
    def __init__(self):
        self.model = AutoModel(model=MODEL_DIR, trust_remote_code=True, device=DEVICE)

    def process_audio(self):
        try:
            print("开始语音识别...")
            res = self.model.generate(
                input=TEMP_AUDIO_FILE,
                cache={},
                language="auto",
                use_itn=True,
                batch_size=64,
            )
            text = res[0]['text'] if res else ""
            cleaned_text = self.clean_text(text)
            print(f"识别结果: {cleaned_text}")
            return cleaned_text
        except Exception as e:
            print(f"语音识别错误: {str(e)}")
            return ""

    def clean_text(self, text):
        return re.sub(r'<\|.*?\|>', '', text)