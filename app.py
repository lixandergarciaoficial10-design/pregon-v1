import streamlit as st
import pandas as pd
from st_supabase_connection import SupabaseConnection
import time

# 1. CONFIGURACIÓN E INYECCIÓN DE CSS
st.set_page_config(page_title="PREGÓN AI", layout="wide", page_icon="🚀")

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
h1, h2, h3, p, b { color: #F9FAFB; }
</style>
""", unsafe_allow_html=True)

# 2. CONEXIÓN SEGURA A SUPABASE (Usando Secrets)
try:
    URL_BASE = st.secrets["SUPABASE_URL"]
    KEY_BASE = st.secrets["SUPABASE_KEY"]
    conn = st.connection("supabase", type=SupabaseConnection, url=URL_BASE, key=KEY_BASE)
    supabase = conn.client
except Exception as e:
    st.error("Error crítico: Configura SUPABASE_URL y SUPABASE_KEY en los Secrets de Streamlit.")
    st.stop()

# 3. MANEJO DE SESIÓN
if 'user' not in st.session_state:
    st.session_state.user = None

# --- FLUJO DE LOGIN / REGISTRO ---
if st.session_state.user is None:
    st.title("🚀 PREGÓN AI")
    st.subheader("Tu radar inteligente de ventas")
    
    with st.sidebar:
        st.title("🔐 Acceso")
        tab1, tab2 = st.tabs(["Ingresar", "Registrarse"])
        
        with tab1:
            email = st.text_input("Correo", key="l_email")
            pw = st.text_input("Contraseña", type="password", key="l_pw")
            if st.button("Entrar"):
                try:
                    res = supabase.auth.sign_in_with_password({"email": email, "password": pw})
                    st.session_state.user = res.user
                    st.rerun()
                except Exception as e: st.error(f"Fallo: {e}")
        
        with tab2:
            st.subheader("Nuevo Negocio")
            n_email = st.text_input("Email")
            n_pw = st.text_input("Contraseña", type="password")
            f_name = st.text_input("Nombre Completo")
            b_name = st.text_input("Nombre del Negocio")
            if st.button("Crear Cuenta"):
                try:
                    res = supabase.auth.sign_up({"email": n_email, "password": n_pw})
                    if res.user:
                        supabase.table("profiles").insert({
                            "id": res.user.id, "full_name": f_name,
                            "business_name": b_name, "status": "pendiente", "plan": "ninguno"
                        }).execute()
                        st.success("¡Cuenta creada! Inicia sesión.")
                except Exception as e: st.error(f"Error: {e}")

else:
    # 4. LÓGICA DE USUARIO LOGUEADO
    user_id = st.session_state.user.id
    # Obtenemos perfil actualizado
    profile_res = supabase.table("profiles").select("*").eq("id", user_id).execute()
    profile = profile_res.data[0] if profile_res.data else None

    # --- MURO DE PAGO (Pendiente) ---
    if profile and profile.get("status") == "pendiente":
        st.title(f"Hola, {profile.get('full_name')} 👋")
        st.warning("Selecciona un plan para activar tu radar:")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown('<div class="card"><h3>Básico</h3><p>RD$ 500</p></div>', unsafe_allow_html=True)
            if st.button("Elegir Básico"):
                supabase.table("profiles").update({"plan": "basico"}).eq("id", user_id).execute()
                st.rerun()
        with c2:
            st.markdown('<div class="card"><h3>Pro</h3><p>RD$ 1,500</p></div>', unsafe_allow_html=True)
            if st.button("Elegir Pro"):
                supabase.table("profiles").update({"plan": "pro"}).eq("id", user_id).execute()
                st.rerun()
        with c3:
            st.markdown('<div class="card"><h3>Elite</h3><p>RD$ 3,500</p></div>', unsafe_allow_html=True)
            if st.button("Elegir Elite"):
                supabase.table("profiles").update({"plan": "elite"}).eq("id", user_id).execute()
                st.rerun()
        st.divider()
        st.link_button("📲 Confirmar Pago vía WhatsApp", f"https://wa.me/1809XXXXXXX?text=Hola, quiero activar mi plan en PregonAI. Mi correo es {profile.get('email')}")
        if st.button("🔄 YA PAGUÉ / RECARGAR"): st.rerun()

    # --- DASHBOARD ACTIVO ---
    elif profile and profile.get("status") == "activo":
        st.sidebar.title("🚀 PREGÓN AI")
        menu = st.sidebar.selectbox("Menú", ["Dashboard", "Radar", "Laboratorio IA", "Suscripción"])
        
        if st.sidebar.button("Cerrar sesión"):
            supabase.auth.sign_out()
            st.session_state.user = None
            st.rerun()

        if menu == "Dashboard":
            st.title("📊 Panel de Leads")
            res_leads = supabase.table("leads").select("*").eq("owner_id", user_id).order('created_at', desc=True).execute()
            leads = res_leads.data if res_leads.data else []
            
            col_a, col_b = st.columns(2)
            col_a.metric("Leads Totales", len(leads))
            col_b.metric("Plan", profile.get("plan", "").upper())

            if leads:
                for l in leads:
                    sc = int(float(l.get('score_ia', 0)) * 100)
                    st.markdown(f"""
                    <div class="card">
                        <h3>👤 @{l.get('usuario_ig')}</h3>
                        <p>🛍️ <b>Interés:</b> {l.get('producto_interes', 'General')}</p>
                        <p>💬 {l.get('comentario')}</p>
                        <p>🔥 <b>Score IA:</b> {sc}%</p>
                        <small>📅 {l.get('created_at')[:10]}</small>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("Dashboard vacío. Ve al Radar y pulsa Escanear para buscar clientes.")

        elif menu == "Radar":
            st.title("📡 Radar de Competencia")
            cuenta = st.text_input("Instagram de la competencia (sin @):").strip()
            if st.button("➕ Agregar al Radar"):
                if cuenta:
                    supabase.table("radar_config").insert({"owner_id": user_id, "cuenta_instagram": cuenta, "esta_activo": True}).execute()
                    st.success(f"Vigilando a {cuenta}")
            
            st.divider()
            if st.button("🚀 INICIAR ESCANEO CON SCRAPE.DO"):
                with st.spinner("Scrape.do está saltando los bloqueos de Instagram..."):
                    # Importamos motor de extracción
                    from vigilante import espiar_instagram, limpiar_y_calificar
                    
                    cuentas_radar = supabase.table("radar_config").select("*").eq("owner_id", user_id).execute().data
                    nuevos = 0
                    
                    for c in cuentas_radar:
                        # Extraemos usando Scrape.do
                        raw = espiar_instagram(c['cuenta_instagram'])
                        # Calificamos con IA
                        calificados = limpiar_y_calificar(raw, "Instagram")
                        
                        for item in calificados:
                            try:
                                supabase.table("leads").insert({
                                    "owner_id": user_id, 
                                    "usuario_ig": item['usuario_ig'],
                                    "comentario": item['comentario'], 
                                    "score_ia": item['score_ia'],
                                    "producto_interes": item.get('producto_interes', 'General'), 
                                    "fuente": "Scrape.do"
                                }).execute()
                                nuevos += 1
                            except:
                                pass # Evita duplicados
                                
                    if nuevos > 0:
                        st.success(f"¡Éxito! Se encontraron {nuevos} leads nuevos.")
                        st.balloons()
                        time.sleep(2)
                        st.rerun()
                    else:
                        st.warning("No se detectaron leads nuevos. Intenta con otra cuenta.")

        elif menu == "Laboratorio IA":
            st.title("🧠 Laboratorio de Inteligencia")
            from ia_engine import analizar_lead
            
            txt = st.text_area("Pega un comentario aquí para ver qué piensa la IA:")
            if st.button("Analizar ahora"):
                if txt:
                    resultado = analizar_lead(txt)
                    st.subheader("Resultado:")
                    st.json(resultado)
                    
                    score = int(resultado['score_ia'] * 100)
                    if score > 70:
                        st.success(f"🔥 Cliente Caliente: {score}% de probabilidad de compra.")
                    else:
                        st.info(f"❄️ Cliente Frío: {score}% de probabilidad.")
                else:
                    st.warning("Escribe algo primero.")

        elif menu == "Suscripción":
            st.title("💳 Mi Suscripción")
            st.markdown(f"""
            <div class="card">
                <h3>Detalles del Plan</h3>
                <p>🏢 <b>Negocio:</b> {profile.get('business_name')}</p>
                <p>💎 <b>Plan Actual:</b> {profile.get('plan', '').upper()}</p>
                <p>✅ <b>Estado:</b> ACTIVO</p>
            </div>
            """, unsafe_allow_html=True)
