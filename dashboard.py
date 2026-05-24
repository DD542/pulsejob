import streamlit as st
import plotly.graph_objects as go
from database import get_toutes_offres
from nlp_engine import (
    analyser_competences,
    analyser_localisations,
    analyser_entreprises,
    analyser_contrats
)

st.set_page_config(
    page_title="PulseJob",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600&family=DM+Mono:wght@400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
        background-color: #0f0f0f;
        color: #e8e8e8;
    }
    .stApp { background-color: #0f0f0f; }
    .header-block {
        padding: 48px 0 32px 0;
        border-bottom: 1px solid #222;
        margin-bottom: 40px;
    }
    .header-label {
        font-family: 'DM Mono', monospace;
        font-size: 11px;
        letter-spacing: 3px;
        color: #555;
        text-transform: uppercase;
        margin-bottom: 12px;
    }
    .header-title {
        font-size: 36px;
        font-weight: 600;
        color: #f0f0f0;
        letter-spacing: -0.5px;
        margin-bottom: 8px;
    }
    .header-sub {
        font-size: 14px;
        color: #555;
        font-weight: 300;
    }
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 1px;
        background: #1a1a1a;
        border: 1px solid #1a1a1a;
        margin-bottom: 40px;
    }
    .kpi-card {
        background: #0f0f0f;
        padding: 28px 24px;
    }
    .kpi-label {
        font-family: 'DM Mono', monospace;
        font-size: 10px;
        letter-spacing: 2px;
        color: #444;
        text-transform: uppercase;
        margin-bottom: 12px;
    }
    .kpi-value {
        font-size: 40px;
        font-weight: 600;
        color: #e8e8e8;
        letter-spacing: -1px;
        line-height: 1;
    }
    .kpi-unit {
        font-size: 13px;
        color: #444;
        margin-top: 6px;
        font-weight: 300;
    }
    .section-title {
        font-family: 'DM Mono', monospace;
        font-size: 10px;
        letter-spacing: 3px;
        color: #444;
        text-transform: uppercase;
        margin-bottom: 20px;
        padding-bottom: 12px;
        border-bottom: 1px solid #1a1a1a;
    }
    .custom-divider {
        height: 1px;
        background: #1a1a1a;
        margin: 40px 0;
    }
    .footer-block {
        margin-top: 60px;
        padding-top: 24px;
        border-top: 1px solid #1a1a1a;
        font-family: 'DM Mono', monospace;
        font-size: 11px;
        color: #333;
        display: flex;
        justify-content: space-between;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 0;
        padding-bottom: 40px;
        max-width: 1400px;
    }
    .stTextInput input {
        background: #141414 !important;
        border: 1px solid #222 !important;
        color: #e8e8e8 !important;
        border-radius: 0 !important;
        font-family: 'DM Mono', monospace !important;
        font-size: 13px !important;
    }
</style>
""", unsafe_allow_html=True)

# Chargement données
df = get_toutes_offres()
top_competences = analyser_competences()
top_villes = analyser_localisations()
top_entreprises = analyser_entreprises()
contrats = analyser_contrats()

# Nettoyage des termes parasites
MOTS_EXCLUS = [
    "r", "age automatique", "ntissage profond",
    "nce des donn", "lyste de donn", "erie des donn",
    "age des donn", "java"
]
top_competences = top_competences[
    ~top_competences["competence"].apply(
        lambda x: any(mot in str(x) for mot in MOTS_EXCLUS)
    )
].reset_index(drop=True)

top_ent_filtre = top_entreprises[
    top_entreprises["entreprise"] != "Non précisé"
].head(10)

PLOT_CONFIG = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color="#555", size=12),
    margin=dict(l=0, r=0, t=30, b=0),
    showlegend=False
)

# Header
st.markdown("""
<div class="header-block">
    <div class="header-label">France Travail API — Données temps réel</div>
    <div class="header-title">PulseJob</div>
    <div class="header-sub">Observatoire du marché Data & Intelligence Artificielle en France</div>
</div>
""", unsafe_allow_html=True)

# KPIs
st.markdown(f"""
<div class="kpi-grid">
    <div class="kpi-card">
        <div class="kpi-label">Offres analysées</div>
        <div class="kpi-value">{len(df):,}</div>
        <div class="kpi-unit">offres collectées</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Villes couvertes</div>
        <div class="kpi-value">{df["localisation"].nunique()}</div>
        <div class="kpi-unit">zones géographiques</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Entreprises</div>
        <div class="kpi-value">{df[df["entreprise"] != "Non précisé"]["entreprise"].nunique()}</div>
        <div class="kpi-unit">recruteurs identifiés</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-label">Compétences</div>
        <div class="kpi-value">{len(top_competences)}</div>
        <div class="kpi-unit">technologies détectées</div>
    </div>
