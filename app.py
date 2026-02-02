"""
PARLEISITOS v5.0 - Edición Definitiva
Diseño: Dark Mode Premium (Negro + Morado + Neón)
Datos: FotMob Anti-Bloqueo + NBA Live
"""

import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import random
from nba_api.live.nba.endpoints import scoreboard

# ==================== CONFIGURACIÓN DE PÁGINA ====================
st.set_page_config(
    page_title="Parleisitos Pro",
    page_icon="💎",
    layout="mobile", # Optimizado para celular
    initial_sidebar_state="collapsed"
)

# ==================== ESTILOS CSS (DISEÑO DRAFTEA) ====================
st.markdown("""
    <style>
    /* FUENTES Y COLORES GLOBALES */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .stApp {
        background-color: #0b0a14 !important; /* Negro Profundo */
        color: white !important;
    }

    /* TARJETAS CON EFECTO GLASS */
    .bet-card {
        background: linear-gradient(145deg, #1a1b2e 0%, #151621 100%);
        border: 1px solid #2d2f45;
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.5);
        position: relative;
        overflow: hidden;
    }
    
    /* EFECTO DE BRILLO EN TARJETAS */
    .bet-card::before {
        content: "";
        position: absolute;
        top: 0; left: 0; width: 4px; height: 100%;
        background: #6d28d9; /* Borde Izquierdo Morado */
    }

    /* TEXTOS */
    h1, h2, h3 { color: white !important; font-weight: 800 !important; }
    small { color: #94a3b8 !important; }
    
    .neon-text {
        color: #22d3ee !important; /* Cian Neón */
        text-shadow: 0 0 10px rgba(34, 211, 238, 0.4);
        font-weight: 800;
    }
    
    .purple-text {
        color: #a855f7 !important;
        font-weight: bold;
    }

    /* BOTONES ESTILO APP */
    .stButton > button {
        background: linear-gradient(90deg, #6d28d9, #7c3aed) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 12px !important;
        font-weight: 700 !important;
        width: 100% !important;
        box-shadow: 0 4px 15px rgba(109, 40, 217, 0.4);
    }
    
    .stButton > button:active { transform: scale(0.98); }

    /* IMÁGENES CIRCULARES */
    .avatar {
        width: 50px; height: 50px;
        border-radius: 50%;
        border: 2px solid #a855f7;
        object-fit: cover;
    }
    
    /* TABS PERSONALIZADOS */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #1a1b2e;
        border-radius: 20px;
        padding: 8px 16px;
        color: #94a3b8;
        border: 1px solid #2d2f45;
    }
    .stTabs [aria-selected="true"] {
        background-color: #6d28d9 !important;
        color: white !important;
        border-color: #8b5cf6 !important;
    }
    </style>
""", unsafe_allow_html=True)

# ==================== DATABASE DE IMÁGENES ====================
PLAYER_IMGS = {
    "Haaland": "https://resources.premierleague.com/premierleague/photos/players/250x250/p223094.png",
    "Mbappé": "https://img.uefa.com/imgml/TP/players/1/2024/324x324/250076574.jpg",
    "Vinicius": "https://img.uefa.com/imgml/TP/players/1/2024/324x324/250076574.jpg", # Placeholder
    "Messi": "https://a.espncdn.com/combiner/i?img=/i/headshots/soccer/players/full/45843.png",
    "LeBron": "https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/1966.png",
    "Curry": "https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/3975.png",
    "Luka": "https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/3945274.png",
    "Generic": "https://cdn-icons-png.flaticon.com/512/847/847969.png"
}

# ==================== LÓGICA DE DATOS ====================

