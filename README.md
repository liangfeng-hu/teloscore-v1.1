# TelosCore Full-Memory Build
**A memory-aware cognitive control layer powered by EverMemOS**

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red)](https://streamlit.io/)
![Last Update](https://img.shields.io/github/last-commit/liangfeng-hu/teloscore-v1.1)
[![Stars](https://img.shields.io/github/stars/liangfeng-hu/teloscore-v1.1?style=social)](https://github.com/liangfeng-hu/teloscore-v1.1/stargazers)

## Powered by EverMemOS
TelosCore Full-Memory Build uses **EverMemOS** as the persistent memory substrate.

- State memory is persisted across sessions
- Event memory is written as conflict / clarify / goal events
- Retrieved memory actively modifies U
- Action selection is therefore memory-aware, not purely reactive

This repository provides a **minimal running full-memory prototype** for the competition.  
The broader architecture is documented in `docs/FULL_MEMORY_ARCHITECTURE.md`.

---

## What this repo contains
- `telos_core.py` — core cognitive energy computation + action selection
- `evermemos_client.py` — EverMemOS client for state/event persistence
- `app.py` — FastAPI server
- `dashboard_pro.py` — Streamlit dashboard
- `demo_script.py` — two-session memory-aware demo
- `auto_make_figs.py` — evidence figure generator
- `assets/00_triptych.png` — Baseline → Spike → Anneal evidence
- `docs/TelosCore_v1.1.pdf` — paper PDF
- `docs/FULL_MEMORY_ARCHITECTURE.md` — architecture SSOT
- `docs/COMPETITION_EVIDENCE.md` — evidence checklist
- `docs/EVAL_PROTOCOL.md` — evaluation claim boundary

---

## Quick start

```bash
git clone https://github.com/liangfeng-hu/teloscore-v1.1.git
cd teloscore-v1.1
pip install -r requirements.txt
Start EverMemOS
docker compose up -d
Start API
uvicorn app:app --reload --port 8000
Run demo
python demo_script.py
Run dashboard
streamlit run dashboard_pro.py
Reproducible evidence

Run:

python auto_make_figs.py

It generates the official evidence chain:

Quantitative snapshot
Stage	Total U	Unc.	Confl.	Ent.	Plasticity
Baseline	0.495	0.000	0.000	0.005	0.925
Spike	0.625	0.540	0.000	0.015	0.882
Anneal	0.000	0.000	0.000	0.000	0.963
Memory-aware behavior

This repository demonstrates a key capability:

historical memory changes current action selection

Example:

first run stores conflict_event

second run retrieves historical conflict memory

retrieved memory raises 
𝑈
c
o
n
U
con
	​


the chosen action shifts toward Patch

This is the central difference between a memory-backed archive and a memory-aware cognitive controller.

Paper

PDF: TelosCore v1.1 Paper

Architecture

SSOT: Full Memory Architecture

Competition evidence

Checklist: Competition Evidence

Evaluation protocol

Boundary: Evaluation Protocol

Demo video

After recording your 90-second demo, place it in the repository root or docs/ and link it here.

Example:

Watch Demo Video

Citation
@misc{teloscore2026,
  title={TelosCore Full-Memory Build: A Memory-Aware Cognitive Control Layer Powered by EverMemOS},
  author={Liangfeng Hu},
  year={2026},
  howpublished={https://github.com/liangfeng-hu/teloscore-v1.1},
}
<details> <summary><b>中文简介（点击展开）</b></summary>

TelosCore 全量记忆版是一个建立在 EverMemOS 之上的“记忆驱动认知控制层”。

它的关键点不是“把状态存起来”，而是：

把关键事件写入长期记忆

检索历史冲突、澄清、目标事件

用历史记忆修正当前 
𝑈
U 向量

让动作选择真正受到长期记忆影响

当前仓库是全量记忆架构的最小可运行雏形，不是最终产品封板版。
完整理论母版见：docs/FULL_MEMORY_ARCHITECTURE.md

</details>
