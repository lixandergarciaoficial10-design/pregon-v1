import streamlit as st
import pandas as pd

# 1. Configuración de Pantalla
st.set_page_config(page_title="PREGÓN AI | Data Intelligence", layout="wide")

# 2. CSS INTELIGENTE (Soluciona el problema de contraste)
st.markdown("""
    <style>
    /* Forzamos el fondo oscuro para evitar errores de contraste en modo claro */
    .stApp {
        background-color: #0E1117 !important;
    }

    /* Forzamos que TODO el texto sea blanco o gris claro, sin importar el modo */
    h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown {
        color: #FFFFFF !important;
    }

    /* Estilo para las métricas (Cuadros de datos) */
    [data-testid="stMetricValue"] {
        color: #00FF00 !important; /* Verde Neón para los números */
    }
    
    [data-testid="stMetricLabel"] {
        color: #888888 !important; /* Gris para las etiquetas */
    }

    /* Estilo de la Barra Lateral */
    [data-testid="stSidebar"] {
        background-color: #161B22 !important;
    }
    
    /* Botón de WhatsApp Estilo Pro */
    .stButton>button {
        background-color: #238636 !important;
        color: white !important;
        border: 1px solid #30363D !important;
        font-weight: bold !important;
    }

    /* Tablas legibles en cualquier modo */
    .stTable, table {
        color: #FFFFFF !important;
        background-color: #161B22 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- CONTENIDO ---
st.sidebar.title("🚀 PREGÓN AI")
menu = st.sidebar.selectbox("Módulo", ["Dashboard", "Radar", "Pagos"])

if menu == "Dashboard":
    st.title("Inteligencia de Datos Dominante")
    st.write("Análisis de leads en tiempo real para el sector automotriz.")
    
    # KPIs
    c1, c2, c3 = st.columns(3)
    c1.metric("Leads Totales", "142", "+5")
    c2.metric("Intención Alta", "92%", "🔥")
    c3.metric("Valor Mercado", "RD$ 12.4M")

    st.markdown("### 📋 Prospectos Recientes")
    # Tabla de ejemplo
    data = {
        "Usuario": ["@melo_luxury", "@vargas_auto", "@tiguere_rd"],
        "Vehículo": ["Lexus LX600", "Toyota Hilux", "Honda Civic"],
        "Intención": ["Compra Inmediata", "Financiamiento", "Permuta"]
    }
    st.table(data)

elif menu == "Pagos":
    st.title("💳 Activación de Cuenta")
    st.write("Haz clic abajo para pagar y activar tu acceso completo.")
    if st.button("Pagar vía WhatsApp"):
        st.markdown("[Ir a WhatsApp](https://wa.me/tu_numero)")
