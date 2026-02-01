import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# ============================================================================
# CONFIGURACIÓN DE PÁGINA Y ESTILOS CSS
# ============================================================================

st.set_page_config(
    page_title="Parley Hunter Pro",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS PERSONALIZADO - ESTILO DRAFTEA
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
    
    .confidence-high {
        color: #10b981;
        font-weight: 600;
    }
    
    .confidence-medium {
        color: #f59e0b;
        font-weight: 600;
    }
    
    .confidence-low {
        color: #ef4444;
        font-weight: 600;
    }
    
    /* Métricas personalizadas */
    [data-testid="stMetricValue"] {
        color: #00e5ff;
        font-size: 28px;
    }
    
    /* Input fields */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
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
    
    /* Selectbox */
    .stSelectbox > div > div {
        background-color: #1a1a23;
        border: 2px solid #2a2a35;
        border-radius: 8px;
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
    
    /* Community post card */
    .community-post {
        background-color: #1a1a23;
        border: 2px solid #2a2a35;
        border-radius: 10px;
        padding: 15px;
        margin: 10px 0;
    }
    
    .vote-button {
        display: inline-block;
        padding: 8px 16px;
        margin: 5px;
        border-radius: 6px;
        font-weight: 600;
        cursor: pointer;
    }
    
    .vote-up {
        background-color: #10b981;
        color: white;
    }
    
    .vote-down {
        background-color: #ef4444;
        color: white;
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
# FUNCIONES DE GENERACIÓN DE DATOS MOCK
# ============================================================================

@st.cache_data(ttl=3600)
def generar_datos_nba():
    """Genera datos simulados de NBA"""
    jugadores = [
        {'nombre': 'LeBron James', 'equipo': 'LAL', 'posicion': 'SF', 'emoji': '👑'},
        {'nombre': 'Stephen Curry', 'equipo': 'GSW', 'posicion': 'PG', 'emoji': '🎯'},
        {'nombre': 'Nikola Jokic', 'equipo': 'DEN', 'posicion': 'C', 'emoji': '🃏'},
        {'nombre': 'Giannis Antetokounmpo', 'equipo': 'MIL', 'posicion': 'PF', 'emoji': '🦌'},
        {'nombre': 'Kevin Durant', 'equipo': 'PHX', 'posicion': 'SF', 'emoji': '🐍'},
        {'nombre': 'Luka Doncic', 'equipo': 'DAL', 'posicion': 'PG', 'emoji': '🔥'},
        {'nombre': 'Joel Embiid', 'equipo': 'PHI', 'posicion': 'C', 'emoji': '💪'},
        {'nombre': 'Jayson Tatum', 'equipo': 'BOS', 'posicion': 'SF', 'emoji': '☘️'},
        {'nombre': 'Damian Lillard', 'equipo': 'MIL', 'posicion': 'PG', 'emoji': '⏰'},
        {'nombre': 'Anthony Davis', 'equipo': 'LAL', 'posicion': 'PF', 'emoji': '🦍'}
    ]
    
    props = []
    for jugador in jugadores:
        props.append({
            'jugador': jugador['nombre'],
            'equipo': jugador['equipo'],
            'emoji': jugador['emoji'],
            'puntos': round(random.uniform(22, 35), 1),
            'rebotes': round(random.uniform(6, 14), 1),
            'asistencias': round(random.uniform(4, 11), 1),
            'triples': round(random.uniform(2, 5), 1),
            'linea_puntos': random.randint(24, 32),
            'linea_rebotes': random.randint(7, 12),
            'linea_asistencias': random.randint(5, 9),
            'linea_triples': random.randint(2, 4),
            'cuota_puntos': round(random.uniform(1.75, 2.10), 2),
            'cuota_rebotes': round(random.uniform(1.80, 2.05), 2),
            'cuota_asistencias': round(random.uniform(1.85, 2.15), 2)
        })
    
    return props

@st.cache_data(ttl=3600)
def generar_datos_futbol():
    """Genera datos simulados de Fútbol"""
    partidos = [
        {'local': 'Real Madrid', 'visitante': 'Barcelona', 'liga': 'La Liga', 'emoji': '⚔️'},
        {'local': 'Manchester City', 'visitante': 'Liverpool', 'liga': 'Premier League', 'emoji': '🔥'},
        {'local': 'Bayern Munich', 'visitante': 'Dortmund', 'liga': 'Bundesliga', 'emoji': '🇩🇪'},
        {'local': 'PSG', 'visitante': 'Marseille', 'liga': 'Ligue 1', 'emoji': '🇫🇷'},
        {'local': 'Inter Milan', 'visitante': 'AC Milan', 'liga': 'Serie A', 'emoji': '🇮🇹'},
        {'local': 'Atlético Madrid', 'visitante': 'Sevilla', 'liga': 'La Liga', 'emoji': '⚽'},
        {'local': 'Arsenal', 'visitante': 'Chelsea', 'liga': 'Premier League', 'emoji': '🏴󠁧󠁢󠁥󠁮󠁧󠁿'},
        {'local': 'Juventus', 'visitante': 'Roma', 'liga': 'Serie A', 'emoji': '🇮🇹'}
    ]
    
    predicciones = []
    for partido in partidos:
        predicciones.append({
            'local': partido['local'],
            'visitante': partido['visitante'],
            'liga': partido['liga'],
            'emoji': partido['emoji'],
            'cuota_local': round(random.uniform(1.50, 2.80), 2),
            'cuota_empate': round(random.uniform(3.00, 3.80), 2),
            'cuota_visitante': round(random.uniform(1.60, 3.20), 2),
            'cuota_btts': round(random.uniform(1.65, 2.10), 2),
            'cuota_over25': round(random.uniform(1.70, 2.20), 2),
            'goles_esperados': round(random.uniform(2.1, 3.5), 1),
            'prob_local': random.randint(35, 60),
            'prob_btts': random.randint(55, 75)
        })
    
    return predicciones

def generar_top_sugerencias():
    """Genera las top 3 sugerencias del día (mix NBA + Fútbol)"""
    sugerencias = []
    
    # Sugerencia NBA
    nba_data = generar_datos_nba()
    top_nba = random.choice(nba_data)
    sugerencias.append({
        'tipo': 'NBA',
        'titulo': f"{top_nba['emoji']} {top_nba['jugador']} - Over {top_nba['linea_puntos']} Puntos",
        'detalle': f"{top_nba['equipo']} | Promedio: {top_nba['puntos']} pts",
        'cuota': top_nba['cuota_puntos'],
        'confianza': 'Alta' if top_nba['puntos'] > top_nba['linea_puntos'] + 3 else 'Media',
        'razon': f"Promedia {top_nba['puntos']} puntos, línea en {top_nba['linea_puntos']}"
    })
    
    # Sugerencia Fútbol
    futbol_data = generar_datos_futbol()
    top_futbol = random.choice(futbol_data)
    sugerencias.append({
        'tipo': 'Fútbol',
        'titulo': f"{top_futbol['emoji']} {top_futbol['local']} vs {top_futbol['visitante']}",
        'detalle': f"Ambos Anotan (BTTS)",
        'cuota': top_futbol['cuota_btts'],
        'confianza': 'Alta' if top_futbol['prob_btts'] > 65 else 'Media',
        'razon': f"{top_futbol['prob_btts']}% probabilidad de que ambos equipos anoten"
    })
    
    # Sugerencia Mix
    otro_nba = random.choice([p for p in nba_data if p != top_nba])
    sugerencias.append({
        'tipo': 'NBA',
        'titulo': f"{otro_nba['emoji']} {otro_nba['jugador']} - Over {otro_nba['linea_asistencias']} Asistencias",
        'detalle': f"{otro_nba['equipo']} | Promedio: {otro_nba['asistencias']} ast",
        'cuota': otro_nba['cuota_asistencias'],
        'confianza': 'Media',
        'razon': f"Promedia {otro_nba['asistencias']} asistencias por partido"
    })
    
    return sugerencias

# ============================================================================
# FUNCIONES DE RENDERIZADO DE TARJETAS
# ============================================================================

def render_parley_card(titulo, detalle, cuota, confianza, razon):
    """Renderiza una tarjeta de parley con estilo Draftea"""
    confianza_class = {
        'Alta': 'confidence-high',
        'Media': 'confidence-medium',
        'Baja': 'confidence-low'
    }
    
    st.markdown(f"""
    <div class="parley-card">
        <h3 style="margin-top: 0;">{titulo}</h3>
        <p style="color: #9ca3af; font-size: 14px;">{detalle}</p>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 15px;">
            <div>
                <span class="neon-text">@{cuota}</span>
            </div>
            <div>
                <span class="{confianza_class[confianza]}">🎯 {confianza}</span>
            </div>
        </div>
        <p style="color: #6b7280; font-size: 13px; margin-top: 10px; border-top: 1px solid #2a2a35; padding-top: 10px;">
            💡 {razon}
        </p>
    </div>
    """, unsafe_allow_html=True)

def render_player_prop_card(jugador_data, prop_type):
    """Renderiza tarjeta de prop de jugador estilo Draftea"""
    if prop_type == "Puntos":
        promedio = jugador_data['puntos']
        linea = jugador_data['linea_puntos']
        cuota = jugador_data['cuota_puntos']
        emoji_stat = '🏀'
    elif prop_type == "Rebotes":
        promedio = jugador_data['rebotes']
        linea = jugador_data['linea_rebotes']
        cuota = jugador_data['cuota_rebotes']
        emoji_stat = '💪'
    else:  # Asistencias
        promedio = jugador_data['asistencias']
        linea = jugador_data['linea_asistencias']
        cuota = jugador_data['cuota_asistencias']
        emoji_stat = '🎯'
    
    recomendacion = "Over" if promedio > linea else "Under"
    diferencia = abs(promedio - linea)
    
    st.markdown(f"""
    <div class="parley-card">
        <div style="display: flex; align-items: center; gap: 15px;">
            <div style="font-size: 40px;">{jugador_data['emoji']}</div>
            <div>
                <h3 style="margin: 0;">{jugador_data['jugador']}</h3>
                <p style="color: #9ca3af; margin: 5px 0;">{jugador_data['equipo']} | {emoji_stat} {prop_type}</p>
            </div>
        </div>
        <div style="margin-top: 20px; padding: 15px; background-color: #0e0e12; border-radius: 8px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <span style="color: #9ca3af;">Línea:</span>
                <span class="stat-value">{linea}</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
                <span style="color: #9ca3af;">Promedio:</span>
                <span class="stat-value">{promedio}</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span style="color: #9ca3af;">Cuota {recomendacion}:</span>
                <span class="neon-text">@{cuota}</span>
            </div>
        </div>
        <div style="margin-top: 15px; text-align: center;">
            <span style="background-color: #5b21b6; padding: 8px 20px; border-radius: 6px; font-weight: 600;">
                🎯 {recomendacion} {linea} ({'+' if recomendacion == 'Over' else '-'}{diferencia:.1f})
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_futbol_card(partido_data):
    """Renderiza tarjeta de partido de fútbol"""
    mejor_cuota = min(partido_data['cuota_local'], partido_data['cuota_visitante'])
    if partido_data['cuota_local'] < partido_data['cuota_visitante']:
        favorito = partido_data['local']
        cuota_favorito = partido_data['cuota_local']
    else:
        favorito = partido_data['visitante']
        cuota_favorito = partido_data['cuota_visitante']
    
    st.markdown(f"""
    <div class="parley-card">
        <div style="text-align: center; margin-bottom: 15px;">
            <span style="font-size: 14px; color: #9ca3af;">{partido_data['liga']}</span>
        </div>
        <h3 style="text-align: center; margin: 10px 0;">
            {partido_data['emoji']} {partido_data['local']} vs {partido_data['visitante']}
        </h3>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 10px; margin: 20px 0;">
            <div style="text-align: center; padding: 10px; background-color: #0e0e12; border-radius: 6px;">
                <div style="color: #9ca3af; font-size: 12px;">Local</div>
                <div class="stat-value">@{partido_data['cuota_local']}</div>
            </div>
            <div style="text-align: center; padding: 10px; background-color: #0e0e12; border-radius: 6px;">
                <div style="color: #9ca3af; font-size: 12px;">Empate</div>
                <div class="stat-value">@{partido_data['cuota_empate']}</div>
            </div>
            <div style="text-align: center; padding: 10px; background-color: #0e0e12; border-radius: 6px;">
                <div style="color: #9ca3af; font-size: 12px;">Visitante</div>
                <div class="stat-value">@{partido_data['cuota_visitante']}</div>
            </div>
        </div>
        <div style="display: flex; justify-content: space-between; margin-top: 15px; padding-top: 15px; border-top: 1px solid #2a2a35;">
            <div>
                <div style="color: #9ca3af; font-size: 12px;">BTTS</div>
                <div class="stat-value">@{partido_data['cuota_btts']}</div>
            </div>
            <div>
                <div style="color: #9ca3af; font-size: 12px;">Over 2.5</div>
                <div class="stat-value">@{partido_data['cuota_over25']}</div>
            </div>
            <div>
                <div style="color: #9ca3af; font-size: 12px;">xG</div>
                <div class="stat-value">{partido_data['goles_esperados']}</div>
            </div>
        </div>
        <div style="margin-top: 15px; text-align: center;">
            <span style="background-color: #5b21b6; padding: 8px 20px; border-radius: 6px; font-weight: 600;">
                💎 Favorito: {favorito} @{cuota_favorito}
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
    st.markdown("<p style='color: #9ca3af; margin-top: 5px;'>Encuentra las mejores apuestas de valor | NBA + Fútbol + Comunidad</p>", unsafe_allow_html=True)

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
    "🔥 Top Sugerencias",
    "🟣 Modo Draftea",
    "⚽ Fútbol",
    "🏀 NBA",
    "📜 Historial",
    "👥 Comunidad"
])

# ============================================================================
# TAB 1: TOP SUGERENCIAS
# ============================================================================

with tabs[0]:
    st.markdown("## 🔥 Top 3 Parleys del Día")
    st.markdown("Las mejores oportunidades seleccionadas para ti")
    st.markdown("")
    
    sugerencias = generar_top_sugerencias()
    
    cols = st.columns(3)
    for i, sug in enumerate(sugerencias):
        with cols[i]:
            render_parley_card(
                titulo=sug['titulo'],
                detalle=sug['detalle'],
                cuota=sug['cuota'],
                confianza=sug['confianza'],
                razon=sug['razon']
            )
            
            if st.button(f"💾 Guardar en Historial", key=f"save_top_{i}"):
                st.session_state.historial.append({
                    'fecha': datetime.now().strftime('%d/%m/%Y %H:%M'),
                    'tipo': sug['tipo'],
                    'descripcion': sug['titulo'],
                    'cuota': sug['cuota'],
                    'estado': 'Pendiente'
                })
                st.success("✅ Guardado en historial")
                st.rerun()
    
    st.markdown("")
    st.markdown("---")
    
    # Métricas del día
    st.markdown("### 📊 Estadísticas del Día")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Parleys Activos", len(st.session_state.historial))
    with col2:
        st.metric("Cuota Promedio", f"@{random.uniform(1.85, 2.15):.2f}")
    with col3:
        st.metric("Win Rate", f"{random.randint(55, 72)}%")
    with col4:
        st.metric("ROI Semanal", f"+{random.randint(8, 25)}%")

# ============================================================================
# TAB 2: MODO DRAFTEA
# ============================================================================

with tabs[1]:
    st.markdown("## 🟣 Modo Draftea - Player Props Generator")
    st.markdown("Generador inteligente de props para jugadores NBA")
    st.markdown("")
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    with col1:
        prop_seleccionado = st.selectbox(
            "🎯 Tipo de Prop",
            ["Puntos", "Rebotes", "Asistencias", "Triples"],
            key="draftea_prop"
        )
    with col2:
        min_cuota = st.slider("💰 Cuota Mínima", 1.5, 3.0, 1.8, 0.1, key="draftea_cuota")
    with col3:
        num_props = st.slider("📊 Número de Props", 3, 10, 6, key="draftea_num")
    
    st.markdown("---")
    
    nba_data = generar_datos_nba()
    
    # Filtrar por cuota mínima
    if prop_seleccionado == "Puntos":
        filtered_data = [p for p in nba_data if p['cuota_puntos'] >= min_cuota]
    elif prop_seleccionado == "Rebotes":
        filtered_data = [p for p in nba_data if p['cuota_rebotes'] >= min_cuota]
    else:
        filtered_data = [p for p in nba_data if p['cuota_asistencias'] >= min_cuota]
    
    filtered_data = filtered_data[:num_props]
    
    # Mostrar props en grid
    cols_per_row = 3
    for i in range(0, len(filtered_data), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            if i + j < len(filtered_data):
                with col:
                    render_player_prop_card(filtered_data[i + j], prop_seleccionado)
                    
                    if st.button(f"💾 Guardar", key=f"save_draftea_{i}_{j}"):
                        jugador = filtered_data[i + j]
                        st.session_state.historial.append({
                            'fecha': datetime.now().strftime('%d/%m/%Y %H:%M'),
                            'tipo': 'NBA',
                            'descripcion': f"{jugador['jugador']} - {prop_seleccionado}",
                            'cuota': jugador[f'cuota_{prop_seleccionado.lower()}'],
                            'estado': 'Pendiente'
                        })
                        st.success("✅ Guardado")
                        st.rerun()

# ============================================================================
# TAB 3: FÚTBOL
# ============================================================================

with tabs[2]:
    st.markdown("## ⚽ Predicciones de Fútbol")
    st.markdown("Análisis de partidos y mercados principales")
    st.markdown("")
    
    # Filtros
    col1, col2 = st.columns(2)
    with col1:
        liga_filtro = st.selectbox(
            "🏆 Filtrar por Liga",
            ["Todas", "Premier League", "La Liga", "Serie A", "Bundesliga", "Ligue 1"],
            key="futbol_liga"
        )
    with col2:
        mercado_filtro = st.selectbox(
            "📊 Mercado",
            ["Todos", "Ganador", "BTTS", "Over/Under"],
            key="futbol_mercado"
        )
    
    st.markdown("---")
    
    futbol_data = generar_datos_futbol()
    
    # Filtrar por liga
    if liga_filtro != "Todas":
        futbol_data = [p for p in futbol_data if p['liga'] == liga_filtro]
    
    # Mostrar partidos
    cols_per_row = 2
    for i in range(0, len(futbol_data), cols_per_row):
        cols = st.columns(cols_per_row)
        for j, col in enumerate(cols):
            if i + j < len(futbol_data):
                with col:
                    render_futbol_card(futbol_data[i + j])
                    
                    if st.button(f"💾 Guardar Predicción", key=f"save_futbol_{i}_{j}"):
                        partido = futbol_data[i + j]
                        st.session_state.historial.append({
                            'fecha': datetime.now().strftime('%d/%m/%Y %H:%M'),
                            'tipo': 'Fútbol',
                            'descripcion': f"{partido['local']} vs {partido['visitante']}",
                            'cuota': min(partido['cuota_local'], partido['cuota_visitante']),
                            'estado': 'Pendiente'
                        })
                        st.success("✅ Guardado")
                        st.rerun()

# ============================================================================
# TAB 4: NBA
# ============================================================================

with tabs[3]:
    st.markdown("## 🏀 Predicciones NBA")
    st.markdown("Props y análisis de jugadores")
    st.markdown("")
    
    # Selector de categoría
    categoria = st.radio(
        "📊 Categoría",
        ["Puntos", "Rebotes", "Asistencias", "Triples"],
        horizontal=True,
        key="nba_categoria"
    )
    
    st.markdown("---")
    
    nba_data = generar_datos_nba()
    
    # Ordenar según categoría
    if categoria == "Puntos":
        nba_data.sort(key=lambda x: x['puntos'], reverse=True)
    elif categoria == "Rebotes":
        nba_data.sort(key=lambda x: x['rebotes'], reverse=True)
    elif categoria == "Asistencias":
        nba_data.sort(key=lambda x: x['asistencias'], reverse=True)
    else:
        nba_data.sort(key=lambda x: x['triples'], reverse=True)
    
    # Top 6 jugadores
    for i in range(0, 6, 3):
        cols = st.columns(3)
        for j, col in enumerate(cols):
            if i + j < 6:
                with col:
                    render_player_prop_card(nba_data[i + j], categoria)

# ============================================================================
# TAB 5: HISTORIAL
# ============================================================================

with tabs[4]:
    st.markdown("## 📜 Historial de Apuestas")
    st.markdown("Tus parleys guardados y su seguimiento")
    st.markdown("")
    
    if not st.session_state.historial:
        st.info("📭 No tienes parleys guardados aún. ¡Empieza a guardar tus favoritos!")
    else:
        # Botones de acción
        col1, col2 = st.columns([6, 1])
        with col2:
            if st.button("🗑️ Limpiar Todo"):
                st.session_state.historial = []
                st.rerun()
        
        st.markdown("---")
        
        # Mostrar historial
        for i, apuesta in enumerate(reversed(st.session_state.historial)):
            col1, col2, col3 = st.columns([3, 2, 2])
            
            with col1:
                st.markdown(f"""
                <div class="parley-card" style="margin: 5px 0;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <strong>{apuesta['descripcion']}</strong>
                            <div style="color: #9ca3af; font-size: 12px; margin-top: 5px;">
                                {apuesta['fecha']} | {apuesta['tipo']}
                            </div>
                        </div>
                        <div>
                            <span class="neon-text">@{apuesta['cuota']}</span>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                estado_color = {
                    'Pendiente': '#f59e0b',
                    'Ganada': '#10b981',
                    'Perdida': '#ef4444'
                }
                estado = st.selectbox(
                    "Estado",
                    ["Pendiente", "Ganada", "Perdida"],
                    index=["Pendiente", "Ganada", "Perdida"].index(apuesta['estado']),
                    key=f"estado_{i}"
                )
                if estado != apuesta['estado']:
                    st.session_state.historial[len(st.session_state.historial) - 1 - i]['estado'] = estado
                    st.rerun()
            
            with col3:
                if st.button("❌ Eliminar", key=f"delete_{i}"):
                    st.session_state.historial.pop(len(st.session_state.historial) - 1 - i)
                    st.rerun()
        
        # Estadísticas del historial
        st.markdown("---")
        st.markdown("### 📊 Estadísticas del Historial")
        
        ganadas = len([a for a in st.session_state.historial if a['estado'] == 'Ganada'])
        perdidas = len([a for a in st.session_state.historial if a['estado'] == 'Perdida'])
        pendientes = len([a for a in st.session_state.historial if a['estado'] == 'Pendiente'])
        total = len(st.session_state.historial)
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Apuestas", total)
        with col2:
            st.metric("✅ Ganadas", ganadas)
        with col3:
            st.metric("❌ Perdidas", perdidas)
        with col4:
            win_rate = (ganadas / (ganadas + perdidas) * 100) if (ganadas + perdidas) > 0 else 0
            st.metric("Win Rate", f"{win_rate:.1f}%")

# ============================================================================
# TAB 6: COMUNIDAD
# ============================================================================

with tabs[5]:
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
            col1, col2, col3, col4 = st.columns([2, 2, 1, 1])
            
            with col1:
                if st.button(f"🤑 ¡Pagó! ({post['votos_pago']})", key=f"voto_si_{post['id']}", use_container_width=True):
                    if post['id'] not in post['votantes']:
                        post['votos_pago'] += 1
                        post['votantes'].append(post['id'])
                        st.rerun()
                    else:
                        st.warning("Ya votaste este post")
            
            with col2:
                if st.button(f"🤡 Nadota ({post['votos_nadota']})", key=f"voto_no_{post['id']}", use_container_width=True):
                    if post['id'] not in post['votantes']:
                        post['votos_nadota'] += 1
                        post['votantes'].append(post['id'])
                        st.rerun()
                    else:
                        st.warning("Ya votaste este post")
            
            with col3:
                if st.button("💾", key=f"save_community_{post['id']}", help="Guardar en historial"):
                    st.session_state.historial.append({
                        'fecha': datetime.now().strftime('%d/%m/%Y %H:%M'),
                        'tipo': post['tipo'],
                        'descripcion': f"{post['nick']}: {post['prediccion'][:50]}...",
                        'cuota': post['cuota'],
                        'estado': 'Pendiente'
                    })
                    st.success("✅")
                    st.rerun()
            
            with col4:
                if st.button("🗑️", key=f"delete_post_{post['id']}", help="Eliminar post"):
                    st.session_state.community_posts = [p for p in st.session_state.community_posts if p['id'] != post['id']]
                    st.rerun()
            
            st.markdown("---")

# ============================================================================
# FOOTER
# ============================================================================

st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; padding: 20px; background-color: #1a1a23; border-radius: 10px; margin-top: 40px;'>
    <h3 style='color: #5b21b6; margin-bottom: 10px;'>Parley Hunter Pro</h3>
    <p style='color: #9ca3af; font-size: 14px;'>
        ⚠️ <strong>Advertencia:</strong> Las apuestas deportivas implican riesgos. Juega responsablemente.<br>
        📊 Datos simulados para fines demostrativos | 🚀 Powered by Streamlit + Python<br>
        💡 Esta herramienta es solo para fines educativos e informativos
    </p>
    <p style='color: #5b21b6; font-size: 12px; margin-top: 10px;'>
        v2.0 Pro Edition | Made with 💜 by Parley Hunters
    </p>
</div>
""", unsafe_allow_html=True)
