\# TelosCore — Cognitive Energy Engine for Memory Agents (2026 Competition Build)



\## 💡 一句话

TelosCore 不是在“更精准检索记忆”，而是在做 \*\*能量驱动的认知调节\*\*：当系统的内部张力升高（不确定/冲突/噪声/目标偏离），它会自动选择最能降低张力的动作（澄清/因果解释/压缩/继续推进）。



\## ❓ 为什么需要它

传统记忆系统越用越像垃圾场：

\*\*存得越多 → 噪声越大 → 冲突越多 → 越容易不稳。\*\*



TelosCore 的做法是：把“记忆系统的健康”变成一个单一能量 U，并让所有行为以降低 U 为目标。



\## 🧮 核心公式



$$U = w\_1 U\_{uncertainty} + w\_2 U\_{conflict} + w\_3 U\_{entropy} + w\_4 U\_{telos}$$



\* \*\*Uncertainty\*\*：不确定性升高 → 触发澄清

\* \*\*Conflict\*\*：矛盾升高 → 触发因果解释式补丁问句

\* \*\*Entropy\*\*：噪声升高 → 触发压缩整理

\* \*\*Telos\*\*：目标偏离升高 → 触发继续推进建议



\## 🏗️ 架构

\* \*\*EverMemOS\*\*：存储/检索“肌肉”（REST API）

\* \*\*TelosCore\*\*：能量计算 + ΔU 动作选择（纯工程实现）

\* \*\*Pro Dashboard\*\*：实时曲线、分量分解、3D 地形演示（评委可一眼理解）



\## 🚀 一键运行



1\. 启动 EverMemOS（默认 1995 端口）

```bash

uv run python src/run.py



2.启动 TelosCore API（8000 端口）

uvicorn app:app --port 8000



3.启动 Pro Dashboard 可视化面板

streamlit run dashboard\_pro.py



4.运行录屏自动脚本（可选）

python demo\_script.py



🎬 Demo 叙事（8 分钟）

1.正常输入 → U 低



2.加入“但是/却/相反” → Conflict 上升 → U 尖峰 → 系统触发 patch



3.加入“也许/不确定” → Uncertainty 上升 → 系统触发 clarify



4.连续废话 → Entropy 上升 → 系统触发 compress



Dashboard 显示：U(t) 从尖峰回落，分量清晰可解释，3D 地形的“山峰”随冲突升高而隆起。



✨ 亮点

新范式：不是 RAG 调参，而是认知热力学式自调节

工程简洁：核心逻辑极短，可读可调

可解释可视化：评委无需看代码就能理解系统行为

兼容生态：可叠加在任何记忆后端之上（这里复用 EverMemOS）


### v1.1 可选增强：Energy-Driven Memory Plasticity（默认关闭）
TelosCore v1.1 允许开启一个可选增强：当系统处于高认知张力（U 较高）时，
本地 fallback 记忆会发生轻量“权重退火”：
- 高冲突/高噪声时：近期记忆权重衰减（降低未来被检索到的概率）
- 目标对齐明显时：近期记忆权重轻度强化
结果：系统越用，越倾向保留低张力、目标相关的记忆片段。

默认 `PLASTICITY=0`（最稳、最易复现）。如需体验自进化，将 `telos_core.py` 顶部 `PLASTICITY=1` 即可。
Dashboard 会显示 `Memory Plasticity` 指标作为可视证据。







