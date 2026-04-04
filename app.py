import streamlit as st
import pandas as pd
from st_supabase_connection import SupabaseConnection

# 1. CONFIGURACIÓN DE PANTALLA PRO
st.set_page_config(page_title="PREGÓN AI | Enterprise", layout="wide")

# 2. CONEXIÓN (Mantenemos tus llaves)
URL_BASE = "https://dqwqrzbskjzxjgihqrzc.supabase.co"
KEY_BASE = "sb_publishable_B8SRZbxZV6IldEkpfnKsWg_bLfg1MUE"

# Conexión estándar para datos y conexión "client" para autenticación
conn = st.connection("supabase", type=SupabaseConnection, url=URL_BASE, key=KEY_BASE)
supabase = conn.client

# 3. MANEJO DE SESIÓN (LOGIN/LOGOUT)
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
            st.error(f"Error de acceso: {e}") # Esto nos dirá el mensaje real de Supabase

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

# 4. ESTILOS CSS (Fuerza visual)
st.markdown("""
    <style>
    .stApp { background-color: #0E1117 !important; }
    h1, h2, h3, h4, h5, h6, p, span, label, .stMarkdown { color: #FFFFFF !important; }
    [data-testid="stMetricValue"] { color: #00FF00 !important; }
    [data-testid="stSidebar"] { background-color: #161B22 !important; }
    .stButton>button { background-color: #238636 !important; color: white !important; font-weight: bold !important; width: 100%; }
    .stDataFrame { background-color: #161B22; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- LÓGICA DE NAVEGACIÓN ---

if st.session_state.user is None:
    # SI NO HAY USUARIO: Pantalla de Bienvenida
    st.title("🚀 PREGÓN AI")
    st.subheader("La red de inteligencia de datos más potente de RD.")
    st.info("Para acceder a tus leads y configurar tu radar, inicia sesión en el panel de la izquierda.")
    st.image("https://images.unsplash.com/photo-1551288049-bbbda536339a?auto=format&fit=crop&q=80&w=1000", caption="Análisis de mercado en tiempo real")
    login_form()
else:
    # SI HAY USUARIO: Dashboard Real
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
            # Filtramos por owner_id para que cada dealer vea lo suyo
            res = supabase.from_("leads").select("*").eq("owner_id", st.session_state.user.id).execute()
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Mis Leads", len(res.data) if res.data else "0")
            c2.metric("Intención Alta", "92%", "🔥")
            c3.metric("Plan Actual", "DEMO")

            st.markdown("### 📋 Prospectos Detectados")
            if res.data:
                df = pd.DataFrame(res.data)
                cols_finales = [c for c in ["usuario_ig", "comentario", "vehiculo_interes", "created_at"] if c in df.columns]
                st.dataframe(df[cols_finales], use_container_width=True)
            else:
                st.info("Aún no tienes leads. Tu radar está listo para recibir datos.")
        except Exception as e:
            st.error(f"Error cargando datos: {e}")

    elif menu == "Radar":
        st.title("📡 Configuración del Radar Personal")
        st.write("Define qué cuentas de Instagram quieres que la IA analice por ti.")
        
        # Formulario para añadir nueva cuenta
        with st.form("nuevo_radar"):
            target_ig = st.text_input("Instagram del Dealer Competencia", placeholder="@dealer_ejemplo")
            submit = st.form_submit_button("Añadir a Monitoreo")
            
            if submit and target_ig:
                if not target_ig.startswith("@"):
                    st.warning("Recuerda incluir el @ al principio.")
                else:
                    try:
                        # Guardamos en la nueva tabla vinculando al ID del usuario actual
                        data_insert = {
                            "owner_id": st.session_state.user.id,
                            "cuenta_instagram": target_ig,
                            "esta_activo": True
                        }
                        supabase.table("radar_config").insert(data_insert).execute()
                        st.success(f"¡Objetivo fijado! {target_ig} ahora está bajo vigilancia.")
                    except Exception as e:
                        st.error(f"Error al guardar: {e}")

        # Mostrar las cuentas que ya está rastreando este usuario
        st.markdown("---")
        st.subheader("🕵️ Cuentas bajo vigilancia actual")
        try:
            mis_objetivos = supabase.table("radar_config").select("*").eq("owner_id", st.session_state.user.id).execute()
            if mis_objetivos.data:
                df_radar = pd.DataFrame(mis_objetivos.data)
                st.table(df_radar[["cuenta_instagram", "esta_activo"]])
            else:
                st.info("Aún no tienes cuentas en monitoreo. Añade la primera arriba.")
        except:
            pass

    elif menu == "Pagos":
        st.title("💳 Activación de Servicio")
        st.write("Tu cuenta está en modo gratuito.")
        if st.button("Subir a Plan Premium (WhatsApp)"):
            st.markdown("[Hablar con Soporte para Pago](https://wa.me/18490000000?text=Hola,%20quiero%20pagar%20mi%20plan%20Premium)")
