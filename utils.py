# utils.py

import os
import time

def safe_remove(filename, max_attempts=10):
    for attempt in range(max_attempts):
        try:
            os.remove(filename)
            break
        except PermissionError:
            print(f"文件 {filename} 正在被使用，尝试第 {attempt+1} 次删除...")
            time.sleep(1)
        except FileNotFoundError:
            break
    else:
        print(f"无法删除文件 {filename}，达到最大重试次数。")