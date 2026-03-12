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

- **State memory** is persisted across sessions
- **Event memory** is written as conflict / clarify / goal events
- Retrieved memory **actively modifies U**
- Action selection is therefore **memory-aware**, not purely reactive

This repository is the **minimal running full-memory prototype** of the broader Full-Memory Architecture documented in `docs/FULL_MEMORY_ARCHITECTURE.md`.

---

## What this repo contains
- `telos_core.py` — core cognitive energy computation + action selection
- `evermemos_client.py` — EverMemOS client for state/event memory persistence
- `app.py` — FastAPI server (port 8000)
- `dashboard_pro.py` — Streamlit dashboard
- `demo_script.py` — demo for memory-aware decision shift
- `auto_make_figs.py` — generates the evidence figure
- `assets/00_triptych.png` — Baseline → Spike → Anneal evidence
- `docs/TelosCore_v1.1.pdf` — paper PDF
- `docs/FULL_MEMORY_ARCHITECTURE.md` — full-memory architecture SSOT

---

## Quick start
```bash
git clone https://github.com/liangfeng-hu/teloscore-v1.1.git
cd teloscore-v1.1
pip install -r requirements.txt
Start EverMemOS
docker compose up -d
Run the demo
python demo_script.py
Run the API
uvicorn app:app --reload --port 8000
Run the dashboard
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

Architecture Document

SSOT: Full Memory Architecture

Demo Video

After recording your 90-second demo, place it in the repository root or docs/ and link it here.

Example:
[Watch Demo Video](demo.mp4)
Citation
@misc{teloscore2026,
  title={TelosCore Full-Memory Build: A Memory-Aware Cognitive Control Layer Powered by EverMemOS},
  author={Liangfeng Hu},
  year={2026},
  howpublished={https://github.com/liangfeng-hu/teloscore-v1.1},
}
