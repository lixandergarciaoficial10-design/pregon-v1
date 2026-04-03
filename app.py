import streamlit as st
import pandas as pd
from st_supabase_connection import SupabaseConnection

# 1. Configuración de Pantalla
st.set_page_config(page_title="PREGÓN AI | Data Intelligence", layout="wide")

# 2. CONEXIÓN A TU BASE DE DATOS
URL_BASE = "https://dqwqrzbskjzxjgihqrzc.supabase.co"
KEY_BASE = "sb_publishable_B8SRZbxZV6IldEkpfnKsWg_bLfg1MUE"

# Inicializamos la conexión
conn = st.connection("supabase", type=SupabaseConnection, url=URL_BASE, key=KEY_BASE)

# 3. CSS PROFESIONAL
st.markdown("""
    <style>
    .stApp { background-color: #0E1117 !important; }
    h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown { color: #FFFFFF !important; }
    [data-testid="stMetricValue"] { color: #00FF00 !important; }
    [data-testid="stMetricLabel"] { color: #888888 !important; }
    [data-testid="stSidebar"] { background-color: #161B22 !important; }
    .stButton>button {
        background-color: #238636 !important;
        color: white !important;
        border: 1px solid #30363D !important;
        font-weight: bold !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- NAVEGACIÓN ---
st.sidebar.title("🚀 PREGÓN AI")
menu = st.sidebar.selectbox("Módulo", ["Dashboard", "Radar", "Pagos"])

if menu == "Dashboard":
    st.title("Inteligencia de Datos Dominante")
    st.write("Análisis de leads en tiempo real.")
    
    # 4. LEER DATOS REALES (Sintaxis Nueva)
    try:
        # AQUÍ ESTÁ EL CAMBIO: Usamos client.table().select()
        res = conn.client.table("dirige").select("*").execute()
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Leads Totales", len(res.data) if res.data else "0", "+")
        c2.metric("Intención Alta", "92%", "🔥")
        c3.metric("Estado Radar", "ACTIVO")

        st.markdown("### 📋 Prospectos en Vivo")
        
        if res.data:
            # Convertimos a tabla limpia de Pandas
            df = pd.DataFrame(res.data)
            # Reordenamos columnas para que se vea bien
            columnas_ordenadas = ["usuario_ig", "comentario", "interés_vehículo", "creado_en"]
            # Solo mostramos las columnas que existan en el DF
            st.dataframe(df[[c for c in columnas_ordenadas if c in df.columns]], use_container_width=True)
        else:
            st.info("El radar está encendido. No hay datos en la tabla 'dirige' todavía.")

    except Exception as e:
        st.error(f"Error de conexión: {e}")

elif menu == "Pagos":
    st.title("💳 Activación")
    if st.button("Pagar vía WhatsApp"):
        st.write("Redirigiendo...")
