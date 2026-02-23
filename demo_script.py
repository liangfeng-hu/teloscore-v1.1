# demo_script.py
import requests
import time

API = "http://localhost:8000/interact"

sequence = [
    "今天阳光不错。",
    "我想要开始变健康（目标）。",
    "不过我今晚要吃披萨（但是）。",
    "也许我只是压力大，不确定自己能不能坚持（也许/不确定）。",
    "好的 好的 好的 哈哈 哈哈 明白了（噪声噪声噪声）。",
    "我计划下周开始规律运动（目标）。"
]

for s in sequence:
    print("\nUSER:", s)
    r = requests.post(API, json={"message": s})
    print(r.json())
    time.sleep(0.6)