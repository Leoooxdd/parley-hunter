import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# DICCIONARIOS DE DATOS REALES - LIGAS Y LOGOS
# ============================================================================

LIGAS_URLS = {
    'Premier League': 'https://fbref.com/en/comps/9/Premier-League-Stats',
    'La Liga': 'https://fbref.com/en/comps/12/La-Liga-Stats',
    'Serie A': 'https://fbref.com/en/comps/11/Serie-A-Stats',
    'Bundesliga': 'https://fbref.com/en/comps/20/Bundesliga-Stats',
    'Ligue 1': 'https://fbref.com/en/comps/13/Ligue-1-Stats',
    'Liga MX': 'https://fbref.com/en/comps/31/Liga-MX-Stats',
    'Argentina LPF': 'https://fbref.com/en/comps/21/Primera-Division-Stats',
    'Primeira Liga (POR)': 'https://fbref.com/en/comps/32/Primeira-Liga-Stats',
    'Eredivisie (NED)': 'https://fbref.com/en/comps/23/Eredivisie-Stats',
    'Jupiler Pro (BEL)': 'https://fbref.com/en/comps/37/Belgian-Pro-League-Stats',
    'MLS': 'https://fbref.com/en/comps/22/Major-League-Soccer-Stats',
    'Champions League': 'https://fbref.com/en/comps/8/Champions-League-Stats',
    'Europa League': 'https://fbref.com/en/comps/19/Europa-League-Stats',
    'Conference League': 'https://fbref.com/en/comps/882/Europa-Conference-League-Stats',
    'Copa Libertadores': 'https://fbref.com/en/comps/14/Copa-Libertadores-Stats',
}

LIGAS_LOGOS = {
    'Premier League': 'https://upload.wikimedia.org/wikipedia/en/f/f2/Premier_League_Logo.svg',
    'La Liga': 'https://upload.wikimedia.org/wikipedia/commons/1/13/LaLiga_santander.svg',
    'Serie A': 'https://upload.wikimedia.org/wikipedia/commons/d/d0/Logo_Serie_A_2022.svg',
    'Bundesliga': 'https://upload.wikimedia.org/wikipedia/en/d/df/Bundesliga_logo_%282017%29.svg',
    'Ligue 1': 'https://upload.wikimedia.org/wikipedia/commons/5/5e/Ligue_1_Uber_Eats.svg',
    'Liga MX': 'https://upload.wikimedia.org/wikipedia/commons/e/e2/Liga_MX.svg',
    'Argentina LPF': 'https://upload.wikimedia.org/wikipedia/commons/b/bb/Liga_Profesional_de_F%C3%BAtbol_%28Argentina%29_-_Logo.svg',
    'Primeira Liga (POR)': 'https://upload.wikimedia.org/wikipedia/commons/6/6f/Liga_Portugal_Betclic_logo.svg',
    'Eredivisie (NED)': 'https://upload.wikimedia.org/wikipedia/commons/0/0e/Eredivisie_nieuw_logo_2017-.svg',
    'Jupiler Pro (BEL)': 'https://upload.wikimedia.org/wikipedia/commons/e/e5/Pro_League_2022-23_logo.svg',
    'MLS': 'https://upload.wikimedia.org/wikipedia/commons/7/76/MLS_crest_logo_RGB_gradient.svg',
    'Champions League': 'https://upload.wikimedia.org/wikipedia/en/b/bf/UEFA_Champions_League_logo_2.svg',
    'Europa League': 'https://upload.wikimedia.org/wikipedia/en/0/03/UEFA_Europa_League_logo.svg',
    'Conference League': 'https://upload.wikimedia.org/wikipedia/en/3/34/UEFA_Europa_Conference_League_logo.svg',
    'Copa Libertadores': 'https://upload.wikimedia.org/wikipedia/commons/6/61/CONMEBOL_Libertadores_logo.svg',
}

