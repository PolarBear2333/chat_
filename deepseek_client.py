# deepseek_client.py - Deepseek API 交互

import requests
import json
from api import api_key, api_url

class DeepseekClient:
    def __init__(self):
        self.session = requests.Session()

    def call_deepseek(self, text):
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "deepseek-chat",
            "messages": [{"role": "user", "content": text}]
        }
        
        try:
            response = self.session.post(
                api_url,
                headers=headers,
                json=data)
            if response.status_code == 200:
                return response.json()['choices'][0]['message']['content']
            else:
                print(f"API调用失败: {response.status_code}")
                return None
        except Exception as e:
            print(f"API调用错误: {str(e)}")
            return None