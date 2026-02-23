import os
import time
import requests
import matplotlib.pyplot as plt

API = "http://localhost:8000/interact"

# 固定演示输入（一次连续对话流）
SEQUENCE = [
    "我想要开始变健康",                 # baseline
    "但是今晚我要吃披萨",               # spike candidate
    "也许我其实不确定能不能坚持",        # uncertainty rise
    "好的 好的 好的 好的 好的",          # entropy rise
    "但是我又想吃辣又怕胃疼",            # spike candidate
    "我想要开始变健康",                 # anneal-ish / settle
]

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "assets")
os.makedirs(ASSETS_DIR, exist_ok=True)

def call(msg: str):
    r = requests.post(API, json={"message": msg}, timeout=10)
    r.raise_for_status()
    return r.json()

def draw_one(step_idx, msg, data, out_path):
    """生成单张“可提交截图”：左侧输入+响应摘要，右侧关键数值，底部U曲线"""
    # 取值（兼容你现在返回结构）
    U = float(data.get("energy", 0.0))
    comps = data.get("components", {}) or {}
    U_unc = float(comps.get("uncertainty", 0.0))
    U_con = float(comps.get("conflict", 0.0))
    U_ent = float(comps.get("entropy", 0.0))
    U_tel = float(comps.get("telos", 0.0))
    plast = float(data.get("plasticity_score", 1.0))
    action = data.get("action", "")
    phase = data.get("phase", "")
    ctx = data.get("context_size", 0)

    # 画布
    fig = plt.figure(figsize=(12, 7))
    fig.suptitle("TelosCore v1.1 — Auto Evidence Snapshot", fontsize=16)

    # 上半部分：文本区
    ax_text = fig.add_axes([0.05, 0.50, 0.90, 0.45])
    ax_text.axis("off")

    ax_text.text(0.00, 0.92, f"Step {step_idx+1}", fontsize=12, weight="bold")
    ax_text.text(0.00, 0.78, "Input:", fontsize=11, weight="bold")
    ax_text.text(0.08, 0.78, msg, fontsize=11)

    resp = data.get("response", "")
    ax_text.text(0.00, 0.60, "Response:", fontsize=11, weight="bold")
    ax_text.text(0.12, 0.60, resp[:180] + ("..." if len(resp) > 180 else ""), fontsize=10)

    ax_text.text(0.00, 0.38, "Action / State:", fontsize=11, weight="bold")
    ax_text.text(0.16, 0.38, f"action={action} | phase={phase} | ctx_size={ctx}", fontsize=10)

    # 右侧关键数值
    metrics = [
        ("Total U", U),
        ("Uncertainty", U_unc),
        ("Conflict", U_con),
        ("Entropy", U_ent),
        ("Telos", U_tel),
        ("Plasticity", plast),
    ]
    y = 0.92
    ax_text.text(0.72, y, "Key Metrics", fontsize=11, weight="bold")
    y -= 0.10
    for k, v in metrics:
        ax_text.text(0.72, y, f"{k:>10}:  {v:.3f}", fontsize=10)
        y -= 0.08

    # 下半部分：曲线
    ax = fig.add_axes([0.08, 0.10, 0.84, 0.30])
    ax.plot([x for x in range(1, step_idx+2)], [U_list[i] for i in range(step_idx+1)], marker="o")
    ax.set_title("Energy Curve U(t)", fontsize=11)
    ax.set_xlabel("Step")
    ax.set_ylabel("U")
    ax.grid(True, alpha=0.3)

    fig.savefig(out_path, dpi=180, bbox_inches="tight")
    plt.close(fig)

def draw_triptych(p1, p2, p3, out_path):
    """三张拼一起（最适合放README）"""
    import matplotlib.image as mpimg

    img1 = mpimg.imread(p1)
    img2 = mpimg.imread(p2)
    img3 = mpimg.imread(p3)

    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    for ax, img, title in zip(
        axes,
        [img1, img2, img3],
        ["(1) Baseline", "(2) Spike", "(3) Anneal"]
    ):
        ax.imshow(img)
        ax.set_title(title, fontsize=12)
        ax.axis("off")

    fig.suptitle("TelosCore v1.1 — Baseline → Spike → Anneal", fontsize=16)
    fig.savefig(out_path, dpi=180, bbox_inches="tight")
    plt.close(fig)

if __name__ == "__main__":
    print("== TelosCore Auto Figure Generator ==")
    print("Make sure uvicorn is running: http://localhost:8000")
    print("Running sequence...")

    results = []
    global U_list
    U_list = []

    for i, msg in enumerate(SEQUENCE):
        data = call(msg)
        results.append((i, msg, data))
        U_list.append(float(data.get("energy", 0.0)))
        print(f"[{i+1}/{len(SEQUENCE)}] U={U_list[-1]:.3f} action={data.get('action')} plast={data.get('plasticity_score', 1.0)}")
        time.sleep(0.3)

    # Baseline：第一步
    base = results[0]

    # Spike：U 最大那一步
    spike = max(results, key=lambda x: float(x[2].get("energy", 0.0)))

    # Anneal：最后一步
    anneal = results[-1]

    p1 = os.path.join(ASSETS_DIR, "01_baseline.png")
    p2 = os.path.join(ASSETS_DIR, "02_spike.png")
    p3 = os.path.join(ASSETS_DIR, "03_anneal.png")
    p0 = os.path.join(ASSETS_DIR, "00_triptych.png")

    draw_one(base[0], base[1], base[2], p1)
    draw_one(spike[0], spike[1], spike[2], p2)
    draw_one(anneal[0], anneal[1], anneal[2], p3)
    draw_triptych(p1, p2, p3, p0)

    print("\nDONE. Files saved to assets/:")
    print("  00_triptych.png")
    print("  01_baseline.png")
    print("  02_spike.png")
    print("  03_anneal.png")