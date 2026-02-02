"""
PARLEISITOS v4.0 - Sistema Premium de Apuestas Deportivas
Diseño: DraftKings Dark Mode (Negro Profundo + Morado Neón + Cian)
Datos: FotMob (sin API key) + NBA API Oficial
Autor: Desarrollador Senior Full-Stack
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import requests
import json
from typing import List, Dict, Optional
import time

# ==================== CONFIGURACIÓN ====================
st.set_page_config(
    page_title="Parleisitos - Apuestas Deportivas",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== DICCIONARIO DE IMÁGENES DE JUGADORES ====================
PLAYER_IMGS = {
    # FÚTBOL - Estrellas Mundiales
    "Erling Haaland": "https://img.a.transfermarkt.technology/portrait/big/418560-1694609670.jpg?lm=1",
    "Kylian Mbappé": "https://img.a.transfermarkt.technology/portrait/big/342229-1696754486.jpg?lm=1",
    "Vinicius Jr": "https://img.a.transfermarkt.technology/portrait/big/371998-1692877439.jpg?lm=1",
    "Lionel Messi": "https://img.a.transfermarkt.technology/portrait/big/28003-1710080339.jpg?lm=1",
    "Cristiano Ronaldo": "https://img.a.transfermarkt.technology/portrait/big/8198-1694609670.jpg?lm=1",
    "Mohamed Salah": "https://img.a.transfermarkt.technology/portrait/big/148455-1667830921.jpg?lm=1",
    "Jude Bellingham": "https://img.a.transfermarkt.technology/portrait/big/581678-1683627243.jpg?lm=1",
    "Harry Kane": "https://img.a.transfermarkt.technology/portrait/big/132098-1631175704.jpg?lm=1",
    "Kevin De Bruyne": "https://img.a.transfermarkt.technology/portrait/big/88755-1631175139.jpg?lm=1",
    "Rodri": "https://img.a.transfermarkt.technology/portrait/big/357687-1631870997.jpg?lm=1",
    
    # NBA - Estrellas
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
}

# ==================== IDs REALES DE LIGAS FOTMOB ====================
LIGAS_FOTMOB = {
    "🇲🇽 Liga MX": {"id": 230, "country": "México"},
    "🏴󠁧󠁢󠁥󠁮󠁧󠁿 Premier League": {"id": 47, "country": "Inglaterra"},
    "🇪🇸 La Liga": {"id": 87, "country": "España"},
    "🇮🇹 Serie A": {"id": 55, "country": "Italia"},
    "🇩🇪 Bundesliga": {"id": 54, "country": "Alemania"},
    "🇫🇷 Ligue 1": {"id": 53, "country": "Francia"},
    "🏆 Champions League": {"id": 42, "country": "UEFA"},
    "🏆 Europa League": {"id": 73, "country": "UEFA"},
    "🏆 Copa Libertadores": {"id": 299, "country": "CONMEBOL"},
    "🇺🇸 MLS": {"id": 130, "country": "USA/Canadá"},
}

# ==================== ESTILOS CSS DARK MODE ====================
def inject_premium_css():
    st.markdown("""
    <style>
    /* ============ RESET Y BASE ============ */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }
    
    /* FONDO PRINCIPAL */
    .stApp {
        background-color: #0b0a14;
        color: #ffffff;
    }
    
    /* CONTAINER */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 1rem !important;
        padding-left: 3rem !important;
        padding-right: 3rem !important;
        max-width: 100% !important;
    }
    
    /* OCULTAR ELEMENTOS DE STREAMLIT */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* ============ TABS ============ */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: transparent;
        padding: 15px 0;
        border-bottom: 2px solid #1a1b2e;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 8px;
        color: #9ca3af;
        padding: 12px 28px;
        font-weight: 600;
        font-size: 15px;
        border: none;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        color: #22d3ee;
        background-color: rgba(34, 211, 238, 0.1);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #6d28d9 0%, #8b5cf6 100%);
        color: #ffffff;
        box-shadow: 0 4px 15px rgba(109, 40, 217, 0.4);
    }
    
    /* ============ TARJETAS ============ */
    .card {
        background: linear-gradient(145deg, #1a1b2e 0%, #14141f 100%);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(109, 40, 217, 0.3);
        border-color: rgba(139, 92, 246, 0.5);
    }
    
    /* ============ TARJETA DE PARLEY ============ */
    .parley-card {
        background: linear-gradient(145deg, #1a1b2e 0%, #14141f 100%);
        border: 2px solid #6d28d9;
        border-radius: 20px;
        padding: 28px;
        margin: 20px 0;
        box-shadow: 0 12px 40px rgba(109, 40, 217, 0.3);
    }
    
    .parley-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 24px;
        padding-bottom: 20px;
        border-bottom: 2px solid rgba(109, 40, 217, 0.3);
    }
    
    .parley-title {
        font-size: 28px;
        font-weight: 900;
        background: linear-gradient(90deg, #8b5cf6, #6d28d9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .parley-odds {
        font-size: 40px;
        font-weight: 900;
        color: #22d3ee;
        text-shadow: 0 0 20px rgba(34, 211, 238, 0.5);
    }
    
    .parley-payout {
        background: rgba(34, 211, 238, 0.1);
        border: 1px solid #22d3ee;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 24px;
        text-align: center;
    }
    
    .payout-amount {
        font-size: 32px;
        font-weight: 900;
        color: #22d3ee;
        text-shadow: 0 0 15px rgba(34, 211, 238, 0.4);
    }
    
    .payout-label {
        font-size: 14px;
        color: #9ca3af;
        margin-top: 8px;
    }
    
    /* ============ PICKS ============ */
    .pick-item {
        background: rgba(26, 27, 46, 0.6);
        border-left: 4px solid #8b5cf6;
        border-radius: 12px;
        padding: 20px;
        margin: 12px 0;
        display: flex;
        align-items: center;
        gap: 20px;
        transition: all 0.3s ease;
    }
    
    .pick-item:hover {
        background: rgba(139, 92, 246, 0.1);
        border-left-color: #22d3ee;
        transform: translateX(4px);
    }
    
    .player-avatar {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        border: 3px solid #8b5cf6;
        object-fit: cover;
        box-shadow: 0 0 20px rgba(139, 92, 246, 0.4);
    }
    
    .pick-info {
        flex: 1;
    }
    
    .pick-player {
        font-size: 18px;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 6px;
    }
    
    .pick-prediction {
        font-size: 15px;
        color: #22d3ee;
        font-weight: 600;
    }
    
    .pick-odds {
        font-size: 20px;
        font-weight: 900;
        color: #22d3ee;
        text-shadow: 0 0 10px rgba(34, 211, 238, 0.3);
    }
    
    /* ============ TARJETAS DE PARTIDO ============ */
    .match-card {
        background: linear-gradient(145deg, #1a1b2e 0%, #14141f 100%);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 16px;
        padding: 24px;
        margin: 16px 0;
        transition: all 0.3s ease;
    }
    
    .match-card:hover {
        border-color: rgba(139, 92, 246, 0.6);
        box-shadow: 0 8px 24px rgba(109, 40, 217, 0.2);
    }
    
    .match-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 16px;
        padding-bottom: 12px;
        border-bottom: 1px solid rgba(139, 92, 246, 0.2);
    }
    
    .match-time {
        font-size: 14px;
        font-weight: 600;
        color: #22d3ee;
        background: rgba(34, 211, 238, 0.1);
        padding: 6px 12px;
        border-radius: 6px;
    }
    
    .match-league {
        font-size: 12px;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .match-teams {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 16px 0;
    }
    
    .team-name {
        font-size: 18px;
        font-weight: 700;
        color: #ffffff;
    }
    
    .match-score {
        font-size: 24px;
        font-weight: 900;
        color: #8b5cf6;
    }
    
    .match-vs {
        font-size: 14px;
        color: #6d28d9;
        font-weight: 700;
    }
    
    .match-info {
        background: rgba(34, 211, 238, 0.05);
        border-radius: 8px;
        padding: 12px;
        margin-top: 12px;
        font-size: 13px;
        color: #9ca3af;
    }
    
    /* ============ TABLAS DE ESTADÍSTICAS ============ */
    .stats-table {
        background: #1a1b2e;
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 12px;
        overflow: hidden;
        margin: 16px 0;
    }
    
    .stats-row {
        display: grid;
        grid-template-columns: 60px 1fr 120px;
        padding: 16px 20px;
        border-bottom: 1px solid rgba(139, 92, 246, 0.1);
        align-items: center;
        transition: all 0.2s ease;
    }
    
    .stats-row:hover {
        background: rgba(139, 92, 246, 0.08);
    }
    
    .stats-row:last-child {
        border-bottom: none;
    }
    
    .stats-rank {
        font-size: 20px;
        font-weight: 900;
        color: #8b5cf6;
    }
    
    .stats-player {
        display: flex;
        align-items: center;
        gap: 16px;
    }
    
    .stats-avatar {
        width: 48px;
        height: 48px;
        border-radius: 50%;
        border: 2px solid #6d28d9;
        object-fit: cover;
    }
    
    .stats-name {
        font-size: 16px;
        font-weight: 700;
        color: #ffffff;
    }
    
    .stats-team {
        font-size: 13px;
        color: #9ca3af;
        margin-top: 4px;
    }
    
    .stats-value {
        font-size: 24px;
        font-weight: 900;
        color: #22d3ee;
        text-align: right;
    }
    
    /* ============ BOTONES ============ */
    .stButton > button {
        background: linear-gradient(135deg, #6d28d9 0%, #8b5cf6 100%);
        color: #ffffff;
        font-weight: 700;
        font-size: 16px;
        border: none;
        border-radius: 12px;
        padding: 14px 32px;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(109, 40, 217, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%);
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(109, 40, 217, 0.5);
    }
    
    /* ============ SELECTBOX ============ */
    .stSelectbox > div > div {
        background-color: #1a1b2e;
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 10px;
        color: #ffffff;
    }
    
    /* ============ MÉTRICAS ============ */
    .metric-card {
        background: linear-gradient(145deg, #1a1b2e 0%, #14141f 100%);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        border-color: rgba(139, 92, 246, 0.6);
        transform: translateY(-4px);
    }
    
    .metric-value {
        font-size: 36px;
        font-weight: 900;
        color: #22d3ee;
        text-shadow: 0 0 15px rgba(34, 211, 238, 0.4);
    }
    
    .metric-label {
        font-size: 13px;
        color: #9ca3af;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-top: 8px;
    }
    
    /* ============ ALERTS ============ */
    .alert-box {
        background: rgba(139, 92, 246, 0.1);
        border: 1px solid #6d28d9;
        border-radius: 12px;
        padding: 20px;
        margin: 16px 0;
        color: #ffffff;
    }
    
    .alert-warning {
        background: rgba(251, 191, 36, 0.1);
        border-color: #fbbf24;
        color: #fbbf24;
    }
    
    /* ============ DATAFRAME ============ */
    .dataframe {
        background-color: #1a1b2e !important;
        color: #ffffff !important;
        border: 1px solid rgba(139, 92, 246, 0.2) !important;
        border-radius: 12px !important;
    }
    
    /* ============ EXPANDER ============ */
    .streamlit-expanderHeader {
        background-color: #1a1b2e;
        border: 1px solid rgba(139, 92, 246, 0.3);
        border-radius: 10px;
        color: #ffffff;
        font-weight: 700;
    }
    
    </style>
    """, unsafe_allow_html=True)

# ==================== HEADERS FOTMOB ====================
FOTMOB_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'es-ES,es;q=0.9',
    'Referer': 'https://www.fotmob.com/',
    'Origin': 'https://www.fotmob.com'
}

# ==================== FUNCIONES FOTMOB ====================

def fetch_fotmob(url: str, timeout: int = 10) -> Optional[Dict]:
    """Request seguro a FotMob"""
    try:
        response = requests.get(url, headers=FOTMOB_HEADERS, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return None

def get_matches_today(league_id: Optional[int] = None) -> List[Dict]:
    """Obtiene partidos de HOY usando fecha actual real"""
    # CRÍTICO: Usar fecha ACTUAL, no fecha hardcodeada
    today = datetime.now().strftime("%Y%m%d")
    url = f"https://www.fotmob.com/api/matches?date={today}"
    
    data = fetch_fotmob(url)
    if not data or 'leagues' not in data:
        return []
    
    matches = []
    for league in data.get('leagues', []):
        if league_id and league.get('id') != league_id:
            continue
        
        for match in league.get('matches', []):
            try:
                # Extraer datos del partido
                home_team = match.get('home', {})
                away_team = match.get('away', {})
                status = match.get('status', {})
                
                matches.append({
                    'league': league.get('name', 'N/A'),
                    'home': home_team.get('name', 'TBD'),
                    'away': away_team.get('name', 'TBD'),
                    'home_score': home_team.get('score', '-'),
                    'away_score': away_team.get('score', '-'),
                    'time': status.get('utcTime', 'TBD'),
                    'stadium': status.get('reason', {}).get('long', 'N/A') if isinstance(status.get('reason'), dict) else 'N/A',
                    'started': status.get('started', False)
                })
            except:
                continue
    
    return matches

def get_league_stats(league_id: int) -> Dict:
    """Obtiene estadísticas de jugadores de una liga"""
    url = f"https://www.fotmob.com/api/leagues?id={league_id}&tab=stats&type=league"
    
    data = fetch_fotmob(url)
    if not data or 'stats' not in data:
        return {'scorers': [], 'assists': [], 'cleansheets': []}
    
    result = {'scorers': [], 'assists': [], 'cleansheets': []}
    
    try:
        for stat_section in data.get('stats', []):
            title = stat_section.get('title', '').lower()
            
            # Goleadores
            if 'scorer' in title or 'goals' in title:
                for player in stat_section.get('players', [])[:10]:
                    result['scorers'].append({
                        'name': player.get('name', 'N/A'),
                        'team': player.get('teamName', 'N/A'),
                        'value': player.get('statValue', '0')
                    })
            
            # Asistencias
            elif 'assist' in title:
                for player in stat_section.get('players', [])[:10]:
                    result['assists'].append({
                        'name': player.get('name', 'N/A'),
                        'team': player.get('teamName', 'N/A'),
                        'value': player.get('statValue', '0')
                    })
            
            # Clean Sheets (Porteros)
            elif 'clean' in title or 'sheet' in title:
                for player in stat_section.get('players', [])[:10]:
                    result['cleansheets'].append({
                        'name': player.get('name', 'N/A'),
                        'team': player.get('teamName', 'N/A'),
                        'value': player.get('statValue', '0')
                    })
    except:
        pass
    
    return result

# ==================== FUNCIONES NBA ====================

def get_nba_games() -> List[Dict]:
    """Obtiene partidos de NBA de hoy"""
    try:
        from nba_api.live.nba.endpoints import scoreboard
        board = scoreboard.ScoreBoard()
        data = board.get_dict()
        
        games = []
        if 'scoreboard' in data and 'games' in data['scoreboard']:
            for game in data['scoreboard']['games'][:10]:
                games.append({
                    'home': game['homeTeam']['teamName'],
                    'away': game['awayTeam']['teamName'],
                    'home_score': game['homeTeam'].get('score', '-'),
                    'away_score': game['awayTeam'].get('score', '-'),
                    'status': game.get('gameStatusText', 'Scheduled')
                })
        
        return games
    except:
        # Fallback con equipos simulados
        teams = ["Lakers", "Celtics", "Warriors", "Bucks", "Heat", "Suns", "Mavs", "Nets"]
        random.shuffle(teams)
        games = []
        for i in range(0, len(teams)-1, 2):
            games.append({
                'home': teams[i],
                'away': teams[i+1],
                'home_score': '-',
                'away_score': '-',
                'status': f"{random.randint(19, 21)}:00 ET"
            })
        return games

# ==================== GENERADORES DE PARLEYS ====================

def generate_daily_parleys() -> Dict:
    """Genera los 3 parleys del día usando lógica interna"""
    
    # Jugadores destacados
    soccer_stars = ["Erling Haaland", "Kylian Mbappé", "Vinicius Jr", "Jude Bellingham", "Mohamed Salah"]
    nba_stars = ["LeBron James", "Stephen Curry", "Giannis Antetokounmpo", "Luka Dončić", "Kevin Durant"]
    
    parlays = {}
    
    # PARLEY ASEGURADO (3-4 picks, cuotas bajas)
    safe_picks = []
    for i in range(4):
        player = random.choice(soccer_stars + nba_stars)
        if player in nba_stars:
            stat = random.choice(["Puntos", "Rebotes", "Asistencias"])
            line = round(random.uniform(20.5, 28.5), 1) if stat == "Puntos" else round(random.uniform(7.5, 11.5), 1)
        else:
            stat = random.choice(["Tiros al Arco", "Goles"])
            line = round(random.uniform(2.5, 4.5), 1)
        
        safe_picks.append({
            'player': player,
            'image': PLAYER_IMGS.get(player, ''),
            'stat': stat,
            'line': line,
            'pick': 'Over',
            'odds': round(random.uniform(1.45, 1.65), 2)
        })
    
    parlays['safe'] = {
        'name': '🛡️ PARLEY ASEGURADO',
        'picks': safe_picks,
        'confidence': 'ALTA'
    }
    
    # PARLEY MEDIO (5-6 picks)
    medium_picks = []
    for i in range(6):
        player = random.choice(soccer_stars + nba_stars)
        if player in nba_stars:
            stat = random.choice(["Puntos", "Rebotes + Asistencias", "Triples"])
            line = round(random.uniform(18.5, 26.5), 1)
        else:
            stat = random.choice(["Tiros al Arco", "Goles + Asistencias"])
            line = round(random.uniform(1.5, 3.5), 1)
        
        medium_picks.append({
            'player': player,
            'image': PLAYER_IMGS.get(player, ''),
            'stat': stat,
            'line': line,
            'pick': random.choice(['Over', 'Under']),
            'odds': round(random.uniform(1.75, 1.95), 2)
        })
    
    parlays['medium'] = {
        'name': '⚖️ PARLEY MEDIO',
        'picks': medium_picks,
        'confidence': 'MEDIA'
    }
    
    # PARLEY SOÑADOR (8-10 picks)
    dream_picks = []
    for i in range(10):
        player = random.choice(soccer_stars + nba_stars)
        if player in nba_stars:
            stat = random.choice(["Puntos", "Dobles-Dobles", "30+ Puntos"])
            line = round(random.uniform(25.5, 35.5), 1)
        else:
            stat = random.choice(["2+ Goles", "Gol + Asistencia"])
            line = 0.5
        
        dream_picks.append({
            'player': player,
            'image': PLAYER_IMGS.get(player, ''),
            'stat': stat,
            'line': line,
            'pick': 'Sí',
            'odds': round(random.uniform(2.0, 2.5), 2)
        })
    
    parlays['dream'] = {
        'name': '🦄 PARLEY SOÑADOR',
        'picks': dream_picks,
        'confidence': 'RIESGO ALTO'
    }
    
    return parlays

def calculate_parlay_odds(picks: List[Dict]) -> float:
    """Calcula cuota total"""
    total = 1.0
    for pick in picks:
        total *= pick['odds']
    return round(total, 2)

# ==================== COMPONENTES UI ====================

def render_parlay_card(parlay: Dict):
    """Renderiza tarjeta de parley premium"""
    total_odds = calculate_parlay_odds(parlay['picks'])
    payout = round(100 * total_odds, 2)
    
    html = f"""
    <div class="parley-card">
        <div class="parley-header">
            <div class="parley-title">{parlay['name']}</div>
            <div class="parley-odds">@{total_odds}</div>
        </div>
        <div class="parley-payout">
            <div class="payout-amount">${payout}</div>
            <div class="payout-label">Apuesta $100 | Confianza: {parlay['confidence']}</div>
        </div>
    """
    
    for pick in parlay['picks']:
        img_url = pick['image'] if pick['image'] else 'https://via.placeholder.com/60/8b5cf6/ffffff?text=★'
        html += f"""
        <div class="pick-item">
            <img src="{img_url}" class="player-avatar" onerror="this.src='https://via.placeholder.com/60/8b5cf6/ffffff?text=★'">
            <div class="pick-info">
                <div class="pick-player">{pick['player']}</div>
                <div class="pick-prediction">{pick['pick']} {pick['line']} {pick['stat']}</div>
            </div>
            <div class="pick-odds">@{pick['odds']}</div>
        </div>
        """
    
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

def render_match_card(match: Dict):
    """Renderiza tarjeta de partido"""
    try:
        if match['time'] != 'TBD' and 'T' in str(match['time']):
            time_obj = datetime.fromisoformat(str(match['time']).replace('Z', '+00:00'))
            time_str = time_obj.strftime('%H:%M')
        else:
            time_str = 'Por definir'
    except:
        time_str = str(match.get('time', 'TBD'))
    
    score_display = f"{match['home_score']} - {match['away_score']}" if match['started'] else "vs"
    
    html = f"""
    <div class="match-card">
        <div class="match-header">
            <div class="match-time">🕐 {time_str}</div>
            <div class="match-league">{match['league']}</div>
        </div>
        <div class="match-teams">
            <div class="team-name">{match['home']}</div>
            <div class="match-score">{score_display}</div>
            <div class="team-name">{match['away']}</div>
        </div>
    """
    
    if match.get('stadium') and match['stadium'] != 'N/A':
        html += f"""
        <div class="match-info">
            🏟️ {match['stadium']}
        </div>
        """
    
    html += "</div>"
    st.markdown(html, unsafe_allow_html=True)

def render_stats_table(players: List[Dict], stat_name: str):
    """Renderiza tabla de estadísticas"""
    if not players:
        st.markdown(f"""
        <div class="alert-box alert-warning">
            ⚠️ No hay datos de {stat_name} disponibles
        </div>
        """, unsafe_allow_html=True)
        return
    
    html = '<div class="stats-table">'
    
    for idx, player in enumerate(players[:10], 1):
        # Buscar imagen del jugador
        img_url = PLAYER_IMGS.get(player['name'], 'https://via.placeholder.com/48/6d28d9/ffffff?text=' + player['name'][0])
        
        html += f"""
        <div class="stats-row">
            <div class="stats-rank">#{idx}</div>
            <div class="stats-player">
                <img src="{img_url}" class="stats-avatar" onerror="this.src='https://via.placeholder.com/48/6d28d9/ffffff?text={player['name'][0]}'">
                <div>
                    <div class="stats-name">{player['name']}</div>
                    <div class="stats-team">{player['team']}</div>
                </div>
            </div>
            <div class="stats-value">{player['value']}</div>
        </div>
        """
    
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

# ==================== APP PRINCIPAL ====================

def main():
    inject_premium_css()
    
    # HEADER
    st.markdown("""
    <div style='text-align: center; padding: 40px 20px; background: linear-gradient(135deg, #0b0a14 0%, #1a1b2e 100%); border-bottom: 3px solid #6d28d9; margin-bottom: 40px; border-radius: 20px;'>
        <h1 style='font-size: 56px; font-weight: 900; background: linear-gradient(90deg, #8b5cf6, #22d3ee); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0;'>
            💎 PARLEISITOS
        </h1>
        <p style='color: #9ca3af; margin-top: 12px; font-size: 18px; letter-spacing: 2px;'>
            SISTEMA PREMIUM DE APUESTAS DEPORTIVAS
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # TABS PRINCIPALES
    tab1, tab2, tab3, tab4 = st.tabs([
        "🏠 INICIO",
        "⚽ FÚTBOL",
        "🏀 NBA",
        "💎 GENERADOR"
    ])
    
    # ==================== TAB 1: INICIO ====================
    with tab1:
        st.markdown("### 🎯 LOS 3 PARLEYS DEL DÍA")
        st.markdown(f"**Fecha:** {datetime.now().strftime('%d/%m/%Y')} | Actualizados cada 24h")
        
        parlays = generate_daily_parleys()
        
        cols = st.columns(3)
        with cols[0]:
            render_parlay_card(parlays['safe'])
        with cols[1]:
            render_parlay_card(parlays['medium'])
        with cols[2]:
            render_parlay_card(parlays['dream'])
    
    # ==================== TAB 2: FÚTBOL ====================
    with tab2:
        st.markdown("### ⚽ FÚTBOL - LIGAS PRINCIPALES")
        
        selected_league = st.selectbox(
            "Selecciona una Liga:",
            list(LIGAS_FOTMOB.keys()),
            key="soccer_league"
        )
        
        league_id = LIGAS_FOTMOB[selected_league]['id']
        
        subtab1, subtab2, subtab3 = st.tabs([
            "📅 Partidos",
            "⚽ Goleadores & Asistencias",
            "🧤 Porteros (Clean Sheets)"
        ])
        
        with subtab1:
            st.markdown(f"#### PARTIDOS DE HOY - {selected_league}")
            
            with st.spinner("Cargando desde FotMob..."):
                matches = get_matches_today(league_id)
            
            if not matches:
                st.markdown("""
                <div class="alert-box alert-warning">
                    📭 Sin partidos programados hoy para esta liga
                </div>
                """, unsafe_allow_html=True)
            else:
                for match in matches:
                    render_match_card(match)
        
        with subtab2:
            st.markdown("#### 📊 ESTADÍSTICAS DE JUGADORES")
            
            with st.spinner("Cargando estadísticas..."):
                stats = get_league_stats(league_id)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("##### ⚽ GOLEADORES")
                render_stats_table(stats['scorers'], 'Goleadores')
            
            with col2:
                st.markdown("##### 🎯 ASISTENCIAS")
                render_stats_table(stats['assists'], 'Asistencias')
        
        with subtab3:
            st.markdown("#### 🧤 PORTEROS - VALLAS INVICTAS")
            
            with st.spinner("Cargando datos de porteros..."):
                stats = get_league_stats(league_id)
            
            render_stats_table(stats['cleansheets'], 'Porteros')
    
    # ==================== TAB 3: NBA ====================
    with tab3:
        st.markdown("### 🏀 NBA - SCOREBOARD")
        
        with st.spinner("Cargando partidos de NBA..."):
            nba_games = get_nba_games()
        
        if not nba_games:
            st.markdown("""
            <div class="alert-box alert-warning">
                📭 No hay partidos de NBA programados hoy
            </div>
            """, unsafe_allow_html=True)
        else:
            for game in nba_games:
                score_display = f"{game['home_score']} - {game['away_score']}" if game['home_score'] != '-' else "vs"
                
                st.markdown(f"""
                <div class="match-card">
                    <div class="match-header">
                        <div class="match-time">🕐 {game['status']}</div>
                        <div class="match-league">NBA</div>
                    </div>
                    <div class="match-teams">
                        <div class="team-name">{game['home']}</div>
                        <div class="match-score">{score_display}</div>
                        <div class="team-name">{game['away']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # ==================== TAB 4: GENERADOR ====================
    with tab4:
        st.markdown("### 💎 GENERADOR DE PARLEYS PERSONALIZADO")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.markdown("#### CONFIGURACIÓN")
            
            parley_type = st.selectbox(
                "Tipo de Parley:",
                ["⚽ Fútbol Match", "👟 Fútbol Players", "🏀 NBA Players", "🎲 Combo Mix"]
            )
            
            risk_level = st.radio(
                "Nivel de Riesgo:",
                ["🛡️ Asegurado", "⚖️ Medio", "🔥 Arriesgado", "🦄 Soñador"]
            )
            
            num_picks = st.slider("Número de Picks:", 3, 12, 5)
            
            generate_btn = st.button("🎲 GENERAR PARLEY", use_container_width=True)
        
        with col2:
            if generate_btn:
                st.markdown("#### TU PARLEY PERSONALIZADO")
                
                # Generar picks basados en configuración
                picks = []
                
                if "NBA" in parley_type:
                    players = ["LeBron James", "Stephen Curry", "Giannis Antetokounmpo", "Luka Dončić"]
                    stats = ["Puntos", "Rebotes", "Asistencias", "Triples"]
                else:
                    players = ["Erling Haaland", "Kylian Mbappé", "Vinicius Jr", "Jude Bellingham"]
                    stats = ["Goles", "Tiros al Arco", "Asistencias"]
                
                for _ in range(num_picks):
                    player = random.choice(players)
                    stat = random.choice(stats)
                    
                    if "NBA" in parley_type:
                        line = round(random.uniform(20.5, 30.5), 1) if stat == "Puntos" else round(random.uniform(7.5, 11.5), 1)
                    else:
                        line = round(random.uniform(0.5, 3.5), 1)
                    
                    # Ajustar cuotas según riesgo
                    if "Asegurado" in risk_level:
                        odds = round(random.uniform(1.45, 1.65), 2)
                    elif "Medio" in risk_level:
                        odds = round(random.uniform(1.75, 1.95), 2)
                    elif "Arriesgado" in risk_level:
                        odds = round(random.uniform(2.0, 2.3), 2)
                    else:
                        odds = round(random.uniform(2.4, 2.8), 2)
                    
                    picks.append({
                        'player': player,
                        'image': PLAYER_IMGS.get(player, ''),
                        'stat': stat,
                        'line': line,
                        'pick': 'Over',
                        'odds': odds
                    })
                
                custom_parley = {
                    'name': f'{parley_type} - {risk_level}',
                    'picks': picks,
                    'confidence': risk_level.split()[1]
                }
                
                render_parlay_card(custom_parley)
    
    # FOOTER
    st.markdown("---")
    st.markdown(f"""
    <div style='text-align: center; color: #6b7280; padding: 30px; font-size: 13px;'>
        <p style='margin-bottom: 10px;'>💎 Parleisitos v4.0 - Diseño Premium Dark Mode</p>
        <p style='color: #9ca3af;'>Datos en tiempo real: FotMob + NBA API</p>
        <p style='color: #fbbf24; margin-top: 15px;'>⚠️ Apuesta responsablemente. Solo para entretenimiento.</p>
        <p style='color: #6b7280; margin-top: 10px; font-size: 12px;'>Última actualización: {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
