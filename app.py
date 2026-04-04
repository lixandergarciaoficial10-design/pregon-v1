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
# 🎨 DISEÑO PREMIUM
# =========================================
st.markdown("""
<style>
.stApp { background: linear-gradient(180deg, #020617, #0F172A); }
[data-testid="stSidebar"] { background-color: #020617; }
.stButton>button {
    background: linear-gradient(90deg, #6366F1, #8B5CF6);
    color: white; border-radius: 8px; font-weight: bold; width: 100%;
}
.card {
    background: linear-gradient(145deg, #111827, #1F2937);
    padding: 20px; border-radius: 15px; margin-bottom: 20px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.5); border: 1px solid #374151;
}
.card:hover { border-color: #6366F1; transform: translateY(-2px); transition: 0.3s; }
h1, h2, h3, p { color: #F9FAFB; }
</style>
""", unsafe_allow_html=True)

# =========================================
# FUNCIONES DE INTERFAZ
# =========================================
def login_form():
    with st.sidebar:
        st.title("🔐 Acceso")
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
                    st.error(f"Error: {e}")

        with tab2:
            st.subheader("Nuevo Negocio")
            new_email = st.text_input("Email", key="reg_email")
            new_password = st.text_input("Contraseña", type="password", key="reg_pass")
            full_name = st.text_input("Nombre Completo")
            biz_name = st.text_input("Nombre del Negocio")
            biz_type = st.selectbox("Rubro", ["Dealer", "Inmobiliaria", "Tecnología", "Otro"])
            
            if st.button("Crear Cuenta"):
                try:
                    res = supabase.auth.sign_up({"email": new_email, "password": new_password})
                    if res.user:
                        user_id = res.user.id
                        supabase.table("profiles").insert({
                            "id": user_id, "full_name": full_name,
                            "business_name": biz_name, "business_type": biz_type,
                            "plan": "ninguno", "status": "pendiente"
                        }).execute()
                        st.success("¡Cuenta creada! Inicia sesión.")
                except Exception as e:
                    st.error(f"Error: {e}")

# =========================================
# LÓGICA PRINCIPAL
# =========================================
if st.session_state.user is None:
    st.title("🚀 PREGÓN AI")
    st.subheader("Tu radar inteligente de ventas")
    login_form()
else:
    user_id = st.session_state.user.id
    try:
        profile = supabase.table("profiles").select("*").eq("id", user_id).single().execute().data
    except:
        profile = None

    if profile and profile.get("status") == "pendiente":
        st.title(f"Hola, {profile.get('full_name')} 👋")
        st.warning("Cuenta en espera de activación.")
        if st.button("🔄 ACTUALIZAR ACCESO"): st.rerun()

        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown('<div class="card"><h3>Básico</h3><p>RD$ 500</p></div>', unsafe_allow_html=True)
            if st.button("Elegir Básico"):
                supabase.table("profiles").update({"plan": "basico"}).eq("id", user_id).execute()
                st.success("Plan solicitado.")
        with c2:
            st.markdown('<div class="card"><h3>Pro</h3><p>RD$ 1,500</p></div>', unsafe_allow_html=True)
            if st.button("Elegir Pro"):
                supabase.table("profiles").update({"plan": "pro"}).eq("id", user_id).execute()
        with c3:
            st.markdown('<div class="card"><h3>Elite</h3><p>RD$ 3,500</p></div>', unsafe_allow_html=True)
            if st.button("Elegir Elite"):
                supabase.table("profiles").update({"plan": "elite"}).eq("id", user_id).execute()
        
        st.divider()
        st.link_button("📲 Confirmar Pago vía WhatsApp", "https://wa.me/1809XXXXXXX")

    elif profile and profile.get("status") == "activo":
        st.sidebar.title("🚀 PREGÓN AI")
        st.sidebar.write(f"🏢 **{profile.get('business_name')}**")
        menu = st.sidebar.selectbox("Menú", ["Dashboard", "Radar", "Suscripción"])

        if st.sidebar.button("Cerrar sesión"):
            supabase.auth.sign_out(); st.session_state.user = None; st.rerun()

        if menu == "Dashboard":
            st.title("📊 Panel de Leads")
            res_leads = supabase.table("leads").select("*").eq("owner_id", user_id).execute()
            data = res_leads.data if res_leads.data else []
            
            col_m1, col_m2 = st.columns(2)
            col_m1.metric("Leads Totales", len(data))
            col_m2.metric("Plan Actual", profile.get("plan").upper())

            if data:
                for lead in data:
                    # Nos aseguramos de que el score sea un número real (decimal)
                    try:
                        raw_score = float(lead.get('score_ia', 0))
                    except:
                        raw_score = 0.0
                        
                    st.markdown(f"""
                    <div class="card">
                        <h3>👤 @{lead.get('usuario_ig', 'usuario')}</h3>
                        <p>🚗 <b>Interés:</b> {lead.get('vehiculo_interes', 'N/A')}</p>
                        <p>💬 {lead.get('comentario', 'Sin comentario')}</p>
                        <p>🔥 <b>Score IA:</b> {int(raw_score * 100)}%</p>
                    </div>
                    """, unsafe_allow_html=True)
                    
            else:
                st.info("Sin leads nuevos por ahora.")

        elif menu == "Radar":
            st.title("📡 Configuración del Radar")
            # ... Lógica de radar igual a la anterior pero limpia ...
            st.write("Agrega cuentas de Instagram para monitorear.")
            with st.form("radar_f"):
                c_ig = st.text_input("Usuario de Instagram")
                if st.form_submit_button("Activar"):
                    supabase.table("radar_config").insert({"owner_id": user_id, "cuenta_instagram": c_ig}).execute()
                    st.success("Radar activo."); st.rerun()

        elif menu == "Suscripción":
            st.title("💳 Mi suscripción")
            st.success(f"Tu plan {profile.get('plan').upper()} está activo.")
