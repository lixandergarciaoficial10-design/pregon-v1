import streamlit as st
import pandas as pd
from st_supabase_connection import SupabaseConnection

# 1. Configuración de Pantalla
st.set_page_config(page_title="PREGÓN AI | Data Intelligence", layout="wide")

# 2. CONEXIÓN A TU BASE DE DATOS (Tus llaves ya integradas)
URL_BASE = "https://dqwqrzbskjzxjgihqrzc.supabase.co"
KEY_BASE = "sb_publishable_B8SRZbxZV6IldEkpfnKsWg_bLfg1MUE"

# Inicializamos la conexión
conn = st.connection("supabase", type=SupabaseConnection, url=URL_BASE, key=KEY_BASE)

# 3. CSS INTELIGENTE (Para que se vea Pro)
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
    .stTable, table { color: #FFFFFF !important; background-color: #161B22 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- NAVEGACIÓN ---
st.sidebar.title("🚀 PREGÓN AI")
menu = st.sidebar.selectbox("Módulo", ["Dashboard", "Radar", "Pagos"])

if menu == "Dashboard":
    st.title("Inteligencia de Datos Dominante")
    st.write("Análisis de leads en tiempo real para el sector automotriz.")
    
    # 4. LEER DATOS REALES DE SUPABASE
    try:
        # Consultamos tu tabla 'dirige'
        res = conn.query("*", table="dirige", ttl="0").execute()
        
        # KPIs (Aquí podrías poner fórmulas reales basadas en los datos)
        c1, c2, c3 = st.columns(3)
        c1.metric("Leads Totales", len(res.data) if res.data else "0", "+")
        c2.metric("Intención Alta", "92%", "🔥")
        c3.metric("Estado Radar", "ACTIVO")

        st.markdown("### 📋 Prospectos en Vivo (Desde la Base de Datos)")
        
        if res.data:
            # Mostramos los datos que tú mismo insertaste en Supabase
            st.dataframe(res.data, use_container_width=True)
        else:
            st.info("El radar está encendido. Esperando que entren leads a la tabla 'dirige'...")

    except Exception as e:
        st.error(f"Error conectando al almacén de datos: {e}")

elif menu == "Radar":
    st.title("📡 Configuración del Radar")
    st.write("Añade cuentas de la competencia para rastrear.")
    st.text_input("Cuenta de Instagram (@)")
    if st.button("Activar Rastreo"):
        st.success("Radar configurado correctamente.")

elif menu == "Pagos":
    st.title("💳 Activación de Cuenta")
    st.write("Haz clic abajo para pagar y activar tu acceso completo.")
    if st.button("Pagar vía WhatsApp"):
        # Cambia 'tu_numero' por tu número real para que te llegue el mensaje
        st.markdown("[Ir a WhatsApp](https://wa.me/18490000000?text=Hola%20Lixander,%20quiero%20pagar%20mi%20plan%20Premium)")
