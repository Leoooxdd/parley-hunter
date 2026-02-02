"""
PARLEY HUNTER ELITE - Sistema Premium de Apuestas Deportivas
Diseño: Minimalista Black & Neon Green
Autor: Experto Full-Stack Developer
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from typing import List, Dict, Tuple
import json

# ==================== CONFIGURACIÓN INICIAL ====================
st.set_page_config(
    page_title="Parley Hunter Elite",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== ESTILOS CSS PREMIUM ====================
def inject_custom_css():
    st.markdown("""
    <style>
    /* RESET Y BASE */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    /* FONDO NEGRO PURO */
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }
    
    /* ELIMINAR PADDING DE STREAMLIT */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 100% !important;
    }
    
    /* OCULTAR HEADER Y FOOTER */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* TABS PERSONALIZADOS */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #121212;
        padding: 10px;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #1a1a1a;
        border-radius: 8px;
        color: #ffffff;
        padding: 12px 24px;
        font-weight: 600;
        border: 1px solid #00ff00;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #00ff00 0%, #00cc00 100%);
        color: #000000;
        box-shadow: 0 0 20px rgba(0, 255, 0, 0.5);
    }
    
    /* TARJETAS DE PARLEY */
    .parley-card {
        background: linear-gradient(145deg, #1a1a1a 0%, #0d0d0d 100%);
        border: 2px solid #00ff00;
        border-radius: 16px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(0, 255, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .parley-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 255, 0, 0.4);
        border-color: #00ff00;
    }
    
    /* HEADER DE PARLEY */
    .parley-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 20px;
        padding-bottom: 15px;
        border-bottom: 1px solid #00ff00;
    }
    
    .parley-title {
        font-size: 24px;
        font-weight: 800;
        background: linear-gradient(90deg, #00ff00, #00cc00);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    
    .parley-odds {
        font-size: 32px;
        font-weight: 900;
        color: #00ff00;
        text-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
    }
    
    /* PICKS CON AVATAR */
    .pick-item {
        display: flex;
        align-items: center;
        background: #0d0d0d;
        padding: 15px;
        margin: 10px 0;
        border-radius: 12px;
        border-left: 4px solid #00ff00;
    }
    
    .player-avatar {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        margin-right: 15px;
        border: 3px solid #00ff00;
        object-fit: cover;
        box-shadow: 0 0 15px rgba(0, 255, 0, 0.3);
    }
    
    .pick-info {
        flex: 1;
    }
    
    .pick-player {
        font-size: 18px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 5px;
    }
    
    .pick-prediction {
        font-size: 14px;
        color: #00ff00;
        font-weight: 600;
    }
    
    .pick-odds {
        font-size: 16px;
        font-weight: 700;
        color: #00ff00;
        margin-left: 20px;
    }
    
    /* BOTONES */
    .stButton > button {
        background: linear-gradient(135deg, #00ff00 0%, #00cc00 100%);
        color: #000000;
        font-weight: 700;
        border: none;
        border-radius: 8px;
        padding: 12px 30px;
        font-size: 16px;
        cursor: pointer;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(0, 255, 0, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 255, 0, 0.5);
    }
    
    /* EXPANDERS */
    .streamlit-expanderHeader {
        background-color: #1a1a1a;
        border: 1px solid #00ff00;
        border-radius: 8px;
        color: #ffffff;
        font-weight: 700;
    }
    
    /* DATAFRAME */
    .dataframe {
        background-color: #0d0d0d !important;
        color: #ffffff !important;
        border: 1px solid #00ff00 !important;
    }
    
    /* MÉTRICAS */
    .metric-container {
        background: #1a1a1a;
        border: 2px solid #00ff00;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
    }
    
    .metric-value {
        font-size: 36px;
        font-weight: 900;
        color: #00ff00;
        text-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
    }
    
    .metric-label {
        font-size: 14px;
        color: #888888;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* COMUNIDAD */
    .post-card {
        background: #1a1a1a;
        border: 1px solid #333333;
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
    }
    
    .vote-button {
        display: inline-block;
        padding: 8px 20px;
        margin: 5px;
        border-radius: 20px;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s;
    }
    
    .vote-win {
        background: #00ff00;
        color: #000000;
    }
    
    .vote-lose {
        background: #ff0000;
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)

# ==================== BASE DE DATOS DE JUGADORES ====================
PLAYER_IMGS = {
    # NBA
    "LeBron James": "https://cdn.nba.com/headshots/nba/latest/1040x760/2544.png",
    "Stephen Curry": "https://cdn.nba.com/headshots/nba/latest/1040x760/201939.png",
    "Giannis Antetokounmpo": "https://cdn.nba.com/headshots/nba/latest/1040x760/203507.png",
    "Luka Dončić": "https://cdn.nba.com/headshots/nba/latest/1040x760/1629029.png",
    "Kevin Durant": "https://cdn.nba.com/headshots/nba/latest/1040x760/201142.png",
    "Nikola Jokić": "https://cdn.nba.com/headshots/nba/latest/1040x760/203999.png",
    "Joel Embiid": "https://cdn.nba.com/headshots/nba/latest/1040x760/203954.png",
    "Jayson Tatum": "https://cdn.nba.com/headshots/nba/latest/1040x760/1628369.png",
    "Anthony Davis": "https://cdn.nba.com/headshots/nba/latest/1040x760/203076.png",
    "Damian Lillard": "https://cdn.nba.com/headshots/nba/latest/1040x760/203081.png",
    
    # FÚTBOL
    "Lionel Messi": "https://a.espncdn.com/combiner/i?img=/i/headshots/soccer/players/full/45843.png",
    "Cristiano Ronaldo": "https://a.espncdn.com/combiner/i?img=/i/headshots/soccer/players/full/45686.png",
    "Kylian Mbappé": "https://a.espncdn.com/combiner/i?img=/i/headshots/soccer/players/full/231447.png",
    "Erling Haaland": "https://a.espncdn.com/combiner/i?img=/i/headshots/soccer/players/full/4328422.png",
    "Vinicius Jr": "https://a.espncdn.com/combiner/i?img=/i/headshots/soccer/players/full/4352055.png",
    "Mohamed Salah": "https://a.espncdn.com/combiner/i?img=/i/headshots/soccer/players/full/149350.png",
    "Jude Bellingham": "https://a.espncdn.com/combiner/i?img=/i/headshots/soccer/players/full/4629889.png",
    "Harry Kane": "https://a.espncdn.com/combiner/i?img=/i/headshots/soccer/players/full/144098.png",
    "Robert Lewandowski": "https://a.espncdn.com/combiner/i?img=/i/headshots/soccer/players/full/103955.png",
    "Neymar Jr": "https://a.espncdn.com/combiner/i?img=/i/headshots/soccer/players/full/110117.png",
    
    # NFL
    "Patrick Mahomes": "https://a.espncdn.com/combiner/i?img=/i/headshots/nfl/players/full/3139477.png",
    "Josh Allen": "https://a.espncdn.com/combiner/i?img=/i/headshots/nfl/players/full/3918298.png",
    "Lamar Jackson": "https://a.espncdn.com/combiner/i?img=/i/headshots/nfl/players/full/3916387.png",
    "Travis Kelce": "https://a.espncdn.com/combiner/i?img=/i/headshots/nfl/players/full/15847.png",
    "Tyreek Hill": "https://a.espncdn.com/combiner/i?img=/i/headshots/nfl/players/full/3116406.png",
}

# ==================== DATOS SIMULADOS DE EQUIPOS ====================
TEAM_POWER = {
    # Premier League
    "Manchester City": 95, "Liverpool": 92, "Arsenal": 90, "Chelsea": 85,
    "Manchester United": 83, "Tottenham": 82, "Newcastle": 80, "Brighton": 78,
    "Aston Villa": 77, "West Ham": 75, "Crystal Palace": 72, "Wolves": 70,
    
    # La Liga
    "Real Madrid": 94, "Barcelona": 91, "Atlético Madrid": 88, "Sevilla": 82,
    "Real Sociedad": 80, "Villarreal": 79, "Athletic Bilbao": 77, "Valencia": 75,
    
    # NBA
    "Boston Celtics": 93, "Denver Nuggets": 91, "Milwaukee Bucks": 90,
    "Phoenix Suns": 88, "LA Lakers": 87, "Golden State Warriors": 86,
    "Dallas Mavericks": 85, "Philadelphia 76ers": 84, "Miami Heat": 82,
    "LA Clippers": 81, "Memphis Grizzlies": 79, "Sacramento Kings": 78,
}

# ==================== FUNCIONES DE GENERACIÓN DE DATOS ====================

def get_nba_games_today():
    """Obtiene partidos de NBA de hoy (con datos reales o simulados)"""
    try:
        from nba_api.live.nba.endpoints import scoreboard
        games = scoreboard.ScoreBoard()
        games_data = games.get_dict()
        
        if games_data and 'scoreboard' in games_data and 'games' in games_data['scoreboard']:
            real_games = []
            for game in games_data['scoreboard']['games'][:5]:
                real_games.append({
                    'home': game['homeTeam']['teamName'],
                    'away': game['awayTeam']['teamName'],
                    'time': game.get('gameStatusText', 'TBD')
                })
            if real_games:
                return real_games
    except:
        pass
    
    # FALLBACK: Partidos simulados
    teams = ["Lakers", "Celtics", "Warriors", "Bucks", "Nets", "Heat", "Suns", "Mavericks"]
    games = []
    random.shuffle(teams)
    for i in range(0, len(teams)-1, 2):
        games.append({
            'home': teams[i],
            'away': teams[i+1],
            'time': f"{random.randint(18, 22)}:{random.choice(['00', '30'])} ET"
        })
    return games

def get_soccer_matches():
    """Genera partidos de fútbol basados en poder de equipos"""
    leagues = {
        "Premier League": ["Manchester City", "Liverpool", "Arsenal", "Chelsea", "Tottenham", "Manchester United"],
        "La Liga": ["Real Madrid", "Barcelona", "Atlético Madrid", "Sevilla", "Real Sociedad", "Villarreal"]
    }
    
    matches = []
    for league, teams in leagues.items():
        random.shuffle(teams)
        for i in range(0, min(4, len(teams)-1), 2):
            home = teams[i]
            away = teams[i+1]
            
            # Calcular cuotas basadas en poder
            power_diff = TEAM_POWER.get(home, 75) - TEAM_POWER.get(away, 75)
            base_odds_home = max(1.3, 2.5 - (power_diff / 30))
            base_odds_away = max(1.3, 2.5 + (power_diff / 30))
            
            matches.append({
                'league': league,
                'home': home,
                'away': away,
                'time': f"{random.randint(12, 20)}:{random.choice(['00', '15', '30', '45'])}",
                'odds_home': round(base_odds_home, 2),
                'odds_draw': round(random.uniform(3.0, 3.8), 2),
                'odds_away': round(base_odds_away, 2),
                'over_2_5': round(random.uniform(1.6, 2.1), 2),
                'under_2_5': round(random.uniform(1.7, 2.2), 2),
                'btts_yes': round(random.uniform(1.7, 2.3), 2),
                'btts_no': round(random.uniform(1.5, 2.0), 2)
            })
    
    return matches

def generate_player_props(sport: str, num_picks: int = 5):
    """Genera props de jugadores con imágenes"""
    props = []
    
    if sport == "NBA":
        stats = ["Puntos", "Rebotes", "Asistencias", "Robos", "Rebotes+Asistencias"]
        nba_players = [p for p in PLAYER_IMGS.keys() if p in [
            "LeBron James", "Stephen Curry", "Giannis Antetokounmpo", "Luka Dončić",
            "Kevin Durant", "Nikola Jokić", "Joel Embiid", "Jayson Tatum"
        ]]
        
        for _ in range(num_picks):
            player = random.choice(nba_players)
            stat = random.choice(stats)
            
            # Valores realistas
            if stat == "Puntos":
                line = round(random.uniform(22.5, 32.5), 1)
            elif stat == "Rebotes":
                line = round(random.uniform(8.5, 12.5), 1)
            elif stat == "Asistencias":
                line = round(random.uniform(6.5, 10.5), 1)
            elif stat == "Robos":
                line = round(random.uniform(1.5, 2.5), 1)
            else:
                line = round(random.uniform(14.5, 20.5), 1)
            
            props.append({
                'player': player,
                'image': PLAYER_IMGS.get(player, ""),
                'stat': stat,
                'line': line,
                'pick': random.choice(["Over", "Under"]),
                'odds': round(random.uniform(1.75, 2.1), 2)
            })
    
    elif sport == "Soccer":
        stats = ["Tiros al Arco", "Goles", "Asistencias", "Tarjetas"]
        soccer_players = [p for p in PLAYER_IMGS.keys() if p in [
            "Kylian Mbappé", "Erling Haaland", "Vinicius Jr", "Mohamed Salah",
            "Jude Bellingham", "Harry Kane", "Robert Lewandowski"
        ]]
        
        for _ in range(num_picks):
            player = random.choice(soccer_players)
            stat = random.choice(stats)
            
            if stat == "Tiros al Arco":
                line = round(random.uniform(2.5, 4.5), 1)
            elif stat == "Goles":
                line = round(random.uniform(0.5, 1.5), 1)
            else:
                line = round(random.uniform(0.5, 2.5), 1)
            
            props.append({
                'player': player,
                'image': PLAYER_IMGS.get(player, ""),
                'stat': stat,
                'line': line,
                'pick': random.choice(["Over", "Under"]),
                'odds': round(random.uniform(1.7, 2.2), 2)
            })
    
    return props

def calculate_parlay_odds(picks: List[Dict]) -> float:
    """Calcula cuota total del parley"""
    total_odds = 1.0
    for pick in picks:
        total_odds *= pick['odds']
    return round(total_odds, 2)

def generate_daily_parlays():
    """Genera los 3 parleys del día"""
    parlays = {
        'safe': {'name': '🛡️ PARLEY ASEGURADO', 'picks': [], 'type': 'safe'},
        'medium': {'name': '⚖️ PARLEY MEDIO', 'picks': [], 'type': 'medium'},
        'dream': {'name': '🦄 PARLEY SOÑADOR', 'picks': [], 'type': 'dream'}
    }
    
    # ASEGURADO (3-4 picks, cuotas bajas)
    safe_picks = generate_player_props("NBA", 2) + generate_player_props("Soccer", 2)
    for pick in safe_picks[:4]:
        pick['odds'] = round(random.uniform(1.4, 1.7), 2)
    parlays['safe']['picks'] = safe_picks[:4]
    
    # MEDIO (5-6 picks, cuotas medias)
    medium_picks = generate_player_props("NBA", 3) + generate_player_props("Soccer", 3)
    for pick in medium_picks[:6]:
        pick['odds'] = round(random.uniform(1.7, 2.0), 2)
    parlays['medium']['picks'] = medium_picks[:6]
    
    # SOÑADOR (8-10 picks, cuotas altas)
    dream_picks = generate_player_props("NBA", 5) + generate_player_props("Soccer", 5)
    for pick in dream_picks[:10]:
        pick['odds'] = round(random.uniform(1.9, 2.4), 2)
    parlays['dream']['picks'] = dream_picks[:10]
    
    return parlays

# ==================== COMPONENTES UI ====================

def render_parlay_card(parlay_data: Dict):
    """Renderiza una tarjeta de parley premium"""
    total_odds = calculate_parlay_odds(parlay_data['picks'])
    potential_win = round(100 * total_odds, 2)
    
    html = f"""
    <div class="parley-card">
        <div class="parley-header">
            <div class="parley-title">{parlay_data['name']}</div>
            <div class="parley-odds">@{total_odds}</div>
        </div>
        <div style="margin-bottom: 15px; color: #00ff00; font-size: 16px; font-weight: 600;">
            💰 Apuesta $100 → Ganas ${potential_win}
        </div>
    """
    
    for pick in parlay_data['picks']:
        html += f"""
        <div class="pick-item">
            <img src="{pick['image']}" class="player-avatar" onerror="this.src='https://via.placeholder.com/50/00ff00/000000?text={pick['player'][0]}'">
            <div class="pick-info">
                <div class="pick-player">{pick['player']}</div>
                <div class="pick-prediction">{pick['pick']} {pick['line']} {pick['stat']}</div>
            </div>
            <div class="pick-odds">@{pick['odds']}</div>
        </div>
        """
    
    html += """
    </div>
    """
    
    st.markdown(html, unsafe_allow_html=True)

def render_top_scorers():
    """Tabla de goleadores con datos de respaldo"""
    scorers_data = [
        {"Jugador": "Erling Haaland", "Equipo": "Man City", "Goles": 28, "Asistencias": 5},
        {"Jugador": "Harry Kane", "Equipo": "Bayern", "Goles": 26, "Asistencias": 8},
        {"Jugador": "Kylian Mbappé", "Equipo": "Real Madrid", "Goles": 25, "Asistencias": 7},
        {"Jugador": "Robert Lewandowski", "Equipo": "Barcelona", "Goles": 23, "Asistencias": 4},
        {"Jugador": "Victor Osimhen", "Equipo": "Napoli", "Goles": 22, "Asistencias": 3},
        {"Jugador": "Mohamed Salah", "Equipo": "Liverpool", "Goles": 21, "Asistencias": 12},
        {"Jugador": "Lautaro Martínez", "Equipo": "Inter", "Goles": 20, "Asistencias": 6},
        {"Jugador": "Vinicius Jr", "Equipo": "Real Madrid", "Goles": 19, "Asistencias": 10},
        {"Jugador": "Jude Bellingham", "Equipo": "Real Madrid", "Goles": 18, "Asistencias": 9},
        {"Jugador": "Cole Palmer", "Equipo": "Chelsea", "Goles": 17, "Asistencias": 11},
    ]
    
    df = pd.DataFrame(scorers_data)
    
    st.markdown("### ⚽ TOP 10 GOLEADORES - EUROPA 2024/25")
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Jugador": st.column_config.TextColumn("Jugador", width="medium"),
            "Equipo": st.column_config.TextColumn("Equipo", width="small"),
            "Goles": st.column_config.NumberColumn("⚽ Goles", width="small"),
            "Asistencias": st.column_config.NumberColumn("🎯 Asistencias", width="small"),
        }
    )

# ==================== APLICACIÓN PRINCIPAL ====================

def main():
    inject_custom_css()
    
    # HEADER
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%); border-bottom: 2px solid #00ff00; margin-bottom: 30px;'>
        <h1 style='font-size: 48px; font-weight: 900; background: linear-gradient(90deg, #00ff00, #00cc00); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0;'>
            💎 PARLEY HUNTER ELITE
        </h1>
        <p style='color: #888888; margin-top: 10px; font-size: 16px; letter-spacing: 2px;'>
            SISTEMA PREMIUM DE APUESTAS DEPORTIVAS
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # TABS PRINCIPALES
    tab1, tab2, tab3, tab4 = st.tabs([
        "🏠 INICIO",
        "⚡ GENERADORES",
        "⚽ GOLEADORES",
        "👥 COMUNIDAD"
    ])
    
    # ==================== TAB 1: INICIO ====================
    with tab1:
        st.markdown("### 🎯 LOS 3 PARLEYS DEL DÍA")
        st.markdown(f"**Fecha:** {datetime.now().strftime('%d/%m/%Y')} | **Actualizados cada 24h**")
        
        daily_parlays = generate_daily_parlays()
        
        cols = st.columns(3)
        with cols[0]:
            render_parlay_card(daily_parlays['safe'])
        with cols[1]:
            render_parlay_card(daily_parlays['medium'])
        with cols[2]:
            render_parlay_card(daily_parlays['dream'])
        
        st.markdown("---")
        st.markdown("### 📊 PARTIDOS DE HOY")
        
        col_nba, col_soccer = st.columns(2)
        
        with col_nba:
            st.markdown("#### 🏀 NBA")
            nba_games = get_nba_games_today()
            for game in nba_games:
                st.markdown(f"""
                <div style='background: #1a1a1a; padding: 15px; margin: 10px 0; border-radius: 10px; border-left: 4px solid #00ff00;'>
                    <div style='font-weight: 700; font-size: 16px;'>{game['home']} vs {game['away']}</div>
                    <div style='color: #00ff00; font-size: 14px; margin-top: 5px;'>🕐 {game['time']}</div>
                </div>
                """, unsafe_allow_html=True)
        
        with col_soccer:
            st.markdown("#### ⚽ FÚTBOL")
            soccer_matches = get_soccer_matches()
            for match in soccer_matches[:5]:
                st.markdown(f"""
                <div style='background: #1a1a1a; padding: 15px; margin: 10px 0; border-radius: 10px; border-left: 4px solid #00ff00;'>
                    <div style='color: #888888; font-size: 12px; margin-bottom: 5px;'>{match['league']}</div>
                    <div style='font-weight: 700; font-size: 16px;'>{match['home']} vs {match['away']}</div>
                    <div style='color: #00ff00; font-size: 14px; margin-top: 5px;'>🕐 {match['time']}</div>
                </div>
                """, unsafe_allow_html=True)
    
    # ==================== TAB 2: GENERADORES ====================
    with tab2:
        st.markdown("### ⚡ GENERADORES DE PARLEYS PERSONALIZADOS")
        
        gen_type = st.selectbox(
            "Selecciona el tipo de Parley:",
            ["🏀 NBA Players", "⚽ Fútbol Players", "🏈 NFL Props", "🎲 COMBO MIX"],
            key="gen_type"
        )
        
        col1, col2 = st.columns([1, 3])
        
        with col1:
            risk_level = st.radio(
                "Nivel de Riesgo:",
                ["🛡️ Asegurada", "⚖️ Media", "🔥 Difícil", "🦄 Soñadora"],
                key="risk"
            )
            
            num_picks = st.slider("Número de Picks:", 3, 16, 6, key="num_picks")
            
            if st.button("🎲 GENERAR PARLEY", use_container_width=True):
                st.session_state.custom_parlay = True
        
        with col2:
            if st.session_state.get('custom_parlay', False):
                if "NBA" in gen_type:
                    picks = generate_player_props("NBA", num_picks)
                elif "Fútbol" in gen_type:
                    picks = generate_player_props("Soccer", num_picks)
                else:
                    picks = generate_player_props("NBA", num_picks//2) + generate_player_props("Soccer", num_picks//2)
                
                # Ajustar cuotas según riesgo
                risk_multipliers = {
                    "🛡️ Asegurada": (1.4, 1.7),
                    "⚖️ Media": (1.7, 2.0),
                    "🔥 Difícil": (1.9, 2.3),
                    "🦄 Soñadora": (2.1, 2.6)
                }
                
                min_odd, max_odd = risk_multipliers[risk_level]
                for pick in picks:
                    pick['odds'] = round(random.uniform(min_odd, max_odd), 2)
                
                custom_parlay = {
                    'name': f'{risk_level} - {gen_type}',
                    'picks': picks,
                    'type': 'custom'
                }
                
                render_parlay_card(custom_parlay)
    
    # ==================== TAB 3: GOLEADORES ====================
    with tab3:
        render_top_scorers()
        
        st.markdown("---")
        st.markdown("### 📈 ESTADÍSTICAS DESTACADAS")
        
        cols = st.columns(4)
        with cols[0]:
            st.metric("🥇 Líder", "Haaland", "28 goles")
        with cols[1]:
            st.metric("🎯 Más Asistencias", "Salah", "12 asistencias")
        with cols[2]:
            st.metric("🔥 Racha", "Mbappé", "5 partidos")
        with cols[3]:
            st.metric("⚡ Promedio", "Kane", "0.89 goles/90'")
    
    # ==================== TAB 4: COMUNIDAD ====================
    with tab4:
        st.markdown("### 👥 MURO DE LA COMUNIDAD")
        
        if 'posts' not in st.session_state:
            st.session_state.posts = [
                {
                    'user': 'ParlayKing23',
                    'parlay': '5-leg NBA parlay @12.5',
                    'result': None,
                    'votes_win': 0,
                    'votes_lose': 0
                },
                {
                    'user': 'SoccerPro',
                    'parlay': 'Haaland + Mbappé Over 0.5 goles @4.2',
                    'result': None,
                    'votes_win': 0,
                    'votes_lose': 0
                },
                {
                    'user': 'DreamChaser',
                    'parlay': '10-leg MIX parlay @245.0',
                    'result': None,
                    'votes_win': 0,
                    'votes_lose': 0
                }
            ]
        
        # Publicar nuevo parley
        with st.expander("➕ PUBLICAR MI PARLEY"):
            user_name = st.text_input("Tu nombre:", placeholder="ParlayHunter")
            parlay_desc = st.text_area("Describe tu parley:", placeholder="LeBron Over 25.5 pts + Curry Over 4.5 3PT...")
            
            if st.button("📤 PUBLICAR"):
                if user_name and parlay_desc:
                    st.session_state.posts.insert(0, {
                        'user': user_name,
                        'parlay': parlay_desc,
                        'result': None,
                        'votes_win': 0,
                        'votes_lose': 0
                    })
                    st.success("✅ ¡Parley publicado!")
                    st.rerun()
        
        # Mostrar posts
        for idx, post in enumerate(st.session_state.posts):
            st.markdown(f"""
            <div class='post-card'>
                <div style='font-weight: 700; color: #00ff00; margin-bottom: 10px;'>@{post['user']}</div>
                <div style='font-size: 16px; margin-bottom: 15px;'>{post['parlay']}</div>
                <div style='display: flex; gap: 10px; align-items: center;'>
                    <span style='color: #888888;'>¿Cómo quedó?</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 1, 4])
            with col1:
                if st.button(f"🤑 Pagó ({post['votes_win']})", key=f"win_{idx}"):
                    st.session_state.posts[idx]['votes_win'] += 1
                    st.rerun()
            with col2:
                if st.button(f"🤡 Nadota ({post['votes_lose']})", key=f"lose_{idx}"):
                    st.session_state.posts[idx]['votes_lose'] += 1
                    st.rerun()
    
    # FOOTER
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #555555; padding: 20px; font-size: 12px;'>
        <p>💎 Parley Hunter Elite v2.0 | Desarrollado con Streamlit & Python</p>
        <p style='color: #00ff00;'>⚠️ Apuesta responsablemente. Este sistema es solo para entretenimiento.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
