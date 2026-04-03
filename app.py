import streamlit as st

# Configuración de página con Look Profesional
st.set_page_config(page_title="PREGÓN AI | Intelligence", layout="wide")

# CSS Avanzado para Look "Black Edition" y Contraste Alto
st.markdown("""
    <style>
    /* Fondo total negro profundo */
    .stApp { background-color: #050505; color: #FFFFFF; }
    
    /* Estilo de las tarjetas de métricas */
    div[data-testid="stMetric"] {
        background-color: #121212;
        border: 1px solid #222222;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    
    /* Sidebar elegante */
    section[data-testid="stSidebar"] { background-color: #000000; border-right: 1px solid #1f1f1f; }
    
    /* Botón de Pago estilo Premium */
    .stButton>button {
        background-color: #E50914; /* Rojo Netflix */
        color: white;
        border-radius: 8px;
        width: 100%;
        border: none;
        font-weight: bold;
        padding: 10px;
    }
    
    /* Mejorar visibilidad de tablas */
    .stTable { background-color: #121212; border-radius: 10px; color: white !important; }
    th { color: #E50914 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<h1 style='color: #E50914;'>PREGÓN AI</h1>", unsafe_allow_html=True)
    st.markdown("---")
    menu = st.radio("Navegación", ["🔥 Leads del Día", "📡 Radar de Competencia", "💎 Plan Premium"])
    st.markdown("---")
    st.write("Versión: 1.0.2 (Alpha)")

# --- CONTENIDO PRINCIPAL ---
if menu == "🔥 Leads del Día":
    st.markdown("## 🚗 Dashboard de Inteligencia")
    st.markdown("<p style='color: #888;'>Filtro de intención de compra detectado por IA en República Dominicana.</p>", unsafe_allow_html=True)
    
    # Métricas con mejor contraste
    c1, c2, c3 = st.columns(3)
    c1.metric("Leads Identificados", "24", "+5")
    c2.metric("Intención de Compra", "92%", "Alta")
    c3.metric("Oportunidad de Venta", "RD$ 6.8M")

    st.markdown("### 📋 Prospectos Calientes")
    # Tabla simulada (después vendrá de Supabase)
    leads = [
        {"Canal": "IG", "Usuario": "@jose_luxury", "Interés": "Toyota Hilux", "Comentario": "¿Qué año y precio?", "Score": "🔥 98%"},
        {"Canal": "IG", "Usuario": "@ana_vargas", "Interés": "Lexus LX", "Comentario": "Tengo el inicial", "Score": "🔥 95%"},
        {"Canal": "IG", "Usuario": "@melo_autos", "Interés": "Honda CR-V", "Comentario": "¿Reciben carro?", "Score": "✅ 88%"}
    ]
    st.table(leads)

elif menu == "📡 Radar de Competencia":
    st.title("📡 Radar en Tiempo Real")
    st.write("Configura las cuentas que deseas espiar.")
    st.text_input("Ingresa el @usuario (ej: @mikonosrd)")
    if st.button("Activar Rastreo de Cuentas"):
        st.success("Radar configurado. Empezaremos a buscar leads en esa cuenta.")

elif menu == "💎 Plan Premium":
    st.markdown("## 💎 Sube de nivel tu Dealer")
    st.write("Para ver leads ilimitados y recibir alertas por WhatsApp, activa tu plan.")
    
    st.markdown("""
    - **Radar Ilimitado:** Espía hasta 100 competidores.
    - **IA Avanzada:** Filtrado de jerga dominicana (KLK, dime de eso, etc).
    - **Alertas WhatsApp:** Notificación al segundo.
    """)
    
    # AQUÍ ESTÁ TU BOTÓN DE COBRO
    if st.button("Hablar con Soporte para Activar"):
        st.write("Redirigiendo a WhatsApp del Ingeniero Lixander...")
        # Enlace real a tu WhatsApp
        st.markdown("[Haz clic aquí para pagar vía WhatsApp](https://wa.me/tu_numero_aqui?text=Hola,%20quiero%20activar%20mi%20plan%20Premium%20en%20Pregon%20AI)")
