# config.py - 参数配置文件

# 录音配置
SAMPLE_RATE = 16000
CHANNELS = 1
AUDIO_FORMAT = 'float32'

# 语音合成配置
TTS_ENGINE = "cosyvoice"  # 选择语音合成引擎，可选项："pyttsx3"、"cosyvoice"、"gtts"
# 采用gtts
TTS_gtts_SPEED = 1.3
TTS_gtts_LANGUAGE = "zh-cn"  # 语言，可选项："zh-CNcn"、"en-US"
# 采用pyttsx3
TTS_pyttsx3_RATE = 200  # 语速
TTS_pyttsx3_VOLUME = 1.3  # 音量
TTS_pyttsx3_LANGUAGE = "zh"  # 语言，可选项："zh"、"en"
# 采用cosyvoice
TTS_cosyvoice_PORT = 50001  # 新增端口号配置
TTS_cosyvoice_SPEAKER = "中文女"
TTS_cosyvoice_STREAMING = 1

# 模型配置
MODEL_DIR = "E:/AI_Model/iic/SenseVoiceSmall"
DEVICE = "cuda:0"

# 其他配置
TEMP_FOLDER = "temp"  # 临时文件夹
TEMP_AUDIO_FILE = f"{TEMP_FOLDER}/temp.wav"  # 临时音频文件
OUTPUT_AUDIO_FILE = f"{TEMP_FOLDER}/output.pcm"  # 输出音频文件