</div>
""", unsafe_allow_html=True)

# Ligne 1
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="section-title">Compétences les plus demandées</div>', unsafe_allow_html=True)
    data_comp = top_competences.head(15)
    fig1 = go.Figure(go.Bar(
        x=data_comp["occurences"],
        y=data_comp["competence"],
        orientation="h",
        marker=dict(
            color=data_comp["occurences"],
            colorscale=[[0, "#1a1a1a"], [1, "#e8e8e8"]],
            line=dict(width=0)
        ),
        text=data_comp["occurences"],
        textposition="outside",
        textfont=dict(family="DM Mono", size=11, color="#444")
    ))
    fig1.update_layout(
        **PLOT_CONFIG,
        yaxis=dict(autorange="reversed", tickfont=dict(size=12, color="#888"), gridcolor="#111"),
        xaxis=dict(showgrid=False, showticklabels=False),
        height=450
    )
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.markdown('<div class="section-title">Concentration géographique</div>', unsafe_allow_html=True)
    data_villes = top_villes.head(10)
    fig2 = go.Figure(go.Bar(
        x=data_villes["nombre_offres"],
        y=data_villes["ville"],
        orientation="h",
        marker=dict(
            color=data_villes["nombre_offres"],
            colorscale=[[0, "#1a1a1a"], [1, "#c8b89a"]],
            line=dict(width=0)
        ),
        text=data_villes["nombre_offres"],
        textposition="outside",
        textfont=dict(family="DM Mono", size=11, color="#444")
    ))
    fig2.update_layout(
        **PLOT_CONFIG,
        yaxis=dict(autorange="reversed", tickfont=dict(size=12, color="#888"), gridcolor="#111"),
        xaxis=dict(showgrid=False, showticklabels=False),
        height=450
    )
    st.plotly_chart(fig2, use_container_width=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# Ligne 2
col3, col4 = st.columns(2)

with col3:
    st.markdown('<div class="section-title">Top recruteurs</div>', unsafe_allow_html=True)
    fig3 = go.Figure(go.Bar(
        x=top_ent_filtre["nombre_offres"],
        y=top_ent_filtre["entreprise"],
        orientation="h",
        marker=dict(
            color=top_ent_filtre["nombre_offres"],
            colorscale=[[0, "#1a1a1a"], [1, "#a8c4a2"]],
            line=dict(width=0)
        ),
        text=top_ent_filtre["nombre_offres"],
        textposition="outside",
        textfont=dict(family="DM Mono", size=11, color="#444")
    ))
    fig3.update_layout(
        **PLOT_CONFIG,
        yaxis=dict(autorange="reversed", tickfont=dict(size=12, color="#888"), gridcolor="#111"),
        xaxis=dict(showgrid=False, showticklabels=False),
        height=380
    )
    st.plotly_chart(fig3, use_container_width=True)

with col4:
    st.markdown('<div class="section-title">Types de contrats</div>', unsafe_allow_html=True)
    fig4 = go.Figure(go.Pie(
        labels=contrats["type_contrat"],
        values=contrats["nombre"],
        hole=0.65,
        marker=dict(
            colors=["#e8e8e8", "#333", "#555", "#777", "#999", "#bbb"],
            line=dict(color="#0f0f0f", width=2)
        ),
        textfont=dict(family="DM Mono", size=11, color="#888"),
        textinfo="label+percent"
    ))
    fig4.update_layout(**PLOT_CONFIG, height=380)
    st.plotly_chart(fig4, use_container_width=True)

st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

# Table
st.markdown('<div class="section-title">Explorer les offres</div>', unsafe_allow_html=True)
recherche = st.text_input(
    "Recherche",
    placeholder="Filtrer par mot clé — titre, entreprise, ville...",
    label_visibility="collapsed"
)

if recherche:
    masque = df.apply(lambda row: recherche.lower() in str(row).lower(), axis=1)
    df_filtre = df[masque]
else:
    df_filtre = df

st.dataframe(
    df_filtre[["titre", "entreprise", "localisation", "type_contrat", "experience", "date_publication"]].head(50),
    use_container_width=True,
    hide_index=True
)

# Footer
st.markdown(f"""
<div class="footer-block">
    <span>PulseJob — Dylan Menga Wanda — ECE Paris B3 Data & IA</span>
    <span>{len(df)} offres — Source France Travail API</span>
</div>
""", unsafe_allow_html=True)