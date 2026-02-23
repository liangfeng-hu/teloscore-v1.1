# TelosCore v1.1
**A deterministic Cognitive Energy Regulation Layer for stable long-term memory agents**

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red)](https://streamlit.io/)
![Last Update](https://img.shields.io/github/last-commit/liangfeng-hu/teloscore-v1.1)
[![Stars](https://img.shields.io/github/stars/liangfeng-hu/teloscore-v1.1?style=social)](https://github.com/liangfeng-hu/teloscore-v1.1/stargazers)

TelosCore v1.1 is a lightweight, backend-agnostic **stability control plane** for persistent memory agents.  
It models internal cognitive tension as a scalar potential **U** (uncertainty / conflict / entropy / telos drift) and selects actions via global minimization of **ΔU** over a bounded control set:

**Clarify / Patch / Compress / Respond**

Version **v1.1** adds energy-triggered **annealing** (recent-window plasticity) for controlled forgetting under sustained high tension.

---

## What this repo contains
- `telos_core.py` — core energy computation + ΔU action selection + annealing
- `app.py` — FastAPI server (port 8000)
- `dashboard_pro.py` — Streamlit dashboard (visualizes U and components)
- `demo_script.py` — quick demo runner
- `auto_make_figs.py` — generates the official triptych evidence figure
- `assets/00_triptych.png` — evidence chain figure (Baseline → Spike → Anneal)

---

## Quick start (reproducible)
```bash
git clone https://github.com/liangfeng-hu/teloscore-v1.1.git
cd teloscore-v1.1
pip install -r requirements.txt

# generate evidence figure
python auto_make_figs.py

# run API
uvicorn app:app --reload --port 8000

# run dashboard
streamlit run dashboard_pro.py

Reproducible evidence (video-free)

Run:
python auto_make_figs.py

It produces the official evidence chain:

Quantitative snapshot (auto-generated)

Stage	Total U	Unc.	Confl.	Ent.	Plasticity
Baseline	0.495	0.000	0.000	0.005	0.925
Spike	0.625	0.540	0.000	0.015	0.882
Anneal	0.000	0.000	0.000	0.000	0.963
Paper

PDF: TelosCore v1.1 Paper

If the link is broken: make sure the PDF is uploaded to docs/TelosCore_v1.1.pdf.

Citation
@misc{teloscore2026,
  title={TelosCore v1.1: A Deterministic Cognitive Energy Regulation Layer for Long-Term Memory Agents},
  author={Liangfeng Hu},
  year={2026},
  howpublished={https://github.com/liangfeng-hu/teloscore-v1.1},
}
<details> <summary><b>中文简介（点击展开）</b></summary>

TelosCore v1.1 是一个轻量级、可插拔的“稳定性控制层”。
它将长期对话中的认知张力（不确定性/冲突/噪声熵/目标偏离）统一为标量势能 U，并在每一步通过最小化 ΔU 来确定性选择动作：

Clarify / Patch / Compress / Respond

v1.1 增加了“退火”（annealing）：当张力持续过高时，仅对近期滑动窗口记忆做受控衰减，避免不稳定痕迹无限积累。

论文 PDF：docs/TelosCore_v1.1.pdf
图证链：assets/00_triptych.png

</details>

Made for the 2026 competition.
If this repo helps, starring it is appreciated.
::contentReference[oaicite:0]{index=0}
