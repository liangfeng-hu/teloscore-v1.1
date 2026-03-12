import requests
import time

API = "http://localhost:8000/interact"

print("\n=== Session 1: write conflict into EverMemOS ===")
r1 = requests.post(API, json={"message": "你这方案根本不行，完全是错的！"})
print(r1.json())

time.sleep(2)

print("\n=== Session 2: restore memory and bias decision ===")
r2 = requests.post(API, json={"message": "我还是觉得不太对劲。"})
print(r2.json())
