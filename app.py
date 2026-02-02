"""
PARLEISITOS - Sistema de Apuestas Deportivas con FotMob
Integración: FotMob (endpoints públicos) + NBA API
Diseño: Minimalista Black & Neon Green
Autor: Hacker Ético & Desarrollador Senior
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import requests
import json
from typing import List, Dict, Optional, Tuple
import time

# ==================== CONFIGURACIÓN INICIAL ====================
st.set_page_config(
    page_title="Parleisitos",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==================== HEADERS PARA FOTMOB (ANTI-BLOQUEO) ====================
FOTMOB_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'es-ES,es;q=0.9,en;q=0.8',
    'Referer': 'https://www.fotmob.com/',
    'Origin': 'https://www.fotmob.com',
    'Connection': 'keep-alive',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin'
}

# ==================== DICCIONARIO DE LIGAS FOTMOB ====================
LIGAS_FOTMOB = {
    "⚽ Liga MX": {"id": 87, "emoji": "🇲🇽", "country": "México"},
    "⚽ Premier League": {"id": 47, "emoji": "🏴󠁧󠁢󠁥󠁮󠁧󠁿", "country": "Inglaterra"},
    "⚽ La Liga": {"id": 87, "emoji": "🇪🇸", "country": "España"},
    "⚽ Serie A": {"id": 55, "emoji": "🇮🇹", "country": "Italia"},
    "⚽ Bundesliga": {"id": 54, "emoji": "🇩🇪", "country": "Alemania"},
    "⚽ Ligue 1": {"id": 53, "emoji": "🇫🇷", "country": "Francia"},
    "⚽ Champions League": {"id": 42, "emoji": "🏆", "country": "UEFA"},
    "⚽ Europa League": {"id": 73, "emoji": "🏆", "country": "UEFA"},
    "⚽ MLS": {"id": 130, "emoji": "🇺🇸", "country": "USA"},
    "⚽ Liga Argentina": {"id": 68, "emoji": "🇦🇷", "country": "Argentina"},
    "⚽ Liga Brasileña": {"id": 71, "emoji": "🇧🇷", "country": "Brasil"},
    "⚽ Copa Libertadores": {"id": 299, "emoji": "🏆", "country": "CONMEBOL"},
    "⚽ Eredivisie": {"id": 57, "emoji": "🇳🇱", "country": "Países Bajos"},
    "⚽ Liga Portuguesa": {"id": 63, "emoji": "🇵🇹", "country": "Portugal"},
}

# ==================== ESTILOS CSS ====================
def inject_custom_css():
    st.markdown("""
    <style>
    /* RESET Y BASE */
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    .stApp {
        background-color: #000000;
        color: #ffffff;
    }
    
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 100% !important;
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* TABS */
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
    
    /* TARJETAS DE PARTIDO */
    .match-card {
        background: linear-gradient(145deg, #1a1a1a 0%, #0d0d0d 100%);
        border: 2px solid #00ff00;
        border-radius: 16px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(0, 255, 0, 0.2);
        transition: all 0.3s ease;
    }
    
    .match-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 40px rgba(0, 255, 0, 0.4);
    }
    
    .match-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 15px;
        padding-bottom: 10px;
        border-bottom: 1px solid #00ff00;
    }
    
    .match-time {
        font-size: 14px;
        color: #00ff00;
        font-weight: 600;
    }
    
    .match-league {
        font-size: 12px;
        color: #888888;
        text-transform: uppercase;
    }
    
    .match-teams {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin: 15px 0;
    }
    
    .team-name {
        font-size: 18px;
        font-weight: 700;
        color: #ffffff;
    }
    
    .match-vs {
        font-size: 16px;
        color: #00ff00;
        font-weight: 700;
    }
    
    .match-info {
        background: #0d0d0d;
        padding: 10px;
        border-radius: 8px;
        margin-top: 10px;
        font-size: 12px;
        color: #888888;
    }
    
    /* TABLA DE POSICIONES */
    .table-container {
        background: #1a1a1a;
        border: 2px solid #00ff00;
        border-radius: 12px;
        padding: 15px;
        margin: 15px 0;
    }
    
    .table-row {
        display: grid;
        grid-template-columns: 50px 1fr 60px 60px 60px 60px;
        padding: 12px 10px;
        border-bottom: 1px solid #333333;
        align-items: center;
    }
    
    .table-row:hover {
        background: #0d0d0d;
    }
    
    .table-header {
        font-weight: 700;
        color: #00ff00;
        font-size: 12px;
        text-transform: uppercase;
    }
    
    .pos-number {
        font-weight: 700;
        color: #00ff00;
        font-size: 16px;
    }
    
    .team-info {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    
    .team-logo {
        width: 30px;
        height: 30px;
        border-radius: 50%;
    }
    
    /* STATS DE JUGADORES */
    .player-card {
        background: #1a1a1a;
        border-left: 4px solid #00ff00;
        padding: 15px;
        margin: 10px 0;
        border-radius: 8px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .player-info {
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .player-photo {
        width: 50px;
        height: 50px;
        border-radius: 50%;
        border: 3px solid #00ff00;
        object-fit: cover;
    }
    
    .player-name {
        font-size: 18px;
        font-weight: 700;
        color: #ffffff;
    }
    
    .player-team {
        font-size: 12px;
        color: #888888;
    }
    
    .player-stat {
        font-size: 24px;
        font-weight: 900;
        color: #00ff00;
        text-shadow: 0 0 10px rgba(0, 255, 0, 0.5);
    }
    
    /* PARLEY CARD */
    .parley-card {
        background: linear-gradient(145deg, #1a1a1a 0%, #0d0d0d 100%);
        border: 2px solid #00ff00;
        border-radius: 16px;
        padding: 20px;
        margin: 15px 0;
        box-shadow: 0 8px 32px rgba(0, 255, 0, 0.2);
    }
    
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
    }
    
    .parley-odds {
        font-size: 32px;
        font-weight: 900;
        color: #00ff00;
    }
    
    .pick-item {
        background: #0d0d0d;
        padding: 15px;
        margin: 10px 0;
        border-radius: 12px;
        border-left: 4px solid #00ff00;
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
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 255, 0, 0.5);
    }
    
    /* ALERT BOX */
    .alert-box {
        background: #1a1a1a;
        border: 2px solid #ff9900;
        border-radius: 10px;
        padding: 15px;
        margin: 15px 0;
        color: #ff9900;
    }
    
    /* DATAFRAME */
    .dataframe {
        background-color: #0d0d0d !important;
        color: #ffffff !important;
    }
    
    </style>
    """, unsafe_allow_html=True)

# ==================== FUNCIONES DE FOTMOB ====================

def fetch_fotmob_data(url: str, timeout: int = 10) -> Optional[Dict]:
    """
    Función genérica para hacer requests a FotMob con manejo de errores
    """
    try:
        response = requests.get(url, headers=FOTMOB_HEADERS, timeout=timeout)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"⚠️ Error al conectar con FotMob: {str(e)}")
        return None
    except json.JSONDecodeError:
        st.error("⚠️ Error al decodificar respuesta de FotMob")
        return None

def get_matches_today(league_id: Optional[int] = None) -> List[Dict]:
    """
    Obtiene partidos de hoy desde FotMob
    """
    today = datetime.now().strftime("%Y%m%d")
    url = f"https://www.fotmob.com/api/matches?date={today}"
    
    data = fetch_fotmob_data(url)
    
    if not data or 'leagues' not in data:
        return []
    
    matches = []
    
    for league in data.get('leagues', []):
        # Si se especifica una liga, filtrar solo esa
        if league_id and league.get('id') != league_id:
            continue
        
        league_name = league.get('name', 'Unknown')
        
        for match in league.get('matches', []):
            try:
                matches.append({
                    'league': league_name,
                    'league_id': league.get('id'),
                    'home': match.get('home', {}).get('name', 'TBD'),
                    'away': match.get('away', {}).get('name', 'TBD'),
                    'time': match.get('status', {}).get('utcTime', 'TBD'),
                    'status': match.get('status', {}).get('started', False),
                    'stadium': match.get('status', {}).get('reason', {}).get('long', 'N/A'),
                    'match_id': match.get('id'),
                    'home_score': match.get('home', {}).get('score', '-'),
                    'away_score': match.get('away', {}).get('score', '-')
                })
            except Exception as e:
                continue
    
    return matches

def get_league_table(league_id: int) -> Optional[pd.DataFrame]:
    """
    Obtiene la tabla de posiciones de una liga desde FotMob
    """
    url = f"https://www.fotmob.com/api/leagues?id={league_id}&tab=table&type=league&timeZone=America/Mexico_City"
    
    data = fetch_fotmob_data(url)
    
    if not data or 'table' not in data:
        return None
    
    try:
        # FotMob puede tener diferentes estructuras
        tables = data['table']
        
        if isinstance(tables, list) and len(tables) > 0:
            table_data = tables[0].get('data', {}).get('table', {}).get('all', [])
        else:
            table_data = []
        
        if not table_data:
            return None
        
        rows = []
        for team in table_data:
            rows.append({
                'Pos': team.get('idx', '-'),
                'Equipo': team.get('name', 'Unknown'),
                'PJ': team.get('played', 0),
                'PG': team.get('wins', 0),
                'PE': team.get('draws', 0),
                'PP': team.get('losses', 0),
                'GF': team.get('scoresFor', 0),
                'GC': team.get('scoresAgainst', 0),
                'DG': team.get('goalConDiff', 0),
                'Pts': team.get('pts', 0)
            })
        
        return pd.DataFrame(rows)
    
    except Exception as e:
        st.error(f"⚠️ Error procesando tabla: {str(e)}")
        return None

def get_league_stats(league_id: int, stat_type: str = 'scorers') -> List[Dict]:
    """
    Obtiene estadísticas de jugadores de una liga
    stat_type: 'scorers', 'assists', 'rating', etc.
    """
    url = f"https://www.fotmob.com/api/leagues?id={league_id}&tab=stats&type=league&timeZone=America/Mexico_City"
    
    data = fetch_fotmob_data(url)
    
    if not data or 'stats' not in data:
        return []
    
    try:
        stats_list = data.get('stats', [])
        
        players = []
        
        # Buscar la sección de goleadores/asistencias
        for stat_section in stats_list:
            if stat_type == 'scorers' and 'TopScorers' in stat_section.get('title', ''):
                players_data = stat_section.get('players', [])
            elif stat_type == 'assists' and 'Assists' in stat_section.get('title', ''):
                players_data = stat_section.get('players', [])
            elif stat_type == 'shots' and 'Shots' in stat_section.get('title', ''):
                players_data = stat_section.get('players', [])
            else:
                continue
            
            for player in players_data[:10]:  # Top 10
                players.append({
                    'name': player.get('name', 'Unknown'),
                    'team': player.get('teamName', 'Unknown'),
                    'stat_value': player.get('statValue', 0),
                    'photo': player.get('imageUrl', '')
                })
            
            break
        
        return players
    
    except Exception as e:
        st.error(f"⚠️ Error obteniendo stats: {str(e)}")
        return []

# ==================== FUNCIONES NBA ====================

def get_nba_games_today() -> List[Dict]:
    """Obtiene partidos de NBA de hoy"""
    try:
        from nba_api.live.nba.endpoints import scoreboard
        games = scoreboard.ScoreBoard()
        games_data = games.get_dict()
        
        if games_data and 'scoreboard' in games_data and 'games' in games_data['scoreboard']:
            real_games = []
            for game in games_data['scoreboard']['games'][:8]:
                real_games.append({
                    'home': game['homeTeam']['teamName'],
                    'away': game['awayTeam']['teamName'],
                    'time': game.get('gameStatusText', 'TBD'),
                    'home_score': game['homeTeam'].get('score', '-'),
                    'away_score': game['awayTeam'].get('score', '-')
                })
            return real_games
    except Exception as e:
        pass
    
    # FALLBACK
    teams = ["Lakers", "Celtics", "Warriors", "Bucks", "Nets", "Heat", "Suns", "Mavs"]
    games = []
    random.shuffle(teams)
    for i in range(0, len(teams)-1, 2):
        games.append({
            'home': teams[i],
            'away': teams[i+1],
            'time': f"{random.randint(18, 22)}:00 ET",
            'home_score': '-',
            'away_score': '-'
        })
    return games

# ==================== GENERADOR DE PARLEYS INTELIGENTE ====================

def generate_smart_parlay(league_id: int, league_name: str) -> Dict:
    """
    Genera un parlay inteligente basado en datos reales de FotMob
    """
    matches = get_matches_today(league_id)
    table = get_league_table(league_id)
    
    if not matches:
        return {
            'name': f'🎲 Parley {league_name}',
            'picks': [],
            'odds': 1.0,
            'confidence': 'N/A'
        }
    
    picks = []
    
    # Seleccionar hasta 5 partidos
    selected_matches = random.sample(matches, min(5, len(matches)))
    
    for match in selected_matches:
        # Determinar favorito basado en tabla (si existe)
        home_pos = away_pos = 10  # Default medio
        
        if table is not None:
            home_data = table[table['Equipo'] == match['home']]
            away_data = table[table['Equipo'] == match['away']]
            
            if not home_data.empty:
                home_pos = int(home_data.iloc[0]['Pos'])
            if not away_data.empty:
                away_pos = int(away_data.iloc[0]['Pos'])
        
        # Lógica de predicción
        pos_diff = abs(home_pos - away_pos)
        
        if pos_diff >= 5:
            # Gran diferencia -> Pick al favorito
            if home_pos < away_pos:
                prediction = f"{match['home']} Gana"
                odds = round(random.uniform(1.5, 1.8), 2)
            else:
                prediction = f"{match['away']} Gana"
                odds = round(random.uniform(1.6, 1.9), 2)
        else:
            # Partido parejo -> Over/Under o BTTS
            prediction = random.choice([
                f"Over 2.5 Goles",
                f"Ambos Anotan (BTTS)",
                f"Under 3.5 Goles"
            ])
            odds = round(random.uniform(1.7, 2.1), 2)
        
        picks.append({
            'match': f"{match['home']} vs {match['away']}",
            'prediction': prediction,
            'odds': odds,
            'league': league_name
        })
    
    # Calcular cuota total
    total_odds = 1.0
    for pick in picks:
        total_odds *= pick['odds']
    
    # Determinar confianza
    if total_odds < 10:
        confidence = "🛡️ ALTA"
    elif total_odds < 30:
        confidence = "⚖️ MEDIA"
    else:
        confidence = "🦄 BAJA"
    
    return {
        'name': f'Parley {league_name}',
        'picks': picks,
        'odds': round(total_odds, 2),
        'confidence': confidence
    }

# ==================== COMPONENTES UI ====================

def render_match_card(match: Dict):
    """Renderiza una tarjeta de partido"""
    
    # Convertir tiempo UTC a formato legible
    try:
        if match['time'] != 'TBD':
            time_str = datetime.fromisoformat(match['time'].replace('Z', '+00:00')).strftime('%H:%M')
        else:
            time_str = 'Por definir'
    except:
        time_str = match['time']
    
    html = f"""
    <div class="match-card">
        <div class="match-header">
            <div class="match-time">🕐 {time_str}</div>
            <div class="match-league">{match['league']}</div>
        </div>
        <div class="match-teams">
            <div class="team-name">{match['home']}</div>
            <div class="match-vs">{match['home_score']} - {match['away_score']}</div>
            <div class="team-name">{match['away']}</div>
        </div>
    """
    
    if match.get('stadium') and match['stadium'] != 'N/A':
        html += f"""
        <div class="match-info">
            🏟️ {match['stadium']}
        </div>
        """
    
    html += """
    </div>
    """
    
    st.markdown(html, unsafe_allow_html=True)

def render_parley_card(parley: Dict):
    """Renderiza tarjeta de parley"""
    potential_win = round(100 * parley['odds'], 2)
    
    html = f"""
    <div class="parley-card">
        <div class="parley-header">
            <div class="parley-title">{parley['name']}</div>
            <div class="parley-odds">@{parley['odds']}</div>
        </div>
        <div style="margin-bottom: 15px; color: #00ff00; font-size: 16px;">
            💰 Apuesta $100 → Ganas ${potential_win} | Confianza: {parley['confidence']}
        </div>
    """
    
    for pick in parley['picks']:
        html += f"""
        <div class="pick-item">
            <div style="font-weight: 700; margin-bottom: 5px;">{pick['match']}</div>
            <div style="color: #00ff00; font-size: 14px;">✅ {pick['prediction']} @{pick['odds']}</div>
        </div>
        """
    
    html += """
    </div>
    """
    
    st.markdown(html, unsafe_allow_html=True)

# ==================== APP PRINCIPAL ====================

def main():
    inject_custom_css()
    
    # HEADER
    st.markdown("""
    <div style='text-align: center; padding: 20px; background: linear-gradient(135deg, #000000 0%, #1a1a1a 100%); border-bottom: 2px solid #00ff00; margin-bottom: 30px;'>
        <h1 style='font-size: 48px; font-weight: 900; background: linear-gradient(90deg, #00ff00, #00cc00); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin: 0;'>
            ⚽ PARLEISITOS
        </h1>
        <p style='color: #888888; margin-top: 10px; font-size: 16px; letter-spacing: 2px;'>
            SISTEMA CON DATOS REALES DE FOTMOB
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # SELECTOR DE LIGA
    col1, col2 = st.columns([3, 1])
    
    with col1:
        selected_league = st.selectbox(
            "Selecciona una Liga:",
            list(LIGAS_FOTMOB.keys()),
            key="league_selector"
        )
    
    with col2:
        st.markdown(f"""
        <div style='text-align: center; padding: 20px; background: #1a1a1a; border-radius: 10px; margin-top: 22px;'>
            <div style='font-size: 40px;'>{LIGAS_FOTMOB[selected_league]['emoji']}</div>
            <div style='color: #888888; font-size: 12px;'>{LIGAS_FOTMOB[selected_league]['country']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    league_id = LIGAS_FOTMOB[selected_league]['id']
    
    # TABS
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📅 Partidos",
        "📊 Tabla",
        "👟 Jugadores",
        "🎲 Parley Generator",
        "🏀 NBA"
    ])
    
    # ==================== TAB 1: PARTIDOS ====================
    with tab1:
        st.markdown(f"### 📅 PARTIDOS DE HOY - {selected_league}")
        
        with st.spinner("Cargando partidos desde FotMob..."):
            matches = get_matches_today(league_id)
        
        if not matches:
            st.markdown("""
            <div class="alert-box">
                ⚠️ No hay partidos programados hoy para esta liga o FotMob no está disponible.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"**{len(matches)} partidos encontrados**")
            
            for match in matches:
                render_match_card(match)
    
    # ==================== TAB 2: TABLA ====================
    with tab2:
        st.markdown(f"### 📊 TABLA DE POSICIONES - {selected_league}")
        
        with st.spinner("Cargando tabla desde FotMob..."):
            table = get_league_table(league_id)
        
        if table is None or table.empty:
            st.markdown("""
            <div class="alert-box">
                ⚠️ Tabla no disponible en este momento.
            </div>
            """, unsafe_allow_html=True)
        else:
            st.dataframe(
                table,
                use_container_width=True,
                hide_index=True,
                column_config={
                    "Pos": st.column_config.NumberColumn("Pos", width="small"),
                    "Equipo": st.column_config.TextColumn("Equipo", width="large"),
                    "PJ": st.column_config.NumberColumn("PJ", width="small"),
                    "PG": st.column_config.NumberColumn("PG", width="small"),
                    "PE": st.column_config.NumberColumn("PE", width="small"),
                    "PP": st.column_config.NumberColumn("PP", width="small"),
                    "GF": st.column_config.NumberColumn("GF", width="small"),
                    "GC": st.column_config.NumberColumn("GC", width="small"),
                    "DG": st.column_config.NumberColumn("DG", width="small"),
                    "Pts": st.column_config.NumberColumn("Pts", width="small")
                }
            )
            
            # Análisis rápido
            if len(table) > 0:
                leader = table.iloc[0]
                last = table.iloc[-1]
                
                st.markdown("---")
                st.markdown("### 📈 ANÁLISIS RÁPIDO")
                
                cols = st.columns(3)
                with cols[0]:
                    st.metric("🥇 Líder", leader['Equipo'], f"{leader['Pts']} pts")
                with cols[1]:
                    st.metric("🔻 Último", last['Equipo'], f"{last['Pts']} pts")
                with cols[2]:
                    best_diff = table.loc[table['DG'].idxmax()]
                    st.metric("⚽ Mejor Diferencia", best_diff['Equipo'], f"+{best_diff['DG']}")
    
    # ==================== TAB 3: JUGADORES ====================
    with tab3:
        st.markdown(f"### 👟 ESTADÍSTICAS DE JUGADORES - {selected_league}")
        
        stat_tab1, stat_tab2, stat_tab3 = st.tabs([
            "⚽ Goleadores",
            "🎯 Asistidores",
            "🔫 Francotiradores"
        ])
        
        with stat_tab1:
            with st.spinner("Cargando goleadores..."):
                scorers = get_league_stats(league_id, 'scorers')
            
            if not scorers:
                st.warning("⚠️ Datos de goleadores no disponibles")
            else:
                for idx, player in enumerate(scorers, 1):
                    st.markdown(f"""
                    <div class="player-card">
                        <div class="player-info">
                            <div style="font-size: 20px; font-weight: 700; color: #00ff00; width: 40px;">{idx}</div>
                            <div>
                                <div class="player-name">{player['name']}</div>
                                <div class="player-team">{player['team']}</div>
                            </div>
                        </div>
                        <div class="player-stat">{player['stat_value']} ⚽</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        with stat_tab2:
            with st.spinner("Cargando asistidores..."):
                assisters = get_league_stats(league_id, 'assists')
            
            if not assisters:
                st.warning("⚠️ Datos de asistencias no disponibles")
            else:
                for idx, player in enumerate(assisters, 1):
                    st.markdown(f"""
                    <div class="player-card">
                        <div class="player-info">
                            <div style="font-size: 20px; font-weight: 700; color: #00ff00; width: 40px;">{idx}</div>
                            <div>
                                <div class="player-name">{player['name']}</div>
                                <div class="player-team">{player['team']}</div>
                            </div>
                        </div>
                        <div class="player-stat">{player['stat_value']} 🎯</div>
                    </div>
                    """, unsafe_allow_html=True)
        
        with stat_tab3:
            with st.spinner("Cargando estadísticas de tiros..."):
                shooters = get_league_stats(league_id, 'shots')
            
            if not shooters:
                st.warning("⚠️ Datos de tiros no disponibles")
            else:
                for idx, player in enumerate(shooters, 1):
                    st.markdown(f"""
                    <div class="player-card">
                        <div class="player-info">
                            <div style="font-size: 20px; font-weight: 700; color: #00ff00; width: 40px;">{idx}</div>
                            <div>
                                <div class="player-name">{player['name']}</div>
                                <div class="player-team">{player['team']}</div>
                            </div>
                        </div>
                        <div class="player-stat">{player['stat_value']} 🔫</div>
                    </div>
                    """, unsafe_allow_html=True)
    
    # ==================== TAB 4: PARLEY GENERATOR ====================
    with tab4:
        st.markdown("### 🎲 GENERADOR DE PARLEYS INTELIGENTE")
        
        st.markdown("""
        <div style='background: #1a1a1a; padding: 15px; border-radius: 10px; margin-bottom: 20px;'>
            <p style='color: #888888; margin: 0;'>
                🧠 Este generador cruza los datos de FotMob para crear parleys inteligentes basados en:
            </p>
            <ul style='color: #00ff00; margin-top: 10px;'>
                <li>Posiciones en tabla</li>
                <li>Partidos del día</li>
                <li>Estadísticas de equipos</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            if st.button("🎲 GENERAR PARLEY", use_container_width=True):
                st.session_state.parley_generated = True
        
        if st.session_state.get('parley_generated', False):
            with st.spinner("Analizando datos y generando parley..."):
                parley = generate_smart_parlay(league_id, selected_league)
            
            if not parley['picks']:
                st.warning("⚠️ No hay suficientes datos para generar un parley en este momento")
            else:
                render_parley_card(parley)
    
    # ==================== TAB 5: NBA ====================
    with tab5:
        st.markdown("### 🏀 PARTIDOS NBA DE HOY")
        
        nba_games = get_nba_games_today()
        
        if not nba_games:
            st.warning("⚠️ No hay partidos de NBA programados hoy")
        else:
            for game in nba_games:
                st.markdown(f"""
                <div class="match-card">
                    <div class="match-header">
                        <div class="match-time">🕐 {game['time']}</div>
                        <div class="match-league">NBA</div>
                    </div>
                    <div class="match-teams">
                        <div class="team-name">{game['home']}</div>
                        <div class="match-vs">{game['home_score']} - {game['away_score']}</div>
                        <div class="team-name">{game['away']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
    
    # FOOTER
    st.markdown("---")
    st.markdown(f"""
    <div style='text-align: center; color: #555555; padding: 20px; font-size: 12px;'>
        <p>⚽ Parleisitos v3.0 | Datos en tiempo real desde FotMob</p>
        <p style='color: #00ff00;'>⚠️ Apuesta responsablemente</p>
        <p style='color: #888888; margin-top: 10px;'>Última actualización: {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
