import streamlit as st
import pandas as pd

# 1. Configuración de Pantalla Completa y Título
st.set_page_config(page_title="PREGÓN AI | Data Intelligence", layout="wide", initial_sidebar_state="expanded")

# 2. CSS PROFESIONAL (Estilo Dark Modern Enterprise)
st.markdown("""
    <style>
    /* Fondo General Profundo */
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    
    /* Sidebar Estilizado */
    [data-testid="stSidebar"] {
        background-color: #161B22;
        border-right: 1px solid #30363D;
    }

    /* Tarjetas de Métricas (KPIs) */
    div[data-testid="stMetric"] {
        background-color: #161B22;
        border: 1px solid #30363D;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.2);
    }

    /* Botones de Acción */
    .stButton>button {
        width: 100%;
        border-radius: 8px;
        height: 3em;
        background-color: #238636; /* Verde Éxito */
        color: white;
        border: none;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #2ea043;
        border: 1px solid #ffffff;
    }

    /* Títulos y Subtítulos */
    h1, h2, h3 {
        font-family: 'Inter', sans-serif;
        letter-spacing: -0.5px;
    }
    
    /* Badge de IA */
    .ia-badge {
        background-color: #1f6feb;
        color: white;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: bold;
    }

    /* Tablas Limpias */
    .styled-table {
        width: 100%;
        border-collapse: collapse;
        margin: 25px 0;
        font-size: 0.9em;
        min-width: 400px;
        border-radius: 5px 5px 0 0;
        overflow: hidden;
    }
    </style>
    """, unsafe_allow_html=True)

# --- NAVEGACIÓN ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=80) # Icono Tech
    st.markdown("## PREGÓN AI")
    st.markdown("---")
    menu = st.sidebar.selectbox(
        "Módulos del Sistema",
        ["📊 Dashboard Principal", "🔍 Radar de Competencia", "💰 Gestión de Pagos"]
    )
    st.markdown("---")
    st.caption("Conectado a la Red de Datos RD v2.4")

# --- LÓGICA DE PANTALLAS ---

if menu == "📊 Dashboard Principal":
    st.title("Inteligencia de Mercado en Tiempo Real")
    st.markdown("#### Análisis de intención de compra en el sector automotriz")
    
    # KPIs Superiores
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Leads Identificados", "142", "+12 hoy")
    col2.metric("Conversión Estimada", "18.5%", "+2.1%")
    col3.metric("Competidores Bajo Radar", "45", "Activos")
    col4.metric("Valor de Cartera", "RD$ 12.4M", "Potencial")

    st.markdown("---")
    
    # Fila de Leads
    st.subheader("🔥 Últimos Leads de Alta Intención")
    
    # Datos Estructurados
    df_leads = pd.DataFrame([
        {"Hora": "14:20", "Usuario": "@melo_luxury", "Interés": "Toyota Runner 2024", "IA Match": "98%", "Estado": "Caliente"},
        {"Hora": "14:15", "Usuario": "@pedro_vargas", "Interés": "Lexus LX600", "IA Match": "94%", "Estado": "Caliente"},
        {"Hora": "13:50", "Usuario": "@ana_ventas", "Interés": "Honda Civic 2020", "IA Match": "89%", "Estado": "Interesado"},
        {"Hora": "13:30", "Usuario": "@carlos_rd", "Interés": "Jeep Wrangler", "IA Match": "85%", "Estado": "Interesado"},
    ])
    
    st.table(df_leads)
    
    st.info("💡 Consejo: Los leads con IA Match superior al 90% tienen un 3x más de probabilidad de cierre inmediato.")

elif menu == "🔍 Radar de Competencia":
    st.title("Configuración de Rastreo Global")
    st.write("Añade cuentas de competidores para que la IA extraiga clientes potenciales.")
    
    col_a, col_b = st.columns([2,1])
    with col_a:
        cuenta = st.text_input("Nombre de usuario de Instagram", placeholder="@ejemplo_dealer")
    with col_b:
        st.write(" ") # Espaciador
        if st.button("Añadir al Radar"):
            st.success(f"La cuenta {cuenta} ha sido añadida a la cola de procesamiento.")

    st.markdown("### Cuentas Monitoreadas Actualmente")
    st.code("@mikonosrd\n@vegaautoimport\n@herreraauto\n@saulautoimport", language="markdown")

elif menu == "💰 Gestión de Pagos":
    st.title("Centro de Facturación")
    
    st.markdown("""
    ### Plan Business Pro
    **Estado:** <span style='color: #e50914;'>Pendiente de Activación</span>
    
    Para habilitar el acceso completo a los datos de contacto y alertas por WhatsApp, por favor completa el pago inicial.
    """, unsafe_allow_html=True)
    
    st.write("---")
    
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("#### Detalles del Plan")
        st.write("✅ Alertas de WhatsApp 24/7")
        st.write("✅ Radar de hasta 50 competidores")
        st.write("✅ Soporte técnico prioritario")
    
    with c2:
        st.markdown("#### Proceder al Pago")
        if st.button("Contactar con Administración (WhatsApp)"):
            st.write("Redirigiendo...")
            st.markdown("[Haz clic aquí para activar tu cuenta](https://wa.me/tu_numero)")
