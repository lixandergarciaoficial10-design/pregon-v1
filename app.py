import streamlit as st
import pandas as pd
from st_supabase_connection import SupabaseConnection

# =========================================
# CONFIGURACIÓN GENERAL
# =========================================
st.set_page_config(page_title="PREGÓN AI", layout="wide", page_icon="🚀")

# =========================================
# CONEXIÓN A SUPABASE (SEGURA)
# =========================================
# Usamos st.secrets para que nadie te robe la base de datos
URL_BASE = st.secrets["SUPABASE_URL"]
KEY_BASE = st.secrets["SUPABASE_KEY"]

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
            biz_type = st.selectbox("Rubro", ["Dealer", "Inmobiliaria", "Otro"])
            
            if st.button("Crear Cuenta"):
                try:
                    res = supabase.auth.sign_up({"email": new_email, "password": new_password})
                    if res.user:
                        supabase.table("profiles").insert({
                            "id": res.user.id, "full_name": full_name,
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
    profile_res = supabase.table("profiles").select("*").eq("id", user_id).execute()
    profile = profile_res.data[0] if profile_res.data else None

    if profile and profile.get("status") == "activo":
        st.sidebar.title("🚀 PREGÓN AI")
        st.sidebar.write(f"🏢 **{profile.get('business_name')}**")
        
        menu = st.sidebar.selectbox("Menú", ["Dashboard", "Radar", "Suscripción"])

        if st.sidebar.button("Cerrar sesión"):
            supabase.auth.sign_out()
            st.session_state.user = None
            st.rerun()

        if menu == "Dashboard":
            st.title("📊 Panel de Leads")
            res_leads = supabase.table("leads").select("*").eq("owner_id", user_id).order('created_at', desc=True).execute()
            data = res_leads.data if res_leads.data else []
            
            c_m1, c_m2 = st.columns(2)
            c_m1.metric("Leads Totales", len(data))
            c_m2.metric("Plan", profile.get("plan", "N/A").upper())

            if data:
                for lead in data:
                    score = int(float(lead.get('score_ia', 0)) * 100)
                    st.markdown(f"""
                    <div class="card">
                        <h3>👤 @{lead.get('usuario_ig', 'usuario')}</h3>
                        <p>🛍️ <b>Interés:</b> {lead.get('producto_interes', 'General')}</p>
                        <p>💬 {lead.get('comentario', 'Sin comentario')}</p>
                        <p>🔥 <b>Calidad:</b> {score}%</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No hay leads aún. Ve al Radar y presiona Escanear.")

        elif menu == "Radar":
            st.title("📡 Radar de Competencia")
            
            with st.expander("➕ Agregar Cuenta"):
                cuenta = st.text_input("Usuario de Instagram:").replace("@", "").strip()
                if st.button("Vigilar Cuenta"):
                    if cuenta:
                        supabase.table("radar_config").insert({"owner_id": user_id, "cuenta_instagram": cuenta, "esta_activo": True}).execute()
                        st.success(f"Vigilando a {cuenta}")
                        st.rerun()

            st.divider()

            if st.button("🚀 ESCANEAR AHORA"):
                with st.spinner("Escaneando Instagram..."):
                    from vigilante import espiar_instagram, limpiar_y_calificar
                    
                    cuentas = supabase.table("radar_config").select("*").eq("owner_id", user_id).execute().data
                    nuevos = 0
                    
                    for c in cuentas:
                        target = c.get('cuenta_instagram')
                        raw = espiar_instagram(target)
                        calificados = limpiar_y_calificar(raw, "Instagram")
                        
                        for l in calificados:
                            try:
                                supabase.table("leads").insert({
                                    "owner_id": user_id,
                                    "usuario_ig": l['usuario_ig'],
                                    "comentario": l['comentario'],
                                    "score_ia": l['score_ia'],
                                    "producto_interes": l.get('vehiculo_interes', 'General'),
                                    "fuente": "Instagram"
                                }).execute()
                                nuevos += 1
                            except: pass
                    
                    if nuevos > 0:
                        st.success(f"¡Encontrados {nuevos} leads!")
                        st.balloons()
                    else:
                        st.warning("No hay comentarios nuevos con intención de compra.")

    else:
        st.title(f"Hola, {profile.get('full_name', 'Usuario')} 👋")
        st.warning("Cuenta pendiente de activación.")