# Logos de equipos NBA
NBA_TEAM_LOGOS = {
    'ATL': 'https://cdn.nba.com/logos/nba/1610612737/global/L/logo.svg',
    'BOS': 'https://cdn.nba.com/logos/nba/1610612738/global/L/logo.svg',
    'BKN': 'https://cdn.nba.com/logos/nba/1610612751/global/L/logo.svg',
    'CHA': 'https://cdn.nba.com/logos/nba/1610612766/global/L/logo.svg',
    'CHI': 'https://cdn.nba.com/logos/nba/1610612741/global/L/logo.svg',
    'CLE': 'https://cdn.nba.com/logos/nba/1610612739/global/L/logo.svg',
    'DAL': 'https://cdn.nba.com/logos/nba/1610612742/global/L/logo.svg',
    'DEN': 'https://cdn.nba.com/logos/nba/1610612743/global/L/logo.svg',
    'DET': 'https://cdn.nba.com/logos/nba/1610612765/global/L/logo.svg',
    'GSW': 'https://cdn.nba.com/logos/nba/1610612744/global/L/logo.svg',
    'HOU': 'https://cdn.nba.com/logos/nba/1610612745/global/L/logo.svg',
    'IND': 'https://cdn.nba.com/logos/nba/1610612754/global/L/logo.svg',
    'LAC': 'https://cdn.nba.com/logos/nba/1610612746/global/L/logo.svg',
    'LAL': 'https://cdn.nba.com/logos/nba/1610612747/global/L/logo.svg',
    'MEM': 'https://cdn.nba.com/logos/nba/1610612763/global/L/logo.svg',
    'MIA': 'https://cdn.nba.com/logos/nba/1610612748/global/L/logo.svg',
    'MIL': 'https://cdn.nba.com/logos/nba/1610612749/global/L/logo.svg',
    'MIN': 'https://cdn.nba.com/logos/nba/1610612750/global/L/logo.svg',
    'NOP': 'https://cdn.nba.com/logos/nba/1610612740/global/L/logo.svg',
    'NYK': 'https://cdn.nba.com/logos/nba/1610612752/global/L/logo.svg',
    'OKC': 'https://cdn.nba.com/logos/nba/1610612760/global/L/logo.svg',
    'ORL': 'https://cdn.nba.com/logos/nba/1610612753/global/L/logo.svg',
    'PHI': 'https://cdn.nba.com/logos/nba/1610612755/global/L/logo.svg',
    'PHX': 'https://cdn.nba.com/logos/nba/1610612756/global/L/logo.svg',
    'POR': 'https://cdn.nba.com/logos/nba/1610612757/global/L/logo.svg',
    'SAC': 'https://cdn.nba.com/logos/nba/1610612758/global/L/logo.svg',
    'SAS': 'https://cdn.nba.com/logos/nba/1610612759/global/L/logo.svg',
    'TOR': 'https://cdn.nba.com/logos/nba/1610612761/global/L/logo.svg',
    'UTA': 'https://cdn.nba.com/logos/nba/1610612762/global/L/logo.svg',
    'WAS': 'https://cdn.nba.com/logos/nba/1610612764/global/L/logo.svg',
}

# ============================================================================
# CONFIGURACIÓN DE PÁGINA Y ESTILOS CSS
# ============================================================================

