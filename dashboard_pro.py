# dashboard_pro.py
import streamlit as st
import requests
import numpy as np
import plotly.graph_objects as go

API_URL = "http://localhost:8000/interact"

st.set_page_config(layout="wide")
st.title("🧠 TelosCore Pro Dashboard — Cognitive Energy Engine (v1.1)")

if "energy" not in st.session_state:
    st.session_state.energy = []
if "comp" not in st.session_state:
    st.session_state.comp = []
if "actions" not in st.session_state:
    st.session_state.actions = []
if "plasticity" not in st.session_state:
    st.session_state.plasticity = []

left, right = st.columns([2, 1])

with left:
    msg = st.text_input("输入消息（制造：矛盾/不确定/噪声/目标）", "")
    if st.button("发送"):
        if msg.strip():
            r = requests.post(API_URL, json={"message": msg}, timeout=10)
            data = r.json()

            st.session_state.energy.append(data["energy"])
            st.session_state.comp.append(data["components"])
            st.session_state.actions.append(data["action"])
            st.session_state.plasticity.append(data.get("plasticity_score", 1.0))

            st.subheader("系统回应")
            st.write(data["response"])
            st.caption(
                f"action={data['action']} | ΔU={data['delta_U']} | "
                f"phase={data['phase']} | ctx={data['context_size']} | "
                f"plasticity={data.get('plasticity_score', 1.0)}"
            )

with right:
    if st.session_state.comp:
        c = st.session_state.comp[-1]
        st.metric("Total U", c["total"])
        st.metric("Uncertainty", c["uncertainty"])
        st.metric("Conflict", c["conflict"])
        st.metric("Entropy", c["entropy"])
        st.metric("Telos", c["telos"])

        # v1.1新增
        st.metric("Memory Plasticity", st.session_state.plasticity[-1] if st.session_state.plasticity else 1.0)

    if st.session_state.actions:
        st.write("最近动作")
        for a in st.session_state.actions[-8:][::-1]:
            st.write(f"- {a}")

st.divider()

c1, c2 = st.columns(2)

with c1:
    st.subheader("Energy Curve")
    if st.session_state.energy:
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=st.session_state.energy, mode="lines+markers"))
        fig.update_layout(height=360, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Energy Breakdown")
    if st.session_state.comp:
        keys = ["uncertainty", "conflict", "entropy", "telos"]
        fig = go.Figure()
        for k in keys:
            fig.add_trace(go.Scatter(y=[x[k] for x in st.session_state.comp], mode="lines", name=k))
        fig.update_layout(height=360, margin=dict(l=10, r=10, t=40, b=10))
        st.plotly_chart(fig, use_container_width=True)

st.divider()

st.subheader("3D Potential Landscape (Demo Visual)")
conf = st.session_state.comp[-1]["conflict"] if st.session_state.comp else 0.0
unc = st.session_state.comp[-1]["uncertainty"] if st.session_state.comp else 0.0

x = np.linspace(-1.8, 1.8, 60)
y = np.linspace(-1.8, 1.8, 60)
X, Y = np.meshgrid(x, y)

Z_base = 0.35 * (X**2 + Y**2)
Z_barrier = (conf + 0.7 * unc) * np.exp(-(X**2 + Y**2) * 3.8)
Z = Z_base + Z_barrier

fig3d = go.Figure(data=[go.Surface(x=X, y=Y, z=Z, showscale=False)])
fig3d.update_layout(height=520, margin=dict(l=10, r=10, t=40, b=10))
st.plotly_chart(fig3d, use_container_width=True)

st.caption("v1.1：可选启用 Memory Plasticity（能量驱动的记忆权重演化）。默认关闭确保稳定复现。")