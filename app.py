import streamlit as st
import pandas as pd
from st_supabase_connection import SupabaseConnection

# 1. Configuración de Pantalla
st.set_page_config(page_title="PREGÓN AI | Data Intelligence", layout="wide")

# 2. CONEXIÓN A TU BASE DE DATOS (Verificada)
URL_BASE = "https://dqwqrzbskjzxjgihqrzc.supabase.co"
KEY_BASE = "sb_publishable_B8SRZbxZV6IldEkpfnKsWg_bLfg1MUE"

# Inicializamos la conexión
conn = st.connection("supabase", type=SupabaseConnection, url=URL_BASE, key=KEY_BASE)

# 3. CSS PROFESIONAL (Fuerza visibilidad y contraste)
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
    /* Estilo para que la tabla sea legible */
    .stDataFrame { background-color: #161B22; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- NAVEGACIÓN ---
st.sidebar.title("🚀 PREGÓN AI")
menu = st.sidebar.selectbox("Módulo", ["Dashboard", "Radar", "Pagos"])

if menu == "Dashboard":
    st.title("Inteligencia de Datos Dominante")
    st.write("Análisis de leads en tiempo real desde Supabase.")
    
    # 4. LEER DATOS REALES DE LA TABLA 'leads'
    try:
        # Usamos .from_("leads") que es más estable
        res = conn.client.from_("leads").select("*").execute()
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Leads Totales", len(res.data) if res.data else "0", "+")
        c2.metric("Intención Alta", "92%", "🔥")
        c3.metric("Estado Radar", "ACTIVO")

        st.markdown("### 📋 Prospectos en Vivo (Tabla: leads)")
        
        if res.data:
            # Convertimos a tabla limpia de Pandas
            df = pd.DataFrame(res.data)
            
            # Definimos las columnas que quieres mostrar (ajustadas a tus capturas)
            # Nota: creado_en suele ser el nombre por defecto de created_at en español si lo tradujiste
            cols_deseadas = ["usuario_ig", "comentario", "vehiculo_interes", "score_ia", "created_at"]
            
            # Filtramos solo las que existan realmente en tu tabla para evitar errores
            cols_finales = [c for c in cols_deseadas if c in df.columns]
            
            st.dataframe(df[cols_finales], use_container_width=True)
        else:
            st.info("Conexión exitosa. La tabla 'leads' está vacía. Inserta un dato en Supabase para verlo aquí.")

    except Exception as e:
        st.error(f"Error de conexión: {e}")

elif menu == "Radar":
    st.title("📡 Configuración del Radar")
    st.write("Monitoreando cuentas de Instagram en RD.")
    st.text_input("Usuario a rastrear", placeholder="@dealer_ejemplo")
    if st.button("Actualizar Radar"):
        st.success("Radar actualizado.")

elif menu == "Pagos":
    st.title("💳 Activación")
    st.write("Estado de cuenta: Suspendido (Modo Demo)")
    if st.button("Pagar vía WhatsApp"):
        # Cambia el número por el tuyo para recibir el mensaje directamente
        st.markdown("[Abrir WhatsApp para pagar](https://wa.me/18490000000?text=Hola%20Lixander,%20quiero%20activar%20mi%20cuenta%20de%20Pregon%20AI)")