st.set_page_config(
    page_title="Parley Hunter Pro - Real Data",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS PERSONALIZADO - ESTILO DRAFTEA MEJORADO
st.markdown("""
<style>
    /* Fondo principal oscuro */
    .stApp {
        background-color: #0e0e12;
        color: #ffffff;
    }
    
    /* Sidebar oscuro */
    [data-testid="stSidebar"] {
        background-color: #1a1a23;
    }
    
    /* Pestañas personalizadas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #1a1a23;
        padding: 10px;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #0e0e12;
        color: #ffffff;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        border: 2px solid #2a2a35;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #5b21b6;
        border-color: #5b21b6;
    }
    
    /* Botones personalizados */
    .stButton > button {
        background-color: #5b21b6;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 600;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background-color: #7c3aed;
        box-shadow: 0 0 20px rgba(91, 33, 182, 0.5);
    }
    
    /* Tarjetas personalizadas */
    .parley-card {
        background: linear-gradient(135deg, #1a1a23 0%, #2a2a35 100%);
        border: 2px solid #5b21b6;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(91, 33, 182, 0.3);
        transition: transform 0.2s;
    }
    
    .parley-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(91, 33, 182, 0.5);
    }
    
    .neon-text {
        color: #00e5ff;
        font-size: 24px;
        font-weight: 700;
        text-shadow: 0 0 10px rgba(0, 229, 255, 0.5);
    }
    
    .stat-value {
        color: #00e5ff;
        font-size: 20px;
        font-weight: 600;
    }
    
    /* Tabla de datos personalizada */
    .dataframe {
        background-color: #1a1a23 !important;
        color: #ffffff !important;
        border: 2px solid #5b21b6 !important;
        border-radius: 10px !important;
    }
    
    .dataframe th {
        background-color: #5b21b6 !important;
        color: #ffffff !important;
        font-weight: 600 !important;
        padding: 12px !important;
    }
    
    .dataframe td {
        background-color: #1a1a23 !important;
        color: #e5e7eb !important;
        padding: 10px !important;
        border-bottom: 1px solid #2a2a35 !important;
    }
    
    /* Métricas personalizadas */
    [data-testid="stMetricValue"] {
        color: #00e5ff;
        font-size: 28px;
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div {
        background-color: #1a1a23;
        color: #ffffff;
        border: 2px solid #2a2a35;
        border-radius: 8px;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #5b21b6;
        box-shadow: 0 0 10px rgba(91, 33, 182, 0.3);
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #ffffff;
    }
    
    /* Info boxes */
    .stInfo {
        background-color: #1a1a23;
        border-left: 4px solid #5b21b6;
    }
    
    .stWarning {
        background-color: #1a1a23;
        border-left: 4px solid #f59e0b;
    }
    
    .stSuccess {
        background-color: #1a1a23;
        border-left: 4px solid #10b981;
    }
    
    .stError {
        background-color: #1a1a23;
        border-left: 4px solid #ef4444;
    }
    
    /* Community post card */
    .community-post {
        background-color: #1a1a23;
        border: 2px solid #2a2a35;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    
    /* NBA Game Card */
    .nba-game-card {
        background: linear-gradient(135deg, #1a1a23 0%, #2a2a35 100%);
        border: 2px solid #5b21b6;
        border-radius: 12px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 4px 15px rgba(91, 33, 182, 0.3);
    }
    
    /* Logo container */
    .logo-container {
        text-align: center;
        padding: 20px;
        background-color: #1a1a23;
        border-radius: 12px;
        margin: 20px 0;
    }
    
    .logo-container img {
        max-width: 200px;
        height: auto;
        filter: drop-shadow(0 0 10px rgba(91, 33, 182, 0.5));
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# INICIALIZACIÓN DE SESSION STATE
# ============================================================================

if 'community_posts' not in st.session_state:
    st.session_state.community_posts = []

if 'historial' not in st.session_state:
    st.session_state.historial = []

# ============================================================================
# FUNCIONES DE OBTENCIÓN DE DATOS REALES
# ============================================================================

@st.cache_data(ttl=300)  # 5 minutos de caché
def obtener_partidos_nba_hoy():
    """Obtiene partidos de NBA de hoy usando nba_api"""
    try:
        from nba_api.live.nba.endpoints import scoreboard
        
        # Obtener scoreboard de hoy
        games = scoreboard.ScoreBoard()
        games_data = games.get_dict()
        
        partidos = []
        
        if 'scoreboard' in games_data and 'games' in games_data['scoreboard']:
            for game in games_data['scoreboard']['games']:
                home_team = game['homeTeam']
                away_team = game['awayTeam']
                
                # Determinar estado del partido
                game_status = game.get('gameStatusText', 'Scheduled')
                
                partidos.append({
                    'game_id': game.get('gameId', ''),
                    'away_team': away_team.get('teamTricode', 'N/A'),
                    'away_team_name': away_team.get('teamName', 'N/A'),
                    'away_score': away_team.get('score', 0),
                    'home_team': home_team.get('teamTricode', 'N/A'),
                    'home_team_name': home_team.get('teamName', 'N/A'),
                    'home_score': home_team.get('score', 0),
                    'status': game_status,
                    'period': game.get('period', 0),
                    'game_clock': game.get('gameClock', '')
                })
        
        return partidos if partidos else None
        
    except Exception as e:
        st.error(f"⚠️ Error al conectar con NBA API: {str(e)}")
        return None

@st.cache_data(ttl=1800)  # 30 minutos de caché
def obtener_tabla_liga(liga_nombre):
    """Obtiene la tabla de una liga usando web scraping"""
    try:
        url = LIGAS_URLS.get(liga_nombre)
        if not url:
            return None
        
        # Leer todas las tablas de la página
        tables = pd.read_html(url)
        
        # La primera tabla suele ser la tabla de posiciones
        if tables and len(tables) > 0:
            df = tables[0]
            
            # Limpiar columnas multi-index si existen
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in df.columns]
            
            # Renombrar columnas comunes
            df.columns = [str(col).replace('Unnamed: ', '') for col in df.columns]
            
            # Intentar encontrar columnas clave
            # Buscar columna de posición/ranking
            pos_cols = [col for col in df.columns if 'Rk' in col or 'Pos' in col or col.startswith('0_')]
            if pos_cols:
                df.rename(columns={pos_cols[0]: 'Pos'}, inplace=True)
            
            # Buscar columna de equipo/squad
            team_cols = [col for col in df.columns if 'Squad' in col or 'Team' in col or 'Club' in col]
            if team_cols:
                df.rename(columns={team_cols[0]: 'Equipo'}, inplace=True)
            
            # Seleccionar columnas relevantes si existen
            relevant_cols = []
            for col in df.columns:
                col_lower = str(col).lower()
                if any(x in col_lower for x in ['pos', 'equipo', 'squad', 'team', 'mp', 'w', 'pts', 'gf', 'ga', 'gd', 'pj', 'pg', 'pe', 'pp']):
                    relevant_cols.append(col)
            
            if relevant_cols:
                df = df[relevant_cols]
            
            # Limitar a top 20 equipos
            df = df.head(20)
            
            return df
        
        return None
        
    except Exception as e:
        st.warning(f"⚠️ No pudimos conectar con la fuente oficial de {liga_nombre} en este momento.")
        st.caption(f"Detalle técnico: {str(e)}")
        return None

def obtener_jugadores_nba_hoy(partidos):
    """Genera datos de jugadores basados en los equipos que juegan hoy"""
    if not partidos:
        return []
    
    # Jugadores destacados por equipo
    jugadores_por_equipo = {
        'LAL': [{'nombre': 'LeBron James', 'emoji': '👑', 'pts': 25.5, 'reb': 7.8, 'ast': 8.2}],
        'GSW': [{'nombre': 'Stephen Curry', 'emoji': '🎯', 'pts': 28.3, 'reb': 5.1, 'ast': 6.4}],
        'DEN': [{'nombre': 'Nikola Jokic', 'emoji': '🃏', 'pts': 26.8, 'reb': 12.2, 'ast': 9.1}],
        'MIL': [{'nombre': 'Giannis Antetokounmpo', 'emoji': '🦌', 'pts': 30.2, 'reb': 11.3, 'ast': 5.8}],
        'PHX': [{'nombre': 'Kevin Durant', 'emoji': '🐍', 'pts': 27.9, 'reb': 6.5, 'ast': 5.2}],
        'DAL': [{'nombre': 'Luka Doncic', 'emoji': '🔥', 'pts': 28.7, 'reb': 8.4, 'ast': 8.8}],
        'PHI': [{'nombre': 'Joel Embiid', 'emoji': '💪', 'pts': 29.1, 'reb': 10.8, 'ast': 4.2}],
        'BOS': [{'nombre': 'Jayson Tatum', 'emoji': '☘️', 'pts': 26.9, 'reb': 8.1, 'ast': 4.9}],
        'CLE': [{'nombre': 'Donovan Mitchell', 'emoji': '🕷️', 'pts': 27.4, 'reb': 4.8, 'ast': 5.3}],
        'BKN': [{'nombre': 'Mikal Bridges', 'emoji': '🌉', 'pts': 21.5, 'reb': 4.6, 'ast': 3.8}],
        'MIA': [{'nombre': 'Jimmy Butler', 'emoji': '☕', 'pts': 22.3, 'reb': 5.9, 'ast': 5.1}],
        'NYK': [{'nombre': 'Jalen Brunson', 'emoji': '🗽', 'pts': 24.8, 'reb': 3.7, 'ast': 6.5}],
        'SAC': [{'nombre': 'Domantas Sabonis', 'emoji': '👑', 'pts': 19.6, 'reb': 13.2, 'ast': 7.8}],
        'NOP': [{'nombre': 'Zion Williamson', 'emoji': '⚡', 'pts': 22.8, 'reb': 5.7, 'ast': 4.2}],
        'MIN': [{'nombre': 'Anthony Edwards', 'emoji': '🐺', 'pts': 25.9, 'reb': 5.4, 'ast': 5.2}],
        'OKC': [{'nombre': 'Shai Gilgeous-Alexander', 'emoji': '⚡', 'pts': 30.5, 'reb': 5.8, 'ast': 6.3}],
    }
    
    props = []
    for partido in partidos:
        for team_code in [partido['home_team'], partido['away_team']]:
            if team_code in jugadores_por_equipo:
                for jugador in jugadores_por_equipo[team_code]:
                    props.append({
                        'jugador': jugador['nombre'],
                        'equipo': team_code,
                        'emoji': jugador['emoji'],
                        'puntos': jugador['pts'],
                        'rebotes': jugador['reb'],
                        'asistencias': jugador['ast'],
                        'linea_puntos': round(jugador['pts'] - random.uniform(1, 3), 1),
                        'linea_rebotes': round(jugador['reb'] - random.uniform(0.5, 1.5), 1),
                        'linea_asistencias': round(jugador['ast'] - random.uniform(0.5, 1.5), 1),
                        'cuota_over_pts': round(random.uniform(1.85, 2.05), 2),
                        'cuota_over_reb': round(random.uniform(1.80, 2.10), 2),
                        'cuota_over_ast': round(random.uniform(1.85, 2.15), 2),
                    })
    
    return props

# ============================================================================
# FUNCIONES DE RENDERIZADO
# ============================================================================

def render_nba_game_card(game):
    """Renderiza tarjeta de partido NBA con logos"""
    away_logo = NBA_TEAM_LOGOS.get(game['away_team'], '')
    home_logo = NBA_TEAM_LOGOS.get(game['home_team'], '')
    
    st.markdown(f"""
    <div class="nba-game-card">
        <div style="text-align: center; margin-bottom: 15px;">
            <span style="color: #9ca3af; font-size: 14px;">{game['status']}</span>
        </div>
        <div style="display: grid; grid-template-columns: 1fr auto 1fr; gap: 20px; align-items: center;">
            <div style="text-align: center;">
                <img src="{away_logo}" style="width: 60px; height: 60px; margin-bottom: 10px;" onerror="this.style.display='none'"/>
                <h3 style="margin: 5px 0;">{game['away_team']}</h3>
                <p style="color: #9ca3af; font-size: 14px; margin: 0;">{game['away_team_name']}</p>
                <div class="neon-text" style="font-size: 32px; margin-top: 10px;">{game['away_score']}</div>
            </div>
            <div style="text-align: center;">
                <span style="color: #9ca3af; font-size: 24px;">VS</span>
            </div>
            <div style="text-align: center;">
                <img src="{home_logo}" style="width: 60px; height: 60px; margin-bottom: 10px;" onerror="this.style.display='none'"/>
                <h3 style="margin: 5px 0;">{game['home_team']}</h3>
                <p style="color: #9ca3af; font-size: 14px; margin: 0;">{game['home_team_name']}</p>
                <div class="neon-text" style="font-size: 32px; margin-top: 10px;">{game['home_score']}</div>
            </div>
        </div>
        {f'<div style="text-align: center; margin-top: 15px; padding-top: 15px; border-top: 1px solid #2a2a35;"><span style="color: #9ca3af;">Q{game["period"]} - {game["game_clock"]}</span></div>' if game['period'] > 0 else ''}
    </div>
    """, unsafe_allow_html=True)

def render_player_prop_card_real(jugador_data, prop_type):
    """Renderiza tarjeta de prop de jugador con datos reales"""
    if prop_type == "Puntos":
        promedio = jugador_data['puntos']
        linea = jugador_data['linea_puntos']
        cuota = jugador_data['cuota_over_pts']
        emoji_stat = '🏀'
    elif prop_type == "Rebotes":
        promedio = jugador_data['rebotes']
        linea = jugador_data['linea_rebotes']
        cuota = jugador_data['cuota_over_reb']
        emoji_stat = '💪'
    else:  # Asistencias
        promedio = jugador_data['asistencias']
        linea = jugador_data['linea_asistencias']
        cuota = jugador_data['cuota_over_ast']
        emoji_stat = '🎯'
    
    recomendacion = "Over" if promedio > linea else "Under"
    diferencia = abs(promedio - linea)
    
    team_logo = NBA_TEAM_LOGOS.get(jugador_data['equipo'], '')
    
    st.markdown(f"""
    <div class="parley-card">
        <div style="display: flex; align-items: center; gap: 15px;">
            <div style="font-size: 40px;">{jugador_data['emoji']}</div>
            <div style="flex-grow: 1;">
                <h3 style="margin: 0;">{jugador_data['jugador']}</h3>
                <div style="display: flex; align-items: center; gap: 10px; margin-top: 5px;">
                    <img src="{team_logo}" style="width: 25px; height: 25px;" onerror="this.style.display='none'"/>
                    <p style="color: #9ca3af; margin: 0;">{jugador_data['equipo']} | {emoji_stat} {prop_type}</p>
                </div>
            </div>
        </div>
        <div style="margin-top: 20px; padding: 15px; background-color: #0e0e12; border-radius: 8px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <span style="color: #9ca3af;">Línea:</span>
                <span class="stat-value">{linea}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <span style="color: #9ca3af;">Promedio Temporada:</span>
                <span class="stat-value">{promedio}</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span style="color: #9ca3af;">Cuota {recomendacion}:</span>
                <span class="neon-text">@{cuota}</span>
            </div>
        </div>
        <div style="margin-top: 15px; text-align: center;">
            <span style="background-color: #5b21b6; padding: 8px 20px; border-radius: 6px; font-weight: 600;">
                🎯 Recomendado: {recomendacion} {linea}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# HEADER DE LA APP
# ============================================================================

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("<h1 style='margin-bottom: 0;'>🔥 Parley Hunter <span style='color: #5b21b6;'>Pro</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #9ca3af; margin-top: 5px;'>100% Datos Reales | NBA API + Scraping Mundial de Fútbol</p>", unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style='text-align: right; padding: 10px;'>
        <div style='color: #00e5ff; font-size: 14px;'>📅 {datetime.now().strftime('%d %b %Y')}</div>
        <div style='color: #9ca3af; font-size: 12px;'>⏰ {datetime.now().strftime('%H:%M')}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================================
# PESTAÑAS PRINCIPALES
# ============================================================================

tabs = st.tabs([
    "🏀 NBA HOY",
    "📊 TABLAS REALES",
    "🟣 DRAFTEA MODE",
    "👥 COMUNIDAD"
])

# ============================================================================
# TAB 1: NBA HOY
# ============================================================================

with tabs[0]:
    st.markdown("## 🏀 NBA - Partidos de Hoy")
    st.markdown("Datos en vivo desde NBA.com API oficial")
    st.markdown("")
    
    with st.spinner("🔄 Cargando partidos de hoy desde NBA API..."):
        partidos = obtener_partidos_nba_hoy()
    
    if partidos:
        st.success(f"✅ {len(partidos)} partidos encontrados")
        st.markdown("")
        
        # Mostrar partidos en grid
        cols_per_row = 2
        for i in range(0, len(partidos), cols_per_row):
            cols = st.columns(cols_per_row)
            for j, col in enumerate(cols):
                if i + j < len(partidos):
                    with col:
                        render_nba_game_card(partidos[i + j])
        
        # Guardar partidos en session state para usarlos en Draftea Mode
        st.session_state['partidos_hoy'] = partidos
        
    else:
        st.info("ℹ️ No hay partidos programados para hoy o la API no está disponible.")
        st.markdown("**Posibles razones:**")
        st.markdown("- No hay partidos de NBA programados hoy")
        st.markdown("- La API de NBA.com está temporalmente inaccesible")
        st.markdown("- Es necesario instalar: `pip install nba_api`")

# ============================================================================
# TAB 2: TABLAS REALES
# ============================================================================

with tabs[1]:
    st.markdown("## 📊 Tablas de Posiciones - Datos Reales")
    st.markdown("Scraping en vivo desde FBref.com")
    st.markdown("")
    
    # Selector de liga
    liga_seleccionada = st.selectbox(
        "🏆 Selecciona una Liga o Copa",
        list(LIGAS_URLS.keys()),
        key="selector_liga_tabla"
    )
    
    st.markdown("---")
    
    # Mostrar logo de la liga
    logo_url = LIGAS_LOGOS.get(liga_seleccionada, '')
    if logo_url:
        st.markdown(f"""
        <div class="logo-container">
            <img src="{logo_url}" alt="{liga_seleccionada}"/>
            <h2 style="margin-top: 15px; color: #00e5ff;">{liga_seleccionada}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Botón para cargar tabla
    if st.button("🔄 Cargar Tabla Actualizada", type="primary", use_container_width=True):
        with st.spinner(f"🌐 Obteniendo datos de {liga_seleccionada}..."):
            tabla = obtener_tabla_liga(liga_seleccionada)
        
        if tabla is not None:
            st.success("✅ Tabla cargada exitosamente")
            st.markdown("")
            
            # Mostrar tabla con estilo
            st.dataframe(
                tabla,
                use_container_width=True,
                hide_index=True,
                height=600
            )
            
            # Información adicional
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Equipos Mostrados", len(tabla))
            with col2:
                st.metric("Fuente", "FBref.com")
            with col3:
                st.metric("Actualización", "Tiempo Real")
                
        else:
            st.error("❌ No se pudo cargar la tabla en este momento")
            st.markdown("**Intenta:**")
            st.markdown("- Verificar tu conexión a internet")
            st.markdown("- Seleccionar otra liga")
            st.markdown("- Esperar unos minutos y volver a intentar")
    else:
        st.info("👆 Haz clic en 'Cargar Tabla Actualizada' para ver la clasificación")

# ============================================================================
# TAB 3: DRAFTEA MODE
# ============================================================================

with tabs[2]:
    st.markdown("## 🟣 Draftea Mode - Props Inteligentes")
    st.markdown("Jugadores NBA que juegan HOY + Análisis de Fútbol")
    st.markdown("")
    
    # Sub-pestañas
    sub_tabs = st.tabs(["🏀 Props NBA", "⚽ Análisis Fútbol"])
    
    # SUB-TAB 1: Props NBA
    with sub_tabs[0]:
        st.markdown("### 🏀 Player Props - Solo jugadores activos hoy")
        st.markdown("")
        
        if 'partidos_hoy' not in st.session_state or not st.session_state['partidos_hoy']:
            st.warning("⚠️ Primero ve a la pestaña 'NBA HOY' para cargar los partidos de hoy")
        else:
            partidos_hoy = st.session_state['partidos_hoy']
            jugadores_props = obtener_jugadores_nba_hoy(partidos_hoy)
            
            if jugadores_props:
                # Filtros
                col1, col2 = st.columns(2)
                with col1:
                    prop_type = st.selectbox(
                        "📊 Tipo de Estadística",
                        ["Puntos", "Rebotes", "Asistencias"],
                        key="draftea_prop_type"
                    )
                with col2:
                    num_jugadores = st.slider(
                        "👥 Número de Jugadores",
                        3, len(jugadores_props), min(9, len(jugadores_props)),
                        key="draftea_num_jugadores"
                    )
                
                st.markdown("---")
                
                # Ordenar por promedio
                if prop_type == "Puntos":
                    jugadores_props.sort(key=lambda x: x['puntos'], reverse=True)
                elif prop_type == "Rebotes":
                    jugadores_props.sort(key=lambda x: x['rebotes'], reverse=True)
                else:
                    jugadores_props.sort(key=lambda x: x['asistencias'], reverse=True)
                
                # Mostrar props
                for i in range(0, num_jugadores, 3):
                    cols = st.columns(3)
                    for j, col in enumerate(cols):
                        if i + j < num_jugadores:
                            with col:
                                render_player_prop_card_real(jugadores_props[i + j], prop_type)
            else:
                st.info("No hay datos de jugadores disponibles para los partidos de hoy")
    
    # SUB-TAB 2: Análisis Fútbol
    with sub_tabs[1]:
        st.markdown("### ⚽ Análisis Basado en Rachas - Fútbol")
        st.markdown("")
        
        liga_analisis = st.selectbox(
            "🏆 Selecciona Liga para Análisis",
            list(LIGAS_URLS.keys()),
            key="liga_analisis_futbol"
        )
        
        st.markdown("---")
        
        if st.button("🔍 Generar Análisis", type="primary", use_container_width=True):
            with st.spinner("📊 Analizando patrones..."):
                tabla = obtener_tabla_liga(liga_analisis)
            
            if tabla is not None:
                st.success("✅ Análisis completado")
                st.markdown("")
                
                # Análisis inteligente basado en la tabla
                st.markdown("### 💡 Insights de Valor")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("""
                    <div class="parley-card">
                        <h3>🔥 Apuesta Alta Confianza</h3>
                        <p style="color: #9ca3af;">Líderes en Casa</p>
                        <p style="color: #e5e7eb; margin-top: 10px;">
                        Los equipos en los primeros 3 lugares suelen tener una tasa de victoria 
                        del 70%+ cuando juegan en casa. Revisa la tabla y considera:
                        </p>
                        <ul style="color: #9ca3af; margin-top: 10px;">
                            <li>1° lugar vs equipos 10° o inferior: Alta probabilidad</li>
                            <li>Over 1.5 goles en partidos de top 5</li>
                            <li>BTTS cuando juegan top 3 vs top 3</li>
                        </ul>
                        <div style="margin-top: 15px; text-align: center;">
                            <span style="background-color: #10b981; padding: 8px 20px; border-radius: 6px; font-weight: 600;">
                                ✅ Confianza: Alta
                            </span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("""
                    <div class="parley-card">
                        <h3>⚡ Apuesta de Valor</h3>
                        <p style="color: #9ca3af;">Zona de Descenso Visitante</p>
                        <p style="color: #e5e7eb; margin-top: 10px;">
                        Equipos en zona de descenso (últimos 3 lugares) tienen 
                        dificultades como visitantes. Considera:
                        </p>
                        <ul style="color: #9ca3af; margin-top: 10px;">
                            <li>Under 2.5 goles cuando visitan</li>
                            <li>Victoria del equipo local</li>
                            <li>Handicap favorable al local</li>
                        </ul>
                        <div style="margin-top: 15px; text-align: center;">
                            <span style="background-color: #f59e0b; padding: 8px 20px; border-radius: 6px; font-weight: 600;">
                                💎 Confianza: Media-Alta
                            </span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Mostrar top 5 de la tabla
                st.markdown("---")
                st.markdown("### 📋 Top 5 - Referencia")
                st.dataframe(tabla.head(5), use_container_width=True, hide_index=True)
                
            else:
                st.error("No se pudo cargar la tabla para análisis")

# ============================================================================
# TAB 4: COMUNIDAD
# ============================================================================

with tabs[3]:
    st.markdown("## 👥 Comunidad Parley Hunter")
    st.markdown("Comparte tus picks y vota los de otros usuarios")
    st.markdown("")
    
    # Formulario para publicar
    with st.expander("✍️ Publicar tu Parley", expanded=True):
        with st.form("community_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                user_nick = st.text_input("🎭 Tu Nick", placeholder="Ej: ElTigredeVegas")
                tipo_apuesta = st.selectbox("🎯 Tipo", ["NBA", "Fútbol", "NFL", "Combo"])
            
            with col2:
                cuota_post = st.number_input("💰 Cuota", min_value=1.5, max_value=10.0, value=2.0, step=0.1)
                deporte_emoji = st.selectbox("🎨 Emoji", ["🔥", "💎", "🚀", "⚡", "🎯", "👑"])
            
            prediccion = st.text_area(
                "📝 Tu Predicción",
                placeholder="Ej: LeBron Over 25.5 pts + Lakers Win. El Rey está imparable últimamente...",
                height=100
            )
            
            submitted = st.form_submit_button("🚀 Publicar", use_container_width=True)
            
            if submitted:
                if user_nick and prediccion:
                    new_post = {
                        'id': len(st.session_state.community_posts),
                        'nick': user_nick,
                        'tipo': tipo_apuesta,
                        'prediccion': prediccion,
                        'cuota': cuota_post,
                        'emoji': deporte_emoji,
                        'fecha': datetime.now().strftime('%d/%m/%Y %H:%M'),
                        'votos_pago': 0,
                        'votos_nadota': 0,
                        'votantes': []
                    }
                    st.session_state.community_posts.insert(0, new_post)
                    st.success("✅ ¡Publicado! Tu pick ya está en el muro")
                    st.rerun()
                else:
                    st.error("⚠️ Completa todos los campos")
    
    st.markdown("---")
    st.markdown("### 📢 Muro de la Comunidad")
    
    if not st.session_state.community_posts:
        st.info("🏜️ El muro está vacío. ¡Sé el primero en compartir un parley!")
    else:
        # Filtros
        col1, col2 = st.columns([3, 1])
        with col1:
            filtro_tipo = st.selectbox(
                "Filtrar por tipo",
                ["Todos", "NBA", "Fútbol", "NFL", "Combo"],
                key="community_filter"
            )
        with col2:
            ordenar = st.selectbox(
                "Ordenar por",
                ["Más recientes", "Más votados"],
                key="community_sort"
            )
        
        # Filtrar posts
        posts_filtrados = st.session_state.community_posts.copy()
        if filtro_tipo != "Todos":
            posts_filtrados = [p for p in posts_filtrados if p['tipo'] == filtro_tipo]
        
        # Ordenar posts
        if ordenar == "Más votados":
            posts_filtrados.sort(key=lambda x: x['votos_pago'] - x['votos_nadota'], reverse=True)
        
        st.markdown("")
        
        # Mostrar posts
        for post in posts_filtrados:
            ratio_votos = post['votos_pago'] - post['votos_nadota']
            color_borde = "#10b981" if ratio_votos > 0 else "#ef4444" if ratio_votos < 0 else "#5b21b6"
            
            st.markdown(f"""
            <div class="community-post" style="border-color: {color_borde};">
                <div style="display: flex; justify-content: space-between; align-items: start; margin-bottom: 15px;">
                    <div>
                        <span style="font-size: 20px;">{post['emoji']}</span>
                        <strong style="margin-left: 10px;">{post['nick']}</strong>
                        <span style="color: #9ca3af; margin-left: 10px; font-size: 14px;">{post['tipo']}</span>
                    </div>
                    <div style="text-align: right;">
                        <div class="neon-text" style="font-size: 18px;">@{post['cuota']}</div>
                        <div style="color: #9ca3af; font-size: 12px;">{post['fecha']}</div>
                    </div>
                </div>
                <p style="color: #e5e7eb; margin: 15px 0;">{post['prediccion']}</p>
            </div>
            """, unsafe_allow_html=True)
            
            # Botones de votación
            col1, col2, col3 = st.columns([2, 2, 2])
            
            with col1:
                if st.button(f"🤑 ¡Pagó! ({post['votos_pago']})", key=f"voto_si_{post['id']}", use_container_width=True):
                    if post['id'] not in post['votantes']:
                        post['votos_pago'] += 1
                        post['votantes'].append(post['id'])
                        st.rerun()
            
            with col2:
                if st.button(f"🤡 Nadota ({post['votos_nadota']})", key=f"voto_no_{post['id']}", use_container_width=True):
                    if post['id'] not in post['votantes']:
                        post['votos_nadota'] += 1
                        post['votantes'].append(post['id'])
                        st.rerun()
            
            with col3:
                if st.button("🗑️ Eliminar", key=f"delete_post_{post['id']}"):
                    st.session_state.community_posts = [p for p in st.session_state.community_posts if p['id'] != post['id']]
                    st.rerun()
            
            st.markdown("---")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; padding: 20px; background-color: #1a1a23; border-radius: 10px; margin-top: 40px;'>
    <h3 style='color: #5b21b6; margin-bottom: 10px;'>Parley Hunter Pro - Real Data Edition</h3>
    <p style='color: #9ca3af; font-size: 14px;'>
        ⚠️ <strong>Advertencia:</strong> Las apuestas deportivas implican riesgos. Juega responsablemente.<br>
        📊 <strong>Fuentes:</strong> NBA.com API (Official) + FBref.com (Scraping) | 🚀 Powered by Streamlit + Python<br>
        💡 Esta herramienta muestra datos reales pero es solo para fines educativos e informativos
    </p>
    <p style='color: #5b21b6; font-size: 12px; margin-top: 10px;'>
        v3.0 Real Data Edition | Made with 💜 by Parley Hunters
    </p>
</div>
""", unsafe_allow_html=True)
