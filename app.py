import streamlit as st

# 1. Configuración de Lujo (Tipo Netflix)
st.set_page_config(page_title="PREGÓN AI | Dashboard", layout="wide")

# Estilo Visual Negro y Rojo
st.markdown("""
    <style>
    .main { background-color: #000000; color: #ffffff; }
    .stSidebar { background-color: #141414; }
    h1 { color: #E50914; font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif; }
    .stMetric { background-color: #1f1f1f; padding: 15px; border-radius: 10px; border-left: 5px solid #E50914; }
    </style>
    """, unsafe_allow_html=True)

# 2. Barra Lateral (Sidebar)
with st.sidebar:
    st.markdown("# 🚀 PREGÓN AI")
    st.markdown("---")
    menu = st.radio("Navegación", ["🔥 Leads Calientes", "📡 Radar Global", "💳 Mi Suscripción"])
    st.markdown("---")
    st.info("Ingeniería de Datos para Dealers")

# 3. Contenido Principal
if menu == "🔥 Leads Calientes":
    st.title("Clientes Detectados por IA")
    
    # Métricas rápidas
    col1, col2, col3 = st.columns(3)
    col1.metric("Leads Hoy", "12", "+2")
    col2.metric("Intención Alta", "85%", "Excelente")
    col3.metric("Ventas Estimadas", "RD$ 4.5M")

    st.markdown("### 📊 Lista de Interesados (Última hora)")
    # Datos de ejemplo (Luego los traeremos de la base de datos)
    datos_prueba = [
        {"Usuario": "@juan_perez", "Vehículo": "Toyota Hilux 2022", "Comentario": "¿Precio y financiamiento?", "IA Score": "98%"},
        {"Usuario": "@maria_rd", "Vehículo": "Honda CR-V", "Comentario": "¿Reciben vehículo?", "IA Score": "94%"},
        {"Usuario": "@pedro_vende", "Vehículo": "Lexus LX600", "Comentario": "Info por favor", "IA Score": "89%"}
    ]
    st.table(datos_prueba)

elif menu == "📡 Radar Global":
    st.title("📡 Radar de Competencia")
    st.write("Configura aquí las cuentas que estamos espiando para ti.")
    st.text_input("Agregar cuenta de Instagram (ej: @lixandergarciaoficial10)")
    st.button("Activar Rastreo")

elif menu == "💳 Mi Suscripción":
    st.title("Estado de Cuenta")
    st.warning("Tu suscripción vence en 15 días.")
    st.button("Renovar Plan Business")
