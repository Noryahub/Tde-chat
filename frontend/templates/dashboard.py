import sys
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(BASE_DIR)

import streamlit as st
from backend.app.services.conversation_service import (
    get_analytics,
    get_signalements
)

import plotly.express as px
import pandas as pd

st.set_page_config(
    page_title="Dashboard TDE",
    page_icon="",
    layout="wide"
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif !important;
}

#MainMenu, footer, header {
    visibility: hidden;
}

.metric-card {
    background: white;
    border-radius: 12px;
    padding: 20px;
    border: 0.5px solid rgba(0,0,0,.1);
    text-align: center;
}

.metric-value {
    font-size: 32px;
    font-weight: 600;
    color: #1D9E75;
}

.metric-label {
    font-size: 13px;
    color: #6b6b67;
    margin-top: 4px;
}

.section-title {
    font-size: 16px;
    font-weight: 500;
    color: #1a1a18;
    margin: 24px 0 12px;
    border-left: 3px solid #1D9E75;
    padding-left: 10px;
}

.badge-nouveau {
    background: #FEF3C7;
    color: #92400E;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 12px;
}

.badge-en_cours {
    background: #DBEAFE;
    color: #1E40AF;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 12px;
}

.badge-resolu {
    background: #D1FAE5;
    color: #065F46;
    padding: 2px 8px;
    border-radius: 4px;
    font-size: 12px;
}
</style>
""", unsafe_allow_html=True)

# ── HEADER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:#1D9E75; border-radius:14px; padding:16px 20px; margin-bottom:24px;">
    <h2 style="color:white; margin:0; font-size:20px;">
        Dashboard Analytique — TDE Chatbot
    </h2>
    <p style="color:rgba(255,255,255,.75); margin:4px 0 0; font-size:13px;">
        Suivi des interactions et indicateurs de performance
    </p>
</div>
""", unsafe_allow_html=True)

# ── CHARGEMENT DONNÉES ─────────────────────────────────────────────────────────
analytics = get_analytics() or {}
signalements = get_signalements(limit=20) or []

# ── DONNÉES SÉCURISÉES ────────────────────────────────────────────────────────
top_intents = analytics.get("top_intents", [])
top_intent = top_intents[0] if top_intents else {}

top_localisations = analytics.get("top_localisations", [])
top_loc = top_localisations[0] if top_localisations else {}

total_conversations = analytics.get("total_conversations", 0)

# ── KPI CARDS ──────────────────────────────────────────────────────────────────
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value">{total_conversations}</div>
        <div class="metric-label">Conversations totales</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="font-size:18px;">
            {top_intent.get('intent', '—').replace('_', ' ')}
        </div>
        <div class="metric-label">Intent le plus fréquent</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="font-size:24px;">
            {top_loc.get('localisation', '—')}
        </div>
        <div class="metric-label">Zone la plus active</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-value" style="color:#E53E3E;">
            {analytics.get('signalements_nouveaux', 0)}
        </div>
        <div class="metric-label">Signalements en attente</div>
    </div>
    """, unsafe_allow_html=True)

# ── GRAPHIQUES ─────────────────────────────────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:

    st.markdown(
        '<div class="section-title">Répartition des intentions</div>',
        unsafe_allow_html=True
    )

    if top_intents:

        df_intents = pd.DataFrame(top_intents)

        df_intents["intent"] = (
            df_intents["intent"]
            .astype(str)
            .str.replace("_", " ")
        )

        fig = px.bar(
            df_intents,
            x="count",
            y="intent",
            orientation="h",
            color_discrete_sequence=["#1D9E75"],
            labels={
                "count": "Nombre",
                "intent": ""
            }
        )

        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            height=250,
            plot_bgcolor="white",
            paper_bgcolor="white"
        )

        st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("Pas encore de données")

with col_right:

    st.markdown(
        '<div class="section-title">Zones les plus touchées</div>',
        unsafe_allow_html=True
    )

    if top_localisations:

        df_locs = pd.DataFrame(top_localisations)

        fig2 = px.pie(
            df_locs,
            values="count",
            names="localisation",
            color_discrete_sequence=px.colors.sequential.Greens_r
        )

        fig2.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            height=250
        )

        st.plotly_chart(fig2, use_container_width=True)

    else:
        st.info("Pas encore de données")

# ── EVOLUTION CONVERSATIONS ────────────────────────────────────────────────────
st.markdown(
    '<div class="section-title">Évolution des conversations (7 derniers jours)</div>',
    unsafe_allow_html=True
)

conv_jour = analytics.get("conversations_par_jour", [])

if conv_jour:

    df_conv = pd.DataFrame(conv_jour)

    fig3 = px.line(
        df_conv,
        x="jour",
        y="count",
        color_discrete_sequence=["#1D9E75"],
        markers=True,
        labels={
            "jour": "Date",
            "count": "Conversations"
        }
    )

    fig3.update_layout(
        margin=dict(l=0, r=0, t=0, b=0),
        height=220,
        plot_bgcolor="white",
        paper_bgcolor="white"
    )

    st.plotly_chart(fig3, use_container_width=True)

else:
    st.info("Pas encore de données")

# ── PROBLEMES FREQUENTS ────────────────────────────────────────────────────────
col_prob, col_sig = st.columns(2)

with col_prob:
    st.markdown('<div class="section-title">Problèmes les plus fréquents</div>',
                unsafe_allow_html=True)
    top_prob = analytics.get('top_problemes', [])
    if top_prob:
        df_prob = pd.DataFrame(top_prob)
        total = analytics.get('total_conversations', 1)
        for _, row in df_prob.iterrows():
            pct = int(row['count'] / total * 100) if total > 0 else 0
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.write(f"⚠️ {row['probleme']}")
            with col_b:
                st.write(f"**{row['count']}** ({pct}%)")
            st.divider()
    else:
        st.info("Pas encore de données")

with col_sig:
    st.markdown('<div class="section-title">Derniers signalements</div>',
                unsafe_allow_html=True)
    if signalements:
        for s in signalements[:8]:
            date_str = str(s['created_at'])[:16] if s['created_at'] else "—"
            col_a, col_b = st.columns([3, 1])
            with col_a:
                st.write(f"📍 {s['localisation'] or '—'} — {s['probleme'] or '—'}")
                st.caption(date_str)
            with col_b:
                statut = s['statut']
                if statut == 'nouveau':
                    st.warning(statut)
                elif statut == 'en_cours':
                    st.info(statut)
                else:
                    st.success(statut)
            st.divider()
    else:
        st.info("Aucun signalement")

# ── REFRESH ────────────────────────────────────────────────────────────────────
st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

if st.button("Actualiser"):
    st.rerun()

