# main.py

import subprocess
import time
import requests
import os
from voice_assistant import VoiceAssistant
from config import TTS_cosyvoice_PORT, TEMP_FOLDER, TTS_ENGINE  # 导入端口号配置和临时文件夹路径
import atexit

def shutdown_wsl():
    print("正在关闭 WSL...")
    # 执行 wsl --shutdown 命令
    subprocess.run(["wsl", "--shutdown"], check=True)
    print("WSL 已关闭")

def check_cosyvoice_connection():
    """
    检查 CosyVoice API 是否已启动
    """
    url = f"http://localhost:{TTS_cosyvoice_PORT}/"  # 使用端口号
    try:
        response = requests.get(url)
        if response.text:  # 只要 API 返回了内容，就认为 API 已启动
            print("CosyVoice API 已成功启动！")
            print(f"API 返回内容: {response.text}")
            return True
        else:
            print("API 未返回任何内容。")
            return False
    except requests.exceptions.RequestException as e:
        print(f"无法连接到 CosyVoice API: {e}")
        return False

def main():
    # 确保临时文件夹存在
    os.makedirs(TEMP_FOLDER, exist_ok=True)

    if TTS_ENGINE =="cosyvoice":
        # 注册退出时的函数
        print("以注册退出wsl任务")
        atexit.register(shutdown_wsl)

        # 启动 CosyVoice API 服务
        print("正在启动 CosyVoice API 服务...")
        process = subprocess.Popen(["start_wsl_cosyvoice.bat"], shell=True)
        print("已异步启动 .bat 文件，继续执行主程序...")

        print("正在检查 CosyVoice API 连接...")
        max_retries = 10
        retry_delay = 5  # 每次重试的延迟时间（秒）

        for attempt in range(max_retries):
            if check_cosyvoice_connection():
                break
            else:
                print(f"连接失败，第 {attempt + 1} 次重试...")
                time.sleep(retry_delay)
        else:
            print(f"经过 {max_retries} 次重试后仍无法连接到 CosyVoice API，程序退出。")
            return

    # 启动语音助手
    print("启动语音助手...")
    assistant = VoiceAssistant()
    assistant.run()

if __name__ == "__main__":
    main()