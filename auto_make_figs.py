import asyncio
import os
import matplotlib.pyplot as plt
import numpy as np


async def run(params=None):
    """
    真实生成图像，不再只是打印占位日志。
    """
    print("[抢跑] 正在生成能量曲线图...")
    os.makedirs("assets", exist_ok=True)

    if params is None:
        params = {}

    x = np.linspace(0, 2, 100)

    # 可选参数，不传就走默认
    baseline = params.get("baseline", 1.0)
    amplitude = params.get("amplitude", 0.5)

    y = baseline + amplitude * np.sin(x)

    plt.figure(figsize=(7, 4))
    plt.plot(x, y, label="U-energy (v1.2)")
    plt.title("TelosCore Energy Landscape")
    plt.xlabel("time")
    plt.ylabel("energy")
    plt.legend()
    plt.tight_layout()

    out_path = "assets/energy_triptych_v1.2.png"
    plt.savefig(out_path, dpi=150)
    plt.close()

    await asyncio.sleep(0.05)
    print(f"[抢跑] 图像已生成：{out_path}")
    return out_path
