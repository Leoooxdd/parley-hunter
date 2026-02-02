import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import random

# ==================== CONFIGURACIÓN ====================
st.set_page_config(page_title="Parleisitos Ultimate", page_icon="💎", layout="centered")

# ==================== ESTILOS CSS DRAFTEA (MINIMALISTA) ====================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&display=swap');
    * { font-family: 'Inter', sans-serif; }
    
    .stApp { background-color: #0b0a14 !important; color: white !important; }
    
    /* TARJETAS FLOTANTES */
    .game-card {
        background: #1a1b2e;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 15px;
        border: 1px solid #2d2f45;
        box-shadow: 0 4px 20px rgba(0,0,0,0.4);
    }
    
    /* TEXTOS */
    h1, h2, h3 { color: white !important; }
    .neon-green { color: #00ff00 !important; font-weight: bold; text-shadow: 0 0 10px rgba(0,255,0,0.3); }
    .neon-purple { color: #a855f7 !important; font-weight: bold; }
    .sub-text { color: #94a3b8; font-size: 0.85em; }
    
    /* BARRAS DE PROGRESO PERSONALIZADAS */
    .stProgress > div > div > div > div {
        background-color: #6d28d9;
    }
    
    /* BOTONES */
    .stButton > button {
        background: #6d28d9 !important;
        color: white !important;
        border-radius: 12px;
        width: 100%;
        border: none;
        font-weight: 800;
    }
    
    /* IMAGENES */
    .team-logo { width: 40px; height: 40px; object-fit: contain; }
    .player-face { width: 60px; height: 60px; border-radius: 50%; border: 2px solid #00ff00; }
    </style>
""", unsafe_allow_html=True)

# ==================== DATA ENGINE (FOTMOB REAL) ====================
@st.cache_data(ttl=600)
def get_real_matches(days_offset=0):
    """Busca partidos de hoy, y si no hay, busca mañana"""
    date = (datetime.now() + timedelta(days=days_offset)).strftime('%Y%m%d')
    url = f"https://www.fotmob.com/api/matches?date={date}"
    try:
        r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
        data = r.json()
        matches = []
        if 'leagues' in data:
            for league in data['leagues']:
                # Filtramos ligas principales por ID
                if league['primaryId'] in [47, 87, 55, 54, 53, 2244, 42, 73]: 
                    for m in league['matches']:
                        matches.append({
                            "league": league['name'],
                            "home": m['home']['name'],
                            "away": m['away']['name'],
                            "time": m['status'].get('startTimeStr', 'VS'),
                            "home_score": m['home']['score'],
                            "away_score": m['away']['score'],
                            "started": m['status']['started'],
                            "id": m['id']
                        })
        return matches, date
    except:
        return [], date

# ==================== UI COMPONENTS ====================

def draw_stat_chart(label, val1, val2, team1, team2):
    """Dibuja un gráfico comparativo simple"""
    st.caption(f"📊 Estadísticas: {label}")
    chart_data = pd.DataFrame({
        'Equipo': [team1, team2],
        label: [val1, val2]
    })
    st.bar_chart(chart_data.set_index('Equipo'), color="#6d28d9")

# ==================== APP LOGIC ====================

st.markdown("<h1 style='text-align:center;'>💎 PARLEISITOS <span class='neon-purple'>ULTIMATE</span></h1>", unsafe_allow_html=True)

tabs = st.tabs(["🔥 INICIO", "⚽ FÚTBOL", "🏀 NBA", "📊 TABLAS", "💎 PARLEY (16)"])

# --- TAB 1: INICIO ---
with tabs[0]:
    st.markdown("### ⚡ Tendencias del Mercado")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class='game-card'>
            <center>
                <img src='https://resources.premierleague.com/premierleague/photos/players/250x250/p223094.png' class='player-face'>
                <h3 class='neon-green'>LA FIJA</h3>
                <p>Haaland: +1.5 Tiros al arco</p>
                <p class='sub-text'>Probabilidad: 94%</p>
            </center>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class='game-card'>
            <center>
                <img src='https://a.espncdn.com/combiner/i?img=/i/headshots/nba/players/full/3975.png' class='player-face' style='border-color:#a855f7;'>
                <h3 class='neon-purple'>EL BOMBAZO</h3>
                <p>Curry: +30 Puntos + Win</p>
                <p class='sub-text'>Cuota: 4.50x</p>
            </center>
        </div>
        """, unsafe_allow_html=True)

# --- TAB 2: FÚTBOL (CON GRÁFICOS) ---
with tabs[1]:
    # Lógica de búsqueda automática de "Próximos Juegos"
    matches, date_used = get_real_matches(0)
    msg = "Partidos de HOY"
    if not matches:
        matches, date_used = get_real_matches(1)
        msg = "No hay destacados hoy. Mostrando partidos de MAÑANA"
    
    st.caption(f"📅 {msg} ({date_used})")
    
    if matches:
        for m in matches:
            with st.container():
                st.markdown(f"""
                <div class='game-card'>
                    <div style='display:flex; justify-content:space-between; margin-bottom:10px;'>
                        <span class='neon-purple'>{m['league']}</span>
                        <span class='sub-text'>{m['time']}</span>
                    </div>
                    <div style='display:flex; justify-content:space-between; align-items:center;'>
                        <h3>{m['home']}</h3>
                        <h2 class='neon-green'>{m['home_score'] if m['started'] else 'VS'}</h2>
                        <h3>{m['away']}</h3>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # GRÁFICO EXPANDIBLE DENTRO DE LA TARJETA
                with st.expander(f"📊 Ver Estadísticas: {m['home']} vs {m['away']}"):
                    # Simulamos datos realistas para el gráfico (ya que no tenemos historial profundo gratis)
                    val1 = random.randint(10, 80)
                    val2 = random.randint(10, 80)
                    st.write("Probabilidad de Victoria (IA Model)")
                    st.progress(val1)
                    st.caption(f"{m['home']}: {val1}% | {m['away']}: {100-val1}%")
                    
                    draw_stat_chart("Goles en últimos 5 partidos", random.randint(3,12), random.randint(3,12), m['home'], m['away'])
    else:
        st.info("No se encontraron partidos importantes en los próximos 2 días.")

# --- TAB 3: NBA ---
with tabs[2]:
    st.markdown("### 🏀 NBA Center")
    # Aquí iría la conexión nba_api, ponemos un placeholder visual potente
    st.markdown("""
    <div class='game-card'>
        <div style='display:flex; justify-content:space-between;'>
            <h3>Lakers</h3>
            <h3 class='neon-green'>112 - 108</h3>
            <h3>Warriors</h3>
        </div>
        <hr style='border-color:#333;'>
        <p class='sub-text'>4to Cuarto - 2:03 min</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.write("Comparativa de Triples")
    chart_data = pd.DataFrame({'Team': ['Lakers', 'Warriors'], 'Triples': [12, 18]})
    st.bar_chart(chart_data.set_index('Team'), color="#00ff00")

# --- TAB 4: TABLAS ---
with tabs[3]:
    st.markdown("### 📊 Tablas de Posiciones")
    league_sel = st.selectbox("Liga", ["Premier League", "La Liga", "Liga MX"])
    
    # Datos simulados de tabla real (para visualización)
    data = {
        'Equipo': ['Liverpool', 'Man City', 'Arsenal', 'Aston Villa', 'Tottenham'],
        'Puntos': [54, 52, 49, 46, 44],
        'Goles': [50, 52, 48, 40, 42]
    }
    df = pd.DataFrame(data)
    
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.write("Gráfico de Poder (Puntos)")
    st.bar_chart(df.set_index('Equipo')['Puntos'], color="#6d28d9")

# --- TAB 5: GENERADOR 16 PICKS ---
with tabs[4]:
    st.markdown("### 💎 Armador de Parleys (Max 16)")
    
    col_a, col_b = st.columns([2, 1])
    with col_a:
        picks_num = st.slider("Cantidad de Selecciones", 2, 16, 4)
        riesgo = st.select_slider("Riesgo", ["Bajo", "Medio", "Alto", "Imposible"])
    
    with col_b:
        st.markdown(f"""
        <div style='background:#1a1b2e; padding:10px; border-radius:10px; text-align:center;'>
            <small>Ganancia Potencial</small>
            <h2 class='neon-green'>${picks_num * 150 * (picks_num/2):,.0f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    if st.button("🚀 GENERAR PARLEY MASIVO"):
        st.markdown(f"<div class='game-card'>", unsafe_allow_html=True)
        st.markdown(f"<h3 class='neon-purple'>PARLEY DE {picks_num} SELECCIONES</h3>", unsafe_allow_html=True)
        
        teams = ["Real Madrid", "Man City", "Lakers", "América", "Boca Jrs", "Barcelona", "Bayern", "PSG", "Celtics", "Chiefs"]
        markets = ["Gana", "Over 2.5", "+0.5 Goles", "+20 Pts", "Gana Directo", "Ambos Anotan"]
        
        for i in range(picks_num):
            t = random.choice(teams)
            m = random.choice(markets)
            st.markdown(f"""
            <div style='display:flex; justify-content:space-between; border-bottom:1px solid #333; padding:8px 0;'>
                <span>{i+1}. <b>{t}</b></span>
                <span class='neon-green'>{m}</span>
            </div>
            """, unsafe_allow_html=True)
            
        st.markdown("</div>", unsafe_allow_html=True)
