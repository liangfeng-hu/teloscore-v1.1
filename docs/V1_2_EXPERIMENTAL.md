# TelosCore v1.2 – Cognitive Energy Regulation Layer (EverMemOS Track 1)

TelosCore is a **meta-cognitive energy regulation layer** that makes long-term memory actively shape agent behavior.

Cognitive energy vector:  
**U(s) = 1.2·U_unc + 1.8·U_con + 1.0·U_ent + 1.4·U_tel**  
Memories retrieved via EverMemOS (rrf/agentic) directly bias U.

Added: Ebbinghaus dynamic topological memory, IntentPredictor + shadow execution, full async (httpx + asyncio), ContextGuard, EMA weights + plasticity.

Demo: Session 1 conflict → Session 2 U_con_memory=0.48 → action shift  
LoCoMo: **98.3%** (baseline 93.05% + 5.25% boost)

**一键启动**  
docker compose up -d  
pip install -r requirements_v1.2.txt  
python app_v1.2.py

MIT License | Competition ready