@st.cache_data(ttl=300)
def get_fotmob_matches(date_str, league_id):
    """
    Obtiene partidos de FotMob con Headers Anti-Bloqueo.
    date_str: Formato YYYYMMDD
    """
    url = f"https://www.fotmob.com/api/matches?date={date_str}"
    
    # HEADERS CRÍTICOS PARA QUE NO TE BLOQUEEN
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json',
        'Referer': 'https://www.fotmob.com/'
    }
    
    try:
        r = requests.get(url, headers=headers, timeout=5)
        if r.status_code == 200:
            data = r.json()
            matches_found = []
            
            # Recorrer ligas
            if 'leagues' in data:
                for league in data['leagues']:
                    # Filtro de ID (0 = Todos, o ID específico)
                    if league_id == 0 or str(league['primaryId']) == str(league_id):
                        for m in league['matches']:
                            matches_found.append({
                                "home": m['home']['name'],
                                "away": m['away']['name'],
                                "time": m['status'].get('startTimeStr', 'HOY'),
                                "score": f"{m['home']['score']} - {m['away']['score']}" if m['status']['started'] else "vs",
                                "league": league['name'],
                                "status": "En Vivo" if m['status']['live'] else "Programado"
                            })
            return matches_found
    except Exception as e:
        st.error(f"Error conectando con FotMob: {e}")
    return []

def get_nba_live():
    try:
        board = scoreboard.ScoreBoard()
        games = board.games.get_dict()
        return games
    except:
        return []

# ==================== INTERFAZ ====================

st.markdown("<h1 style='text-align:center; margin-bottom: 20px;'>💎 PARLEISITOS <span style='font-size:0.5em; color:#a855f7; vertical-align:super;'>PRO</span></h1>", unsafe_allow_html=True)

# NAVEGACIÓN
tabs = st.tabs(["🔥 INICIO", "⚽ FÚTBOL", "🏀 NBA", "🎲 GENERADOR"])

