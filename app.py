import streamlit as st
import pandas as pd
import requests
from datetime import datetime
from nba_api.live.nba.endpoints import scoreboard

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Parleisitos Pro", page_icon="🟣", layout="centered")

# --- CSS ESTILO DRAFTEA (Morado/Negro/Neón) ---
st.markdown("""
    <style>
    /* Fondo General */
    .stApp {
        background-color: #0b0a14 !important;
        color: white !important;
    }
    
    /* Eliminar padding extra de Streamlit */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 5rem;
    }

    /* Tarjetas de Apuestas */
    .bet-card {
        background: linear-gradient(145deg, #1a1b2e, #151621);
        border: 1px solid #2d2f45;
        border-radius: 16px;
        padding: 15px;
        margin-bottom: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        color: white;
    }

    /* Botones Morados */
    .stButton > button {
        background-color: #6d28d9 !important;
        color: white !important;
        border-radius: 12px;
        border: none;
        font-weight: bold;
        width: 100%;
        padding: 10px;
    }
    .stButton > button:hover {
        background-color: #7c3aed !important;
    }

    /* Textos Neón */
    .neon-text {
        color: #22d3ee;
        font-weight: bold;
        text-shadow: 0 0 5px rgba(34, 211, 238, 0.3);
    }
    
    .profit-text {
        color: #4ade80; /* Verde Ganancia */
        font-weight: bold;
    }

    /* Imágenes Circulares */
    .player-img {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        object-fit: cover;
        border: 2px solid #6d28d9;
        margin-right: 10px;
    }
    
    /* Selectores */
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #1a1b2e !important;
        color: white !important;
        border-color: #5b21b6 !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- BASE DE DATOS DE IMÁGENES ---
PLAYER_IMGS = {
    "Haaland": "https://resources.premierleague.com/premierleague/photos/players/250x250/p223094.png",
    "Salah": "https://resources.premierleague.com/premierleague/photos/players/250x250/p118748.png",
    "Bellingham": "https://img.uefa.com/imgml/TP/players/1/2024/324x324/250106631.jpg",
    "Vinicius": "https://img.uefa.com/imgml/TP/players/1/2024/324x324/250076574.jpg",
    "Messi": "https://a.espncdn.com/combiner/i?img=/i/headshots/soccer/players/full/45843.png",
    "LeBron": "https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/1966.png",
    "Curry": "https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/3975.png",
    "Luka": "https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/3945274.png",
    "Generic": "https://cdn-icons-png.flaticon.com/512/847/847969.png"
}

# --- FUNCIONES DE DATOS ---

@st.cache_data(ttl=300)
def get_fotmob_data(league_id):
    # FECHA REAL DINÁMICA (Para evitar error 2026)
    hoy = datetime.now().strftime('%Y%m%d')
    url = f"https://www.fotmob.com/api/matches?date={hoy}"
    
    try:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
        if r.status_code == 200:
            data = r.json()
            matches = []
            for league in data.get('leagues', []):
                # Si league_id es 0 trae todos, si no, filtra
                if league_id == 0 or str(league['primaryId']) == str(league_id):
                    for m in league['matches']:
                        matches.append({
                            "home": m['home']['name'],
                            "away": m['away']['name'],
                            "time": m['status'].get('startTimeStr', 'Live'),
                            "score": f"{m['home']['score']} - {m['away']['score']}" if m['status']['started'] else "vs",
                            "league": league['name']
                        })
            return matches
    except:
        pass
    return []

def get_nba_data():
    try:
        board = scoreboard.ScoreBoard()
        games = board.games.get_dict()
        return games
    except:
        return []

# --- INTERFAZ ---

st.markdown("<h1 style='text-align:center; color:#a855f7;'>🟣 PARLEISITOS</h1>", unsafe_allow_html=True)

tabs = st.tabs(["🔥 INICIO", "⚽ FÚTBOL", "🏀 NBA", "💎 PARLEY"])

# --- TAB 1: INICIO ---
with tabs[0]:
    st.markdown("### ⚡ Recomendados del Día")
    
    # Parley Asegurado
    st.markdown(f"""
    <div class="bet-card">
        <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
            <span style="color:#a855f7; font-weight:bold;">🛡️ PARLEY ASEGURADO</span>
            <span class="profit-text">Prob: 92%</span>
        </div>
        <div style="display:flex; align-items:center;">
            <img src="{PLAYER_IMGS['Haaland']}" class="player-img">
            <div>
                <div style="font-weight:bold;">Erling Haaland</div>
                <div style="color:#ccc; font-size:0.9em;">+0.5 Tiros al Arco</div>
            </div>
            <div style="margin-left:auto;">
                <span class="neon-text" style="font-size:1.2em;">1.35x</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Parley Soñador
    st.markdown(f"""
    <div class="bet-card" style="border: 1px solid #a855f7;">
        <div style="display:flex; justify-content:space-between; margin-bottom:10px;">
            <span style="color:#22d3ee; font-weight:bold;">🦄 PARLEY SOÑADOR</span>
            <span class="profit-text">Prob: 35%</span>
        </div>
        <div style="display:flex; align-items:center;">
            <img src="{PLAYER_IMGS['LeBron']}" class="player-img">
            <div>
                <div style="font-weight:bold;">Lakers Win + LeBron 30pts</div>
                <div style="color:#ccc; font-size:0.9em;">NBA Combo</div>
            </div>
            <div style="margin-left:auto;">
                <span class="neon-text" style="font-size:1.2em;">4.50x</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- TAB 2: FÚTBOL ---
with tabs[1]:
    # Mapa de IDs de FotMob
    ligas = {"🇬🇧 Premier": 47, "🇪🇸 La Liga": 87, "🇲🇽 Liga MX": 2244, "🇮🇹 Serie A": 55, "🇪🇺 Champions": 42}
    sel_liga = st.selectbox("Selecciona Liga:", list(ligas.keys()))
    
    matches = get_fotmob_data(ligas[sel_liga])
    
    if matches:
        for m in matches:
            st.markdown(f"""
            <div class="bet-card">
                <div style="display:flex; justify-content:space-between; font-size:0.8em; color:#888;">
                    <span>{m['league']}</span>
                    <span>{m['time']}</span>
                </div>
                <div style="display:flex; justify-content:space-between; align-items:center; margin-top:10px;">
                    <span style="font-weight:bold; font-size:1.1em;">{m['home']}</span>
                    <span style="background:#0b0a14; padding:5px 10px; border-radius:8px; color:#22d3ee; font-weight:bold;">{m['score']}</span>
                    <span style="font-weight:bold; font-size:1.1em;">{m['away']}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info(f"No hay partidos programados hoy para {sel_liga} (o están en descanso).")
        # Ejemplo Visual para que no se vea vacío
        st.markdown(f"""
        <div class="bet-card" style="opacity:0.7;">
            <center>
                <div>⚽ Próximo Partido Destacado</div>
                <h3>Real Madrid vs Barcelona</h3>
                <span class="neon-text">Mañana 14:00 PM</span>
            </center>
        </div>
        """, unsafe_allow_html=True)

# --- TAB 3: NBA ---
with tabs[2]:
    st.markdown("### 🏀 NBA Scoreboard")
    games = get_nba_data()
    
    if games:
        for g in games:
            home = g['homeTeam']['teamName']
            away = g['awayTeam']['teamName']
            score = f"{g['homeTeam']['score']} - {g['awayTeam']['score']}"
            status = g['gameStatusText']
            
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
                <center><small style="color:#a855f7;">{status}</small></center>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="bet-card">
            <div style="display:flex; align-items:center;">
                <img src="{PLAYER_IMGS['Curry']}" class="player-img">
                <div>
                    <b>Stephen Curry</b>
                    <div style="font-size:0.9em; color:#ccc;">Props Disponibles: +4.5 Triples</div>
                </div>
                <div style="margin-left:auto;">
                    <span class="neon-text">Ver Picks</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.warning("No hay partidos en vivo ahora mismo.")

# --- TAB 4: GENERADOR ---
with tabs[3]:
    st.markdown("### 💎 Armar Parley")
    
    col1, col2 = st.columns(2)
    with col1:
        nivel = st.selectbox("Riesgo", ["Asegurado", "Medio", "Soñador"])
    with col2:
        deporte = st.selectbox("Deporte", ["Mix", "Fútbol", "NBA"])
        
    if st.button("GENERAR JUGADA"):
        st.markdown(f"""
        <div class="bet-card" style="border: 2px solid #a855f7; box-shadow: 0 0 15px rgba(168, 85, 247, 0.4);">
            <center><h3 style="color:#22d3ee !important; margin:0;">PARLEY {nivel.upper()}</h3></center>
            <hr style="border-color:#333;">
            <div style="margin: 10px 0;">
                <p>1. ⚽ <b>América:</b> Over 1.5 Goles</p>
                <p>2. 🏀 <b>Luka Doncic:</b> +8.5 Asistencias</p>
                <p>3. ⚽ <b>Man City:</b> Gana Directo</p>
            </div>
            <div style="background:#0b0a14; padding:10px; border-radius:10px; display:flex; justify-content:space-between;">
                <span>Total Cuota:</span>
                <span class="neon-text">3.85x</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
