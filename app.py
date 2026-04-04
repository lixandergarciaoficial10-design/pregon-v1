import streamlit as st
import pandas as pd
from st_supabase_connection import SupabaseConnection

# 1. CONFIGURACIÓN DE PANTALLA PRO
st.set_page_config(page_title="PREGÓN AI | Enterprise", layout="wide")

# 2. CONEXIÓN (Mantenemos tus llaves)
URL_BASE = "https://dqwqrzbskjzxjgihqrzc.supabase.co"
KEY_BASE = "sb_publishable_B8SRZbxZV6IldEkpfnKsWg_bLfg1MUE"

# Conexión estándar
conn = st.connection("supabase", type=SupabaseConnection, url=URL_BASE, key=KEY_BASE)
supabase = conn.client

# 3. MANEJO DE SESIÓN
if 'user' not in st.session_state:
    st.session_state.user = None

def login_form():
    with st.sidebar:
        st.title("🔐 Acceder a Pregón AI")
        tab1, tab2 = st.tabs(["Ingresar", "Registrarse"])
        
        with tab1:
            email = st.text_input("Correo", key="login_email")
            password = st.text_input("Contraseña", type="password", key="login_pass")
            if st.button("Entrar"):
                try:
                    res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                    st.session_state.user = res.user
                    st.rerun()
                except Exception as e:
                    st.error(f"Error de acceso: {e}")

        with tab2:
            st.write("Crea tu cuenta")
            new_email = st.text_input("Nuevo Correo", key="reg_email")
            new_password = st.text_input("Nueva Contraseña", type="password", key="reg_pass")
            if st.button("Crear Cuenta"):
                try:
                    supabase.auth.sign_up({"email": new_email, "password": new_password})
                    st.success("¡Cuenta creada! Ya puedes ingresar.")
                except Exception as e:
                    st.error(f"Error: {e}")

# 4. ESTILOS CSS
st.markdown("""
    <style>
    .stApp { background-color: #0E1117 !important; }
    h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown { color: #FFFFFF !important; }
    [data-testid="stMetricValue"] { color: #00FF00 !important; }
    [data-testid="stSidebar"] { background-color: #161B22 !important; }
    .stButton>button { background-color: #238636 !important; color: white !important; font-weight: bold !important; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE NAVEGACIÓN ---

if st.session_state.user is None:
    st.title("🚀 PREGÓN AI")
    st.subheader("La red de inteligencia de datos automotriz más potente de RD.")
    st.info("Inicia sesión en el panel lateral para continuar.")
    login_form()
else:
    st.sidebar.title("🚀 PREGÓN AI")
    st.sidebar.write(f"Usuario: **{st.session_state.user.email}**")
    
    menu = st.sidebar.selectbox("Módulo", ["Dashboard", "Radar", "Pagos"])
    
    if st.sidebar.button("Cerrar Sesión"):
        supabase.auth.sign_out()
        st.session_state.user = None
        st.rerun()

    if menu == "Dashboard":
        st.title("Inteligencia de Datos Dominante")
        try:
            # Filtramos leads por el usuario actual
            res = supabase.from_("leads").select("*").eq("owner_id", st.session_state.user.id).execute()
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Mis Leads", len(res.data) if res.data else "0")
            c2.metric("Intención Alta", "92%", "🔥")
            c3.metric("Plan", "DEMO")

            if res.data:
                df = pd.DataFrame(res.data)
                st.dataframe(df, use_container_width=True)
            else:
                st.info("No hay leads aún.")
        except Exception as e:
            st.error(f"Error: {e}")

    elif menu == "Radar":
        st.title("📡 Configuración del Radar")
        with st.form("radar_form"):
            target = st.text_input("Instagram del Dealer (ej: @saulauto)")
            if st.form_submit_button("Añadir a Monitoreo"):
                try:
                    data = {"owner_id": st.session_state.user.id, "cuenta_instagram": target, "esta_activo": True}
                    supabase.table("radar_config").insert(data).execute()
                    st.success(f"Vigilando a {target}")
                except Exception as e:
                    st.error(f"Error: {e}")
        
        # Mostrar lo que ya rastreamos
        try:
            res_r = supabase.table("radar_config").select("*").eq("owner_id", st.session_state.user.id).execute()
            if res_r.data:
                st.table(pd.DataFrame(res_r.data)[["cuenta_instagram", "esta_activo"]])
        except:
            pass

    elif menu == "Pagos":
        st.title("💳 Pagos")
        st.write("Contacta a soporte para activar tu plan.")
