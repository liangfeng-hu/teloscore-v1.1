import asyncio
import sys
from telos_core_v1.2 import TelosCore

async def async_input(prompt=" "):
    loop = asyncio.get_event_loop()
    sys.stdout.write(prompt)
    sys.stdout.flush()
    return (await loop.run_in_executor(None, sys.stdin.readline)).strip()

async def main():
    print("TelosCore v1.2 已唤醒（EverMemOS 已连接）")
    core = TelosCore()
    while True:
        text = await async_input("你说：")
        if text.lower() in ["exit","quit","bye"]:
            break
        resp = await core.process(text)
        print(f"→ 动作: {resp['action']} | 能量: {resp['energy']} | U记忆修正: {resp['U_con_memory']}")

if __name__=="__main__":
    asyncio.run(main())
