# 🎯 Parley Hunter (Free Edition)

Aplicación web gratuita para encontrar apuestas de valor (Parleys) en NFL y Fútbol.

## 📋 Características

- ✅ **NFL**: Props de QB (Passing Yards) y WR/TE (Receiving Yards)
- ✅ **Fútbol**: Over/Under Goles y BTTS (Ambos Equipos Anotan)
- ✅ **Datos Reales**: NFL Data Py + Web Scraping de FBref
- ✅ **3 Categorías**: Parleys Seguros, de Valor y Arriesgados
- ✅ **Caché Inteligente**: Carga rápida de datos
- ✅ **Fallback a Mock Data**: Si el scraping falla, usa datos simulados

## 🚀 Instalación

### 1. Clonar/Descargar archivos
Asegúrate de tener los archivos:
- `app.py`
- `requirements.txt`

### 2. Crear entorno virtual (Opcional pero recomendado)
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Ejecutar la aplicación
```bash
streamlit run app.py
```

La app se abrirá automáticamente en tu navegador en `http://localhost:8501`

## 📖 Cómo Usar

1. **Selecciona el Deporte** (NFL o Fútbol) en la barra lateral
2. **Elige el Mercado** (Props QB, WR/TE, Goles, BTTS)
3. **Haz clic en "Buscar Parleys"**
4. **Revisa las 3 columnas**:
   - 🟢 **Parleys Seguros**: Alta probabilidad, cuotas bajas
   - 🟡 **Parleys de Valor**: Balance riesgo/recompensa
   - 🔴 **Parleys Arriesgados**: Cuotas altas, más riesgo

## 🔧 Solución de Problemas

### Error al cargar datos de NFL
Si `nfl_data_py` tarda mucho o falla:
- La app automáticamente usará datos simulados
- Primera carga puede tardar 30-60 segundos (se cachea después)

### Error de scraping en fútbol
Si FBref bloquea el acceso:
- La app automáticamente usará datos simulados
- Considera usar un VPN o esperar unos minutos

### Dependencias no instaladas
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

## 📊 Fuentes de Datos

- **NFL**: `nfl_data_py` (Play-by-Play 2024-2025)
- **Fútbol**: FBref.com (Web Scraping con Pandas)
- **Fallback**: Datos simulados realistas

## ⚠️ Disclaimer

Esta herramienta es solo para fines educativos e informativos. Las apuestas deportivas conllevan riesgos financieros. Juega responsablemente.

## 📝 Notas Técnicas

- **Caché**: 1 hora (`@st.cache_data`)
- **NFL**: Mínimo 3 partidos jugados para estadísticas
- **Fútbol**: Scraping con `pd.read_html` + lxml
- **Interfaz**: Streamlit con layout de 3 columnas

## 🆕 Próximas Mejoras (Ideas)

- [ ] Más ligas de fútbol (Bundesliga, Serie A)
- [ ] Props de rushing yards NFL
- [ ] Sistema de historial de parleys
- [ ] Exportar parleys a CSV
- [ ] Integración con APIs de cuotas

---

**Versión**: 1.0  
**Creado con**: Python 3.9+ | Streamlit | NFL Data Py