# --- TAB 1: INICIO (PARLEYS RECOMENDADOS) ---
with tabs[0]:
    st.markdown("### ⚡ Jugadas del Día")
    
    # 1. PARLEY ASEGURADO
    st.markdown(f"""
    <div class="bet-card">
        <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
            <span class="purple-text">🛡️ ASEGURADO</span>
            <span style="color:#4ade80; font-weight:bold;">Prob: 92%</span>
        </div>
        <div style="display:flex; align-items:center; gap:15px;">
            <img src="{PLAYER_IMGS['Haaland']}" class="avatar">
            <div style="flex-grow:1;">
                <div style="font-weight:bold; font-size:1.1em;">Erling Haaland</div>
                <small>Man City vs Brentford</small>
            </div>
            <div style="text-align:right;">
                <div class="neon-text" style="font-size:1.4em;">1.35x</div>
                <small>Over 0.5 Tiros</small>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. PARLEY SOÑADOR
    st.markdown(f"""
    <div class="bet-card" style="border: 1px solid #22d3ee;">
        <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
            <span class="neon-text">🦄 SOÑADOR (High Risk)</span>
            <span style="color:#fbbf24; font-weight:bold;">Prob: 35%</span>
        </div>
        <div style="display:flex; align-items:center; gap:15px;">
            <img src="{PLAYER_IMGS['LeBron']}" class="avatar">
            <div style="flex-grow:1;">
                <div style="font-weight:bold; font-size:1.1em;">LeBron James</div>
                <small>Lakers Win + 25 Pts</small>
            </div>
            <div style="text-align:right;">
                <div class="neon-text" style="font-size:1.4em;">4.50x</div>
                <small>Combo NBA</small>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- TAB 2: FÚTBOL (CON DATOS REALES) ---
with tabs[1]:
    # Configuración de búsqueda
    col_a, col_b = st.columns(2)
    with col_a:
        # Selector de Fecha (Default: Hoy)
        fecha_sel = st.date_input("Fecha", datetime.now())
        fecha_str = fecha_sel.strftime("%Y%m%d")
    with col_b:
        # Selector de Liga
        ligas_map = {
            "🌎 Todo el Mundo": 0,
            "🇲🇽 Liga MX": 2244,
            "🇬🇧 Premier League": 47,
            "🇪🇸 La Liga": 87,
            "🇪🇺 Champions": 42
        }
        liga_sel = st.selectbox("Liga", list(ligas_map.keys()))

    # Botón para buscar (ayuda a refrescar)
    if st.button("🔄 Buscar Partidos"):
        st.cache_data.clear()
        
    # Obtener datos
    matches = get_fotmob_matches(fecha_str, ligas_map[liga_sel])

    if matches:
        st.caption(f"Se encontraron {len(matches)} partidos.")
        for m in matches:
            # Color del marcador
            score_color = "#22d3ee" if m['status'] == "En Vivo" else "#6d28d9"
            
            st.markdown(f"""
            <div class="bet-card">
                <div style="display:flex; justify-content:space-between; font-size:0.8em; margin-bottom:8px;">
                    <span style="color:#ccc;">{m['league']}</span>
                    <span style="color:#a855f7;">{m['time']}</span>
                </div>
                <div style="display:flex; align-items:center; justify-content:space-between;">
                    <span style="font-weight:bold; font-size:1.1em; width:40%; text-align:right;">{m['home']}</span>
                    <span style="background:#0b0a14; color:{score_color}; padding:5px 12px; border-radius:8px; font-weight:bold;">{m['score']}</span>
                    <span style="font-weight:bold; font-size:1.1em; width:40%; text-align:left;">{m['away']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No se encontraron partidos para esta fecha y liga.")
        st.markdown("**Prueba cambiando la fecha a mañana o seleccionando 'Todo el Mundo'.**")

# --- TAB 3: NBA ---
with tabs[2]:
    st.markdown("### 🏀 NBA Scoreboard")
    games = get_nba_live()
    
    if games:
        for g in games:
            home = g['homeTeam']['teamName']
            away = g['awayTeam']['teamName']
            score = f"{g['homeTeam']['score']} - {g['awayTeam']['score']}"
            
            st.markdown(f"""
            <div class="bet-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div style="display:flex; align-items:center; gap:10px;">
                        <img src="https://cdn.nba.com/logos/nba/{g['homeTeam']['teamId']}/primary/L/logo.svg" width="35">
                        <b>{home}</b>
                    </div>
                    <span class="neon-text" style="font-size:1.2em;">{score}</span>
                    <div style="display:flex; align-items:center; gap:10px;">
                        <b>{away}</b>
                        <img src="https://cdn.nba.com/logos/nba/{g['awayTeam']['teamId']}/primary/L/logo.svg" width="35">
                    </div>
                </div>
                <center><small style="color:#a855f7; margin-top:5px; display:block;">{g['gameStatusText']}</small></center>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("No hay partidos de NBA en este momento.")
        # Simulación Visual
        st.markdown(f"""
        <div class="bet-card" style="opacity:0.6;">
            <div style="display:flex; gap:15px; align-items:center;">
                <img src="{PLAYER_IMGS['Curry']}" class="avatar">
                <div>
                    <b>Stephen Curry</b><br>
                    <small>Esperando próximo partido...</small>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- TAB 4: GENERADOR ---
with tabs[3]:
    st.markdown("### 💎 Armador de Jugadas")
    
    col1, col2 = st.columns(2)
    with col1:
        nivel = st.select_slider("Riesgo", ["Bajo", "Medio", "Alto", "Locura"])
    with col2:
        deporte = st.selectbox("Deporte", ["Mix", "Fútbol", "NBA"])
        
    if st.button("🔮 GENERAR PARLEY"):
        picks = []
        cuota = 0
        
        if nivel == "Bajo":
            picks = [("Real Madrid", "Gana Directo"), ("Haaland", "+0.5 Tiros al arco")]
            cuota = 1.85
        elif nivel == "Alto":
            picks = [("Lakers", "Gana"), ("LeBron", "+25 Pts"), ("América", "Over 2.5 Goles")]
            cuota = 5.20
            
        st.markdown(f"""
        <div class="bet-card" style="border: 1px solid #22d3ee; box-shadow: 0 0 20px rgba(34,211,238,0.2);">
            <center><h3 style="color:#22d3ee !important;">PARLEY {nivel.upper()}</h3></center>
            <hr style="border-color:#333;">
            <div style="margin: 15px 0;">
        """, unsafe_allow_html=True)
        
        for i, p in enumerate(picks, 1):
            st.markdown(f"<p style='margin:5px 0;'>{i}. <b>{p[0]}</b>: {p[1]}</p>", unsafe_allow_html=True)
            
        st.markdown(f"""
            </div>
            <div style="background:#0b0a14; padding:10px; border-radius:10px; display:flex; justify-content:space-between; align-items:center;">
                <span style="color:#a855f7;">Cuota Total:</span>
                <span class="neon-text" style="font-size:1.5em;">{cuota}x</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# FOOTER
st.markdown("<br><center><small>Parleisitos Pro v5.0 | Datos FotMob & NBA API</small></center>", unsafe_allow_html=True)
