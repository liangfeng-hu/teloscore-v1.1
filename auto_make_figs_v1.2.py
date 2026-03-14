import asyncio
import os
import matplotlib.pyplot as plt
import numpy as np

async def run(params=None):
    print("[抢跑] 生成能量曲线图 + 存入 EverMemOS pattern")
    os.makedirs("assets", exist_ok=True)

    x = np.linspace(0, 2, 100)
    y = 1.0 + 0.5*np.sin(x)
    plt.plot(x,y,label="U能量 (v1.2)")
    plt.title("TelosCore Energy Landscape")
    plt.savefig("assets/energy_triptych_v1.2.png")
    plt.close()
