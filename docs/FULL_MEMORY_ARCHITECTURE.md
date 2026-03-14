```markdown
# TelosCore Full-Memory Architecture
**全量记忆认知能量稳定性调节层总方案**

## 1. 总定位

TelosCore Full-Memory Architecture 不是单纯的记忆数据库，也不是单纯的动作选择器，而是一个三层咬合的系统：

1. **EverMemOS 记忆体底座**
   - 负责持久化、跨会话、跨时间窗的记忆保存与检索
2. **TelosCore 认知控制核**
   - 负责把当前输入、历史记忆、冲突模式、目标轨迹统一压到标量势能 \(U\) 上
   - 通过 \(\arg\min \Delta U\) 选择动作
3. **法则与审计层**
   - 由 CanonHeader / DigestGate / PendingLedger / Commit\(_{\mathrm{Unique}}\) 组成
   - 负责可复算、可追溯、可回滚的系统约束

一句话表述：

> EverMemOS 负责“记住”，TelosCore 负责“记住之后如何裁决”，法则层负责“保证这一切可信”。

---

## 2. 五层记忆结构

### 2.1 State Memory（状态记忆层）
记录每一个时刻的内部认知态：

\[
\mathbf{u}_t=
\big(
U_{\mathrm{unc}},
U_{\mathrm{con}},
U_{\mathrm{ent}},
U_{\mathrm{tel}}
\big)_t
\]

并同时记录：
- \(U_t\)：总势能
- \(a_t\)：当前动作
- \(\Delta U_t\)：动作能量差
- \(t\)：时间戳
- \(\sigma_t\)：当前上下文摘要

### 2.2 Event Memory（事件记忆层）
关键事件拆分为：
- `conflict_event`
- `clarify_event`
- `compress_event`
- `respond_event`
- `goal_event`
- `rollback_event`
- `pending_event`

### 2.3 Trajectory Memory（轨迹记忆层）
记录：
- \(\{U_{\mathrm{unc}}(t)\}\)
- \(\{U_{\mathrm{con}}(t)\}\)
- \(\{U_{\mathrm{ent}}(t)\}\)
- \(\{U_{\mathrm{tel}}(t)\}\)
- \(\{a_t\}\)

### 2.4 Pattern Memory（模式记忆层）
从轨迹中提炼：
- `persistent_conflict_pattern`
- `recurring_ambiguity_pattern`
- `entropy_inflation_pattern`
- `telos_drift_pattern`
- `rollback_trigger_pattern`

定义：
\[
\mathcal{P}_t := \Pi_{\mathrm{pattern}}(\mathcal{M}^{\mathrm{traj}}_t)
\]

### 2.5 Audit Memory（审计记忆层）
至少包含：
- `CanonHeader`
- `Transition`
- `EnergyDecision`
- `FlowGate`
- `CommitSeal`
- `EvHash / WindowHash`
- `RollbackReason`
- `PendingLedgerSnapshot`

---

## 3. 统一认知控制律

### 3.1 总势能函数
\[
U(s)=w_1U_{\mathrm{unc}}(s)+w_2U_{\mathrm{con}}(s)+w_3U_{\mathrm{ent}}(s)+w_4U_{\mathrm{tel}}(s)
\]

默认权重：
\[
(w_1,w_2,w_3,w_4)=(1.2,1.8,1.0,1.4)
\]

### 3.2 动作库
\[
\mathcal{A}=
\{\mathrm{Clarify},\mathrm{Patch},\mathrm{Compress},\mathrm{Respond}\}
\]

### 3.3 状态转移与能量差
\[
s_{t+1}=f(s_t,a)
\]

\[
\Delta U(a)=U(f(s_t,a))-U(s_t)
\]

### 3.4 唯一裁决器
\[
a^\*=\arg\min_{a\in\mathcal{A}}\Delta U(a)
\]

---

## 4. 记忆驱动认知动力学

定义当前输入驱动状态：
\[
\mathbf{u}_{\mathrm{current}}
\]

定义历史记忆偏置：
\[
\mathbf{u}_{\mathrm{memory}}=
\big(
U_{\mathrm{unc}}^{(\mathrm{memory})},
U_{\mathrm{con}}^{(\mathrm{memory})},
U_{\mathrm{ent}}^{(\mathrm{memory})},
U_{\mathrm{tel}}^{(\mathrm{memory})}
\big)
\]

则总态为：
\[
\mathbf{u}_{\mathrm{total}}
=
\mathbf{u}_{\mathrm{current}}
+
\lambda \mathbf{u}_{\mathrm{memory}}
\]

### 4.1 记忆修正规则
- 历史冲突模式密集 → 抬高 \(U_{\mathrm{con}}\)
- 历史澄清失败反复出现 → 抬高 \(U_{\mathrm{unc}}\)
- 冗余噪声模式累积 → 抬高 \(U_{\mathrm{ent}}\)
- 长期目标轨迹稳定 → 拉低 \(U_{\mathrm{tel}}\)
- 长期目标持续漂移 → 抬高 \(U_{\mathrm{tel}}\)

---

## 5. EffectModelSpec（动作偏移模型）

定义动作位移：
\[
\delta(a)=
\big(
\delta_{a,\mathrm{unc}},
\delta_{a,\mathrm{con}},
\delta_{a,\mathrm{ent}},
\delta_{a,\mathrm{tel}}
\big)
\]

固定偏移矩阵：
\[
\mathbf{M}_{\mathrm{effect}}=
\begin{bmatrix}
-0.30&+0.10&+0.05&-0.10\\
-0.10&-0.40&+0.10&-0.20\\
+0.05&+0.05&-0.30&+0.05\\
-0.05&+0.05&+0.10&-0.40
\end{bmatrix}
\]

状态更新：
\[
\mathbf{u}(s_{t+1})=
\mathrm{clamp}\big(
\mathbf{u}(s_t)+\delta(a),0,1
\big)
\]

\[
U(s)=\mathbf{w}^\top \mathbf{u}(s)
\]

\[
\Delta U(a)=U(s_{t+1})-U(s_t)
\]

\[
a^\*=\arg\min_{a\in\mathcal{A}}\Delta U(a)
\]

零负步触发：
\[
\forall a\in\mathcal{A}:\Delta U(a)\ge 0
\Rightarrow
I_{\mathrm{FLOW}}=+\infty
\Rightarrow
\Gamma\rightarrow\Gamma_0
\]

---

## 6. Annealing（退火可塑性）
\[
W_{\mathrm{new}}
=
W_{\mathrm{old}}
\cdot
\exp\left(-\eta\cdot \max(0,U-\tau)\right)
\]

默认参数：
\[
\tau=1.10,\qquad \eta=0.14,\qquad K=30
\]

---

## 7. 法则层：硬墙、审计与回滚

### 7.1 PENDING 总阀门
\[
\Xi_{\mathrm{PEND}}(\Gamma)=
\mathbf{1}[\exists X:\mathrm{PENDING}(X)=1]
\]

\[
I_{\mathrm{PENDING}}=
\begin{cases}
0,&\Xi_{\mathrm{PEND}}=0\\
+\infty,&\Xi_{\mathrm{PEND}}=1
\end{cases}
\]

### 7.2 Digest Gate
\[
\mathrm{DigestOK}(h)
\Longleftrightarrow
\mathrm{LenHex}(h)=64
\wedge
\mathrm{RegexHex}(h)=1
\]

\[
I_{\mathrm{DIGEST}}=
\mathbf{1}\big[\forall h\in\mathrm{DigestSet}:\mathrm{DigestOK}(h)=1\big]
\]

### 7.3 统一硬墙
\[
I_{\mathrm{FLOW}}=
I_{\mathrm{LEDGER}}
+
I_{\mathrm{PENDING}}
+
I_{\mathrm{DIGEST}}
+
I_{\mathrm{PQC}}
+
\sum I_X
\]

\[
I_{\mathrm{FLOW}}=+\infty
\Rightarrow
\Gamma\rightarrow\Gamma_0
\]

---

## 8. CanonHeader 与证据闭包

### 8.1 CanonHeader 六字段
\[
\mathrm{CanonHeader}:=
(
\mathrm{CanonVersion},
\mathrm{FieldOrder},
\mathrm{WhitespaceNorm},
\mathrm{ListSortRule},
\mathrm{UnitsDeclared},
\mathrm{StatConvention}
)
\]

所有：
- `EvHash`
- `WindowHash`
- `SSOT_Hash`
- `AuditRec`

必须绑定同一 CanonHeader。

---

## 9. Commit_Unique（唯一写回针）

### 9.1 两阶段写回
**Phase 1: Staging**
\[
\mathrm{WAL}_t:=
\langle
\widetilde{\Gamma}_t,
\mathrm{ReceiptCard}^{\mathrm{FLOW}},
\mathrm{AuditRec}_t
\rangle
\]

**Phase 2: Pointer Swap**
\[
I_{\mathrm{FLOW}}=0
\Rightarrow
\Gamma_{t+1}\leftarrow \widetilde{\Gamma}_t
\wedge
\mathrm{Commit}_{\mathrm{Unique}}=1
\]

### 9.2 回滚闭包
\[
I_{\mathrm{FLOW}}\ne 0
\Rightarrow
\mathrm{Drop}(\mathrm{WAL}_t)
\wedge
\Gamma\rightarrow\Gamma_0
\wedge
\mathrm{Log}(\mathrm{ReasonCode})
\]

---

## 10. 当前工程定位（诚实口径）

本仓库当前工程版为：

**TelosCore Full-Memory Build (minimal running prototype)**

已经工程落地：
- State memory
- Event memory
- EverMemOS persistence
- Memory-aware U correction
- Minimal pattern stub

尚未完全工程落地：
- Full CanonHeader enforcement
- Full DigestGate verification
- Full Commit\(_{\mathrm{Unique}}\) atomic write
- TrainRec / RCS / PQC / FOES closure

---

## 11. 当前 Pending（诚实保留）

- PEND-011：TrainRecSchema
- PEND-012：RCSSchema
- PEND-013：Pattern Consolidation Engine
- PEND-014：PQC / FOES certificate closure
- PEND-015：Dev-Orchestrator-Ω product line

统一 Pending 语义：
\[
I_X=+\infty
\Rightarrow
I_{\mathrm{FLOW}}=+\infty
\Rightarrow
\Gamma\rightarrow\Gamma_0
\]

---

## 12. 最终结论

TelosCore Full-Memory Build 的本质不是“更会存”，而是：

> 让长期记忆真正进入势能计算、动作裁决、审计闭环与回滚逻辑。

这就是它相对于普通 memory-backed agent 的根本区别。
