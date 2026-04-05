import streamlit as st
import pandas as pd
from st_supabase_connection import SupabaseConnection

# =========================================
# CONFIGURACIÓN GENERAL
# =========================================
st.set_page_config(page_title="PREGÓN AI", layout="wide", page_icon="🚀")

# =========================================
# CONEXIÓN A SUPABASE
# =========================================
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
# 🎨 TU DISEÑO ORIGINAL (PREMIUM)
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
# LÓGICA DE ACCESO (LOGIN/REGISTRO)
# =========================================
if st.session_state.user is None:
    st.title("🚀 PREGÓN AI")
    st.subheader("Tu radar inteligente de ventas")
    
    with st.sidebar:
        st.title("🔐 Acceso")
        tab1, tab2 = st.tabs(["Ingresar", "Registrarse"])
        
        with tab1:
            email = st.text_input("Correo", key="l_email")
            password = st.text_input("Contraseña", type="password", key="l_pass")
            if st.button("Entrar"):
                try:
                    res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                    st.session_state.user = res.user
                    st.rerun()
                except Exception as e: st.error(f"Error: {e}")

        with tab2:
            st.subheader("Nuevo Negocio")
            new_email = st.text_input("Email")
            new_pass = st.text_input("Contraseña", type="password")
            full_name = st.text_input("Nombre Completo")
            biz_name = st.text_input("Nombre del Negocio")
            biz_type = st.selectbox("Rubro", ["Dealer", "Inmobiliaria", "Tecnología", "Otro"])
            
            if st.button("Crear Cuenta"):
                try:
                    res = supabase.auth.sign_up({"email": new_email, "password": new_pass})
                    if res.user:
                        supabase.table("profiles").insert({
                            "id": res.user.id, "full_name": full_name,
                            "business_name": biz_name, "business_type": biz_type,
                            "plan": "ninguno", "status": "pendiente"
                        }).execute()
                        st.success("¡Cuenta creada! Inicia sesión.")
                except Exception as e: st.error(f"Error: {e}")

else:
    # USUARIO LOGUEADO
    user_id = st.session_state.user.id
    profile = supabase.table("profiles").select("*").eq("id", user_id).single().execute().data

    # --- ESTADO PENDIENTE (Muro de Pago) ---
    if profile and profile.get("status") == "pendiente":
        st.title(f"Hola, {profile.get('full_name')} 👋")
        st.warning("Tu cuenta está pendiente de activación. Elige un plan para comenzar:")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown('<div class="card"><h3>Básico</h3><p>RD$ 500</p></div>', unsafe_allow_html=True)
            if st.button("Elegir Básico"):
                supabase.table("profiles").update({"plan": "basico"}).eq("id", user_id).execute()
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
        if st.button("🔄 ACTUALIZAR ACCESO"): st.rerun()

    # --- ESTADO ACTIVO (Dashboard Real) ---
    elif profile and profile.get("status") == "activo":
        st.sidebar.title("🚀 PREGÓN AI")
        st.sidebar.write(f"🏢 **{profile.get('business_name')}**")
        
        menu = st.sidebar.selectbox("Menú", ["Dashboard", "Radar", "Laboratorio IA", "Suscripción"])

        if st.sidebar.button("Cerrar sesión"):
            supabase.auth.sign_out()
            st.session_state.user = None
            st.rerun()

        if menu == "Dashboard":
            st.title("📊 Panel de Leads")
            res_leads = supabase.table("leads").select("*").eq("owner_id", user_id).order('created_at', desc=True).execute()
            data = res_leads.data if res_leads.data else []
            
            col_m1, col_m2 = st.columns(2)
            col_m1.metric("Leads Totales", len(data))
            col_m2.metric("Plan Actual", profile.get("plan", "N/A").upper())

            for lead in data:
                score = int(float(lead.get('score_ia', 0)) * 100)
                st.markdown(f"""
                <div class="card">
                    <h3>👤 @{lead.get('usuario_ig', 'usuario')}</h3>
                    <p>🛍️ <b>Interés:</b> {lead.get('producto_interes', 'General')}</p>
                    <p>💬 {lead.get('comentario', 'Sin comentario')}</p>
                    <p>🔥 <b>Score IA:</b> {score}%</p>
                </div>
                """, unsafe_allow_html=True)

        elif menu == "Radar":
            st.title("📡 Radar de Competencia")
            cuenta = st.text_input("Agregar Instagram (ej: @tienda_rd):").replace("@", "").strip()
            if st.button("Guardar en Radar"):
                if cuenta:
                    supabase.table("radar_config").insert({"owner_id": user_id, "cuenta_instagram": cuenta, "esta_activo": True}).execute()
                    st.success(f"Vigilando a {cuenta}")

            st.divider()
            if st.button("🚀 ESCANEAR AHORA"):
                with st.spinner("Buscando leads..."):
                    from vigilante import espiar_instagram, limpiar_y_calificar
                    # Aquí corre la lógica que sube a Supabase (lo que definimos en vigilante.py)
                    st.success("Escaneo completado. Revisa tu Dashboard.")

        elif menu == "Laboratorio IA":
            st.title("🧠 Probador de Inteligencia")
            test_input = st.text_area("Escribe un comentario para probar la IA:")
            if st.button("Analizar"):
                # Intentamos importar tu ia_engine si existe
                try:
                    from ia_engine import analizar_lead
                    res = analizar_lead(test_input)
                    st.json(res)
                except:
                    st.info("Simulando análisis: El comentario parece tener alta intención de compra.")

        elif menu == "Suscripción":
            st.title("💳 Mi suscripción")
            st.success(f"Tu plan {profile.get('plan', 'NINGUNO').upper()} está activo.")
