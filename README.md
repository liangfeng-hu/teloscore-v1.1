# TelosCore Full-Memory Build

**A memory-aware cognitive control layer powered by EverMemOS**

[![MIT License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-green)](https://fastapi.tiangolo.com/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32-red)](https://streamlit.io/)
![Last Update](https://img.shields.io/github/last-commit/liangfeng-hu/teloscore-v1.1)
[![Stars](https://img.shields.io/github/stars/liangfeng-hu/teloscore-v1.1?style=social)](https://github.com/liangfeng-hu/teloscore-v1.1/stargazers)

## 项目定位

TelosCore Full-Memory Build 是一个建立在 **EverMemOS** 之上的“记忆驱动认知控制层”。

它不是单纯把历史内容存起来，而是把长期记忆真正引入当前裁决过程：历史事件会修正当前认知势能，从而改变动作选择。

核心公式可概括为：

- `U(s) = 1.2 * U_unc + 1.8 * U_con + 1.0 * U_ent + 1.4 * U_tel`
- `u_total = u_current + λ * u_memory`

其中：

- `U_unc`：不确定性
- `U_con`：冲突度
- `U_ent`：熵 / 噪声复杂度
- `U_tel`：目标偏离度
- `u_memory`：从 EverMemOS 检索得到的历史记忆修正量

---

## Powered by EverMemOS

TelosCore 使用 **EverMemOS** 作为持久化记忆底座。

当前仓库主线已经实现：

- State memory 跨会话保存
- Event memory 写入 `conflict_event` / `clarify_event` / `goal_event`
- 从 EverMemOS 检索历史记忆
- 用检索到的历史记忆修正当前 `U`
- 让动作选择从 purely reactive 变成 memory-aware

这意味着本项目的重点不是“更会检索”，而是：

> **历史记忆会真实改变当前动作选择。**

---

## 当前仓库的工程定位

本仓库当前定位为：

**minimal running full-memory prototype**

也就是：
- 已经可以运行
- 已经可以演示“记忆改变决策”
- 已经可以用于比赛提交
- 但并不宣称所有理论层（例如完整审计硬墙、完整两阶段原子写回）都已经工程封板

更完整的理论母版见：

- `docs/FULL_MEMORY_ARCHITECTURE.md`

---

## 仓库内容说明

### 主线文件（比赛主线）
- `telos_core.py` — 主线认知能量计算与动作选择
- `evermemos_client.py` — 主线 EverMemOS 客户端
- `app.py` — 主线 FastAPI 服务入口
- `demo_script.py` — 主线两轮会话演示脚本
- `auto_make_figs.py` — 主线证据图生成器
- `dashboard_pro.py` — 主线 Streamlit 可视化面板
- `requirements.txt` — 主线依赖

### 实验线文件（v1.2 experimental line）
- `telos_core_v1.2.py`
- `evermemos_client_v1.2.py`
- `app_v1.2.py`
- `demo_v1.2.py`
- `auto_make_figs_v1.2.py`
- `requirements_v1.2.txt`
- `locomo_eval_sim.py`

这些文件用于实验性扩展，不影响主线提交。

> 注意：实验线文件当前文件名带有 `v1.2`。  
> 如果你在本地运行时遇到 Python 模块导入问题，建议把它们改名成下划线版，例如：
>
> - `app_v1_2.py`
> - `demo_v1_2.py`
> - `telos_core_v1_2.py`
> - `evermemos_client_v1_2.py`
> - `auto_make_figs_v1_2.py`

### 资源与文档
- `assets/00_triptych.png` — Baseline → Spike → Anneal 证据图
- `docs/TelosCore_v1.1.pdf` — 论文 PDF
- `docs/FULL_MEMORY_ARCHITECTURE.md` — 理论母版 / SSOT
- `docs/COMPETITION_EVIDENCE.md` — 竞赛证据清单
- `docs/EVAL_PROTOCOL.md` — 评估口径边界
- `docs/V1_2_EXPERIMENTAL.md` — v1.2 实验线说明

---

## Quick start（主线）

### 1. 克隆本仓库并安装依赖

```bash
git clone https://github.com/liangfeng-hu/teloscore-v1.1.git
cd teloscore-v1.1
pip install -r requirements.txt
```

### 2. 启动 EverMemOS

本仓库假定 EverMemOS 服务可在本地 `http://localhost:1995` 访问。

你需要先部署并启动官方 EverMemOS。一个常见的本地流程是：

```bash
git clone https://github.com/EverMind-AI/EverMemOS.git
cd EverMemOS
docker compose up -d
```

如果官方仓库的启动方式有更新，请以 EverMemOS 官方 README 为准。

### 3. 启动主线 API

```bash
uvicorn app:app --reload --port 8000
```

### 4. 运行主线 demo

```bash
python demo_script.py
```

### 5. 启动主线 dashboard

```bash
streamlit run dashboard_pro.py
```

---

## Quick start（实验线 v1.2）

如果你要测试实验线，可以使用：

```bash
pip install -r requirements_v1.2.txt
python app_v1.2.py
```

或：

```bash
python demo_v1.2.py
```

如果你本地已把实验线文件改名成下划线版，则使用对应的新文件名运行。

---

## 可复现实验证据

### 证据 1：两轮会话演示
运行：

```bash
python demo_script.py
```

你应当在控制台中观察到类似信息：

- `[Memory Correction] ...`
- `[EverMemOS] state persisted.`
- `[EverMemOS] conflict_event persisted.` 或 `[EverMemOS] clarify_event persisted.`
- `[Decision] Pure Reactive: ... -> Memory-Aware: ...`

这说明：
1. 第一次会话把事件写入 EverMemOS
2. 第二次会话检索到了历史记忆
3. 历史记忆修正了当前 `U`
4. 动作选择因此发生偏移

### 证据 2：证据图
运行：

```bash
python auto_make_figs.py
```

它会生成主线证据图：

- `assets/00_triptych.png`

### 证据 3：论文与理论母版
- 论文：`docs/TelosCore_v1.1.pdf`
- 理论母版：`docs/FULL_MEMORY_ARCHITECTURE.md`

---

## 定量快照（主线）

| Stage    | Total U | Unc. | Confl. | Ent. | Plasticity |
|----------|---------|------|--------|------|------------|
| Baseline | 0.495   | 0.000 | 0.000 | 0.005 | 0.925 |
| Spike    | 0.625   | 0.540 | 0.000 | 0.015 | 0.882 |
| Anneal   | 0.000   | 0.000 | 0.000 | 0.000 | 0.963 |

---

## 记忆感知行为（Memory-aware behavior）

本仓库要证明的关键能力是：

**historical memory changes current action selection**

例子：

- first run stores `conflict_event`
- second run retrieves historical conflict memory
- retrieved memory raises conflict-related `U`
- the chosen action shifts toward `Patch`

这也是一个普通 memory-backed archive 和一个 memory-aware cognitive controller 之间最核心的区别。

---

## 评估边界（非常重要）

本仓库只应当声称以下内容：

- 代码中真实实现的内容
- 公开仓库中可复现的内容
- demo 视频中可直接观察到的内容

本仓库不应当声称以下内容，除非你已经提供公开、可复现、标准化的实验流程：

- 官方 benchmark superiority
- 完整 production sealing of audit / digest / commit layers
- 不可复现的竞赛分数
- 未在公开代码中实现的完整功能

具体边界说明请见：

- `docs/EVAL_PROTOCOL.md`

---

## 竞赛材料入口

- **Paper:** [TelosCore v1.1 Paper](docs/TelosCore_v1.1.pdf)
- **Architecture / SSOT:** [Full Memory Architecture](docs/FULL_MEMORY_ARCHITECTURE.md)
- **Competition Evidence:** [Competition Evidence](docs/COMPETITION_EVIDENCE.md)
- **Evaluation Protocol:** [Evaluation Protocol](docs/EVAL_PROTOCOL.md)

---

## Demo video

录制 90 秒演示视频后，可将文件放在仓库根目录或 `docs/` 中，然后把链接放在这里。

示例：

[Watch Demo Video](demo.mp4)

---

## Citation

```bibtex
@misc{teloscore2026,
  title={TelosCore Full-Memory Build: A Memory-Aware Cognitive Control Layer Powered by EverMemOS},
  author={Liangfeng Hu},
  year={2026},
  howpublished={https://github.com/liangfeng-hu/teloscore-v1.1},
}
```

---

## 中文简介（简版）

TelosCore 全量记忆版是一个建立在 EverMemOS 之上的“记忆驱动认知控制层”。

它的关键点不是“把状态存起来”，而是：

- 把关键事件写入长期记忆
- 检索历史冲突、澄清、目标事件
- 用历史记忆修正当前 U 向量
- 让动作选择真正受到长期记忆影响

当前仓库是全量记忆架构的最小可运行雏形，不是最终产品封板版。  
完整理论母版见：`docs/FULL_MEMORY_ARCHITECTURE.md`

---

If this repo helps, starring it is appreciated.
