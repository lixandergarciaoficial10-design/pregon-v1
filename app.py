import streamlit as st
import pandas as pd
from st_supabase_connection import SupabaseConnection

# =========================================
# CONFIGURACIÓN GENERAL
# =========================================
st.set_page_config(page_title="PREGÓN AI", layout="wide")

# =========================================
# CONEXIÓN A SUPABASE
# =========================================
URL_BASE = "https://dqwqrzbskjzxjgihqrzc.supabase.co"
KEY_BASE = "sb_publishable_B8SRZbxZV6IldEkpfnKsWg_bLfg1MUE"

conn = st.connection("supabase", type=SupabaseConnection, url=URL_BASE, key=KEY_BASE)
supabase = conn.client

# =========================================
# SESIÓN
# =========================================
if 'user' not in st.session_state:
    st.session_state.user = None

# =========================================
# 🎨 DISEÑO PREMIUM (OPTIMIZADO PARA CELULAR)
# =========================================
st.markdown("""
<style>

/* Fondo elegante */
.stApp {
    background: linear-gradient(180deg, #020617, #0F172A);
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #020617;
}

/* Botones */
.stButton>button {
    background: linear-gradient(90deg, #6366F1, #8B5CF6);
    color: white;
    border-radius: 8px;
    font-weight: bold;
}

/* Cards estilo premium */
.card {
    background: linear-gradient(145deg, #111827, #1F2937);
    padding: 15px;
    border-radius: 12px;
    margin-bottom: 15px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.4);
}

/* Hover suave */
.card:hover {
    transform: scale(1.01);
    transition: 0.2s;
}

/* Texto */
h1, h2, h3, p {
    color: #F9FAFB;
}

/* Links */
a {
    color: #60A5FA;
    text-decoration: none;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# LOGIN
# =========================================
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
            st.subheader("Crea tu cuenta de Negocio")
            new_email = st.text_input("Correo Electrónico", key="reg_email")
            new_password = st.text_input("Contraseña", type="password", key="reg_pass")
            
            # --- NUEVOS CAMPOS PARA TU DATA ---
            full_name = st.text_input("Tu Nombre Completo")
            biz_name = st.text_input("Nombre de tu Negocio (Batidas el sabor, etc.)")
            biz_type = st.selectbox("Tipo de Negocio", ["Dealer", "Inmobiliaria", "Electromuebles", "Equipos tecnológicos", "Otro"])
            
            if st.button("Crear Cuenta"):
                try:
                    # 1. Creamos el usuario en Auth
                    res = supabase.auth.sign_up({"email": new_email, "password": new_password})
                    
                    if res.user:
                        # 2. Guardamos sus datos en la tabla 'profiles' que acabas de crear
                        user_id = res.user.id
                        profile_data = {
                            "id": user_id,
                            "full_name": full_name,
                            "business_name": biz_name,
                            "business_type": biz_type,
                            "plan": "ninguno",
                            "status": "pendiente"
                        }
                        supabase.table("profiles").insert(profile_data).execute()
                        st.success("¡Cuenta creada! Ahora inicia sesión para elegir tu plan.")
                except Exception as e:
                    st.error(f"Error en registro: {e}")

# =========================================
# 🚀 APP PRINCIPAL (CON MURO DE PAGO)
# =========================================

if st.session_state.user is None:
    st.title("🚀 PREGÓN AI")
    st.subheader("Sistema inteligente de captación de clientes")
    st.info("Inicia sesión para continuar")
    login_form()

else:
    # 1. BUSCAR EL PERFIL DEL USUARIO EN LA TABLA QUE CREASTE
    try:
        user_id = st.session_state.user.id
        profile_res = supabase.table("profiles").select("*").eq("id", user_id).single().execute()
        profile = profile_res.data
    except Exception:
        profile = None

    # 2. VERIFICAR SI EL USUARIO ESTÁ ACTIVO O PENDIENTE
    if profile and profile.get("status") == "pendiente":
        st.title(f"¡Bienvenido, {profile.get('full_name', 'Emprendedor')}! 👋")
        st.warning("🔒 Tu cuenta está en espera de activación.")
        
        st.subheader("Elige un Plan para desbloquear tu Radar:")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""<div class="card"><h3>🛡️ BÁSICO</h3><p>RD$ 500 / mes</p><p>1 Cuenta propia</p></div>""", unsafe_allow_html=True)
            st.button("Elegir Básico", key="p1")
        with col2:
            st.markdown("""<div class="card"><h3>🔥 PRO</h3><p>RD$ 1,500 / mes</p><p>5 Cuentas Competencia</p></div>""", unsafe_allow_html=True)
            st.button("Elegir Pro", key="p2")
        with col3:
            st.markdown("""<div class="card"><h3>🦅 ELITE</h3><p>RD$ 3,500 / mes</p><p>Radar Ilimitado</p></div>""", unsafe_allow_html=True)
            st.button("Elegir Elite", key="p3")
            
        st.divider()
        st.info("Una vez elijas, envía el comprobante de pago para activar tu acceso inmediato.")
        st.link_button("📲 Enviar Comprobante (WhatsApp)", "https://wa.me/tu_numero_aqui")
        
        if st.sidebar.button("Cerrar Sesión"):
            supabase.auth.sign_out()
            st.session_state.user = None
            st.rerun()

    elif profile and profile.get("status") == "activo":
        # =========================================
        # DASHBOARD REAL (SOLO PARA ACTIVOS)
        # =========================================
        st.sidebar.title("🚀 PREGÓN AI")
        st.sidebar.write(f"🏢 **{profile.get('business_name', 'Mi Negocio')}**")
        st.sidebar.write(f"👤 {st.session_state.user.email}")

        menu = st.sidebar.selectbox("Menú", ["Dashboard", "Radar", "Pagos"])

        if st.sidebar.button("Cerrar sesión"):
            supabase.auth.sign_out()
            st.session_state.user = None
            st.rerun()

        if menu == "Dashboard":
            st.title("📊 Panel de Leads en Vivo")
            try:
                res = supabase.from_("leads").select("*").eq("owner_id", user_id).execute()
                data = res.data if res.data else []
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Leads Detectados", len(data))
                col2.metric("Plan", profile.get("plan", "Básico").upper())
                col3.metric("Sistema", "Online")
                st.divider()

                if data:
                    for lead in data:
                        st.markdown(f"""
                        <div class="card">
                            <h3>👤 @{lead.get('username','usuario')}</h3>
                            <p>💬 {lead.get('comment_text','Sin comentario')}</p>
                            <p>🔥 Intención: {round(lead.get('intent_score',0)*100)}%</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("Aún no hay leads detectados.")
            except Exception as e:
                st.error(f"Error cargando leads: {e}")

        elif menu == "Radar":
            st.title("📡 Configurar Radar")
            with st.form("radar"):
                cuenta = st.text_input("Cuenta de Instagram (@usuario)")
                if st.form_submit_button("Activar"):
                    supabase.table("radar_config").insert({
                        "owner_id": user_id,
                        "cuenta_instagram": cuenta,
                        "esta_activo": True
                    }).execute()
                    st.success(f"Radar activado para {cuenta}")

        elif menu == "Pagos":
            st.title("💳 Mi Suscripción")
            st.write(f"Tu plan actual es: **{profile.get('plan', 'Ninguno').upper()}**")
            st.info("Para renovar o cambiar de plan, contáctanos.")
