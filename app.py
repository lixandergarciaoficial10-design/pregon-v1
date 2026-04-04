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
            biz_name = st.text_input("Nombre del Negocio (Dealer, etc.)")
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
# APP PRINCIPAL
# =========================================
if st.session_state.user is None:
    st.title("🚀 PREGÓN AI")
    st.subheader("Sistema inteligente de captación de clientes")
    st.info("Inicia sesión para continuar")
    login_form()

else:
    st.sidebar.title("🚀 PREGÓN AI")
    st.sidebar.write(f"👤 {st.session_state.user.email}")

    menu = st.sidebar.selectbox("Menú", ["Dashboard", "Radar", "Pagos"])

    if st.sidebar.button("Cerrar sesión"):
        supabase.auth.sign_out()
        st.session_state.user = None
        st.rerun()

    # =========================================
    # DASHBOARD (AQUÍ ESTÁ EL FLOW DURO)
    # =========================================
    if menu == "Dashboard":

        st.title("📊 Panel de Leads en Vivo")

        try:
            res = supabase.from_("leads").select("*").eq(
                "owner_id", st.session_state.user.id
            ).execute()

            data = res.data if res.data else []

            # ===============================
            # MÉTRICAS
            # ===============================
            col1, col2, col3 = st.columns(3)
            col1.metric("Leads Detectados", len(data))
            col2.metric("Estado", "Activo")
            col3.metric("Sistema", "Online")

            st.divider()

            # ===============================
            # LEADS VISUALES (LO IMPORTANTE)
            # ===============================
            if data:

                for lead in data:

                    st.markdown(f"""
                    <div class="card">
                        <h3>👤 @{lead.get('username','usuario')}</h3>
                        <p>💬 {lead.get('comment_text','Sin comentario')}</p>
                        <p>🔥 Intención: {round(lead.get('intent_score',0)*100)}%</p>
                        <p>⏱ {lead.get('created_at','')}</p>
                    </div>
                    """, unsafe_allow_html=True)

                    colA, colB = st.columns(2)

                    # 👤 PERFIL
                    if lead.get("profile_url"):
                        colA.link_button("Ver Perfil", lead["profile_url"])

                    # 📌 POST
                    if lead.get("post_url"):
                        colB.link_button("Ver Publicación", lead["post_url"])

            else:
                st.warning("Aún no hay leads. El sistema empezará a detectarlos pronto.")

        except Exception as e:
            st.error(f"Error: {e}")

    # =========================================
    # RADAR
    # =========================================
    elif menu == "Radar":

        st.title("📡 Activar Radar")

        with st.form("radar"):
            cuenta = st.text_input("Cuenta a monitorear (@dealer)")
            submit = st.form_submit_button("Activar")

            if submit:
                try:
                    supabase.table("radar_config").insert({
                        "owner_id": st.session_state.user.id,
                        "cuenta_instagram": cuenta,
                        "esta_activo": True
                    }).execute()

                    st.success(f"Radar activado para {cuenta}")
                    st.info("El sistema comenzará a analizar comentarios automáticamente.")

                except Exception as e:
                    st.error(f"Error: {e}")

    # =========================================
    # PAGOS
    # =========================================
    elif menu == "Pagos":

        st.title("💳 Activar Plan")

        st.markdown("""
        ### Plan Básico RD$2,000 / mes

        ✔ Leads en tiempo real  
        ✔ Acceso completo al sistema  
        ✔ Soporte básico  

        ---
        """)

        st.info("Para activar, contáctanos por WhatsApp.")

        st.link_button("💬 Activar ahora", "https://wa.me/1809XXXXXXX")
