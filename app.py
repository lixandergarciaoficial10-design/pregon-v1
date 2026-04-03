import streamlit as st

# 1. Configuración de Pestaña
st.set_page_config(page_title="PREGÓN AI | Netflix Edition", layout="wide")

# 2. INYECCIÓN DE DISEÑO NETFLIX (Fuerza Modo Oscuro y Colores Reales)
st.markdown("""
    <style>
    /* Forzar fondo negro Netflix en toda la app */
    .stApp, .main, .stSidebar, [data-testid="stHeader"] {
        background-color: #000000 !important;
        color: white !important;
    }

    /* Ocultar elementos innecesarios de Streamlit */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}

    /* El Rojo Netflix para Títulos y Botones */
    h1, h2, h3 {
        color: #E50914 !important;
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 2px;
    }

    /* Estilo de Tarjetas de Leads (Tipo Posters de Películas) */
    .lead-card {
        background-color: #141414;
        border-radius: 4px;
        padding: 15px;
        border-bottom: 3px solid #E50914;
        transition: transform .2s;
        margin-bottom: 20px;
    }
    .lead-card:hover {
        transform: scale(1.05);
        background-color: #1f1f1f;
    }

    /* Botón de Pago Estilo Netflix */
    .stButton>button {
        background-color: #E50914 !important;
        color: white !important;
        border: none !important;
        border-radius: 4px !important;
        font-weight: bold !important;
        font-size: 1.2rem !important;
        padding: 10px 20px !important;
    }

    /* Ajuste de Tablas para que no brillen en blanco */
    .stTable, [data-testid="stTable"] {
        background-color: #141414 !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- BARRA LATERAL (SIDEBAR) ---
with st.sidebar:
    st.markdown("<h1 style='font-size: 2.5rem;'>NETFLIX</h1>", unsafe_allow_html=True) # Logo texto estilo Netflix
    st.markdown("<p style='color: #808080; font-weight: bold;'>PREGÓN AI EDITION</p>", unsafe_allow_html=True)
    st.write("")
    menu = st.radio("", ["🏠 Inicio", "🔍 Explorar Radar", "📺 Mis Suscripción"])

# --- CONTENIDO PRINCIPAL ---
if menu == "🏠 Inicio":
    st.markdown("<h1>RECIÉN AGREGADOS</h1>", unsafe_allow_html=True)
    st.write("### Leads calientes detectados hoy en RD")
    
    # Simulación de Fila de Netflix (3 columnas)
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
            <div class="lead-card">
                <p style='color: #E50914; font-weight: bold;'>🔥 98% MATCH</p>
                <h3>@juan_melo</h3>
                <p><b>Vehículo:</b> Toyota Hilux 2023</p>
                <p><i>"Dime el precio de esa grasa, k lo k"</i></p>
            </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
            <div class="lead-card">
                <p style='color: #E50914; font-weight: bold;'>🔥 95% MATCH</p>
                <h3>@ana_perez</h3>
                <p><b>Vehículo:</b> Lexus LX600</p>
                <p><i>"¿Dónde están ubicados? Quiero ir hoy."</i></p>
            </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
            <div class="lead-card">
                <p style='color: #E50914; font-weight: bold;'>🔥 89% MATCH</p>
                <h3>@tiguere_ventas</h3>
                <p><b>Vehículo:</b> Honda Civic</p>
                <p><i>"¿Reciben vehículo y cuánto es el inicial?"</i></p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<h1>TENDENCIAS AHORA</h1>", unsafe_allow_html=True)
    st.info("Radar activo espiando 52 dealers en Santo Domingo y Santiago.")

elif menu == "🔍 Explorar Radar":
    st.title("CONFIGURAR RADAR")
    st.write("Añade cuentas de la competencia para empezar a extraer datos.")
    cuenta = st.text_input("Usuario de Instagram (ej: @mikonosrd)")
    if st.button("EMPEZAR A ESPIAR"):
        st.success(f"Radar fijado en {cuenta}. Los datos aparecerán en 'Inicio' pronto.")

elif menu == "📺 Mis Suscripción":
    st.title("PLANES Y PAGOS")
    st.write("Para ver los datos completos de los clientes y recibir alertas por WhatsApp:")
    st.markdown("### PLAN PREMIUM: RD$ 5,000 / mes")
    
    # BOTÓN DE PAGO
    if st.button("DESBLOQUEAR AHORA"):
        st.write("Conectando con el Ingeniero Lixander...")
        st.markdown("[Pagar vía WhatsApp / Transferencia](https://wa.me/tu_numero?text=Hola,%20quiero%20activar%20mi%20plan%20Premium)")
