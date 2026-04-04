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
        
        # MENÚ CON LA NUEVA OPCIÓN
        menu = st.sidebar.selectbox("Menú", ["Dashboard", "Radar", "Laboratorio IA", "Suscripción"])

        if st.sidebar.button("Cerrar sesión"):
            supabase.auth.sign_out()
            st.session_state.user = None
            st.rerun()

        if menu == "Dashboard":
            st.title("📊 Panel de Leads")
            res_leads = supabase.table("leads").select("*").eq("owner_id", user_id).execute()
            data = res_leads.data if res_leads.data else []
            
            col_m1, col_m2 = st.columns(2)
            col_m1.metric("Leads Totales", len(data))
            col_m2.metric("Plan Actual", profile.get("plan").upper())

            if data:
                for lead in data:
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
            st.title("📡 Radar de Competencia (Automático)")
            st.info("Aquí monitoreamos las cuentas de los dealers que tú elijas.")
            
            # 1. EL FORMULARIO PARA AGREGAR CUENTAS
            with st.expander("➕ Agregar Cuenta al Radar"):
                col1, col2 = st.columns([1, 2])
                with col1:
                    red_social = st.selectbox("Plataforma", ["Instagram", "TikTok"])
                with col2:
                    cuenta_id = st.text_input("Nombre de Usuario (ej: @dealer_perez):")
                
                if st.button("Guardar en Radar"):
                    if cuenta_id:
                        # Guardamos la cuenta en Supabase para vigilarla siempre
                        supabase.table("radar_config").insert({
                            "owner_id": user_id,
                            "plataforma": red_social,
                            "cuenta_objetivo": cuenta_id.replace("@", "")
                        }).execute()
                        st.success(f"Vigilando a {cuenta_id} en {red_social}")
                    else:
                        st.error("Pon el nombre de la cuenta.")

            st.divider()

            # 2. EL BOTÓN MÁGICO DE SINCRONIZACIÓN
            st.subheader("🔄 Sincronización en Tiempo Real")
            if st.button("🚀 ESCANEAR TODAS LAS CUENTAS AHORA"):
                with st.spinner("El Vigilante está barriendo las redes... Limpiando leads..."):
                    # LLAMAMOS AL VIGILANTE
                    from vigilante import espiar_instagram, espiar_tiktok, limpiar_y_calificar
                    
                    # Buscamos qué cuentas tiene este cliente en su Radar
                    mis_cuentas = supabase.table("radar_config").select("*").eq("owner_id", user_id).execute()
                    
                    total_leads = 0
                    for fila in mis_cuentas.data:
                        plataforma = fila['plataforma']
                        user_target = fila['cuenta_objetivo']
                        
                        # El Vigilante hace su trabajo
                        if plataforma == "Instagram":
                            datos = espiar_instagram(user_target)
                        else:
                            datos = espiar_tiktok(user_target)
                        
                        # Supongamos que 'datos' trae los comentarios (ajustado a tus APIs)
                        leads_encontrados = limpiar_y_calificar(datos, plataforma)
                        
                        # GUARDAR SOLO LOS LEADS LIMPIOS EN SUPABASE
                        for lead in leads_encontrados:
                            supabase.table("leads").insert({
                                "owner_id": user_id,
                                "usuario_ig": lead['usuario_ig'],
                                "comentario": lead['comentario'],
                                "score_ia": lead['score_ia'],
                                "vehiculo_interes": lead['vehiculo_interes'],
                                "fuente": lead['fuente']
                            }).execute()
                            total_leads += 1
                    
                    if total_leads > 0:
                        st.success(f"¡Éxito! Encontramos {total_leads} leads calientes y limpios.")
                        st.balloons()
                    else:
                        st.warning("Revisamos todo, pero no había comentarios con intención de compra hoy.")

            # 3. MOSTRAR LAS CUENTAS QUE YA ESTÁN EN EL RADAR
            st.subheader("👀 Cuentas bajo vigilancia")
            mis_cuentas_view = supabase.table("radar_config").select("*").eq("owner_id", user_id).execute()
            if mis_cuentas_view.data:
                for c in mis_cuentas_view.data:
                    st.write(f"✅ {c['plataforma']}: **@{c['cuenta_objetivo']}**")
            else:
                st.write("Aún no tienes cuentas en el Radar. Agrega la primera arriba.")

        elif menu == "Laboratorio IA":
            st.title("🧠 Probador de Inteligencia (Groq)")
            st.info("Escribe un comentario aquí para ver cómo la IA lo analiza antes de guardarlo.")
            
            # Importamos tu otro archivo
            try:
                from ia_engine import analizar_lead
                
                test_input = st.text_input("Escribe un comentario de prueba:")
                if st.button("Analizar ahora"):
                    if test_input:
                        with st.spinner("Llama 3 analizando..."):
                            resultado = analizar_lead(test_input)
                            st.json(resultado)
                            
                            st.divider()
                            st.subheader("Vista previa en el Dashboard:")
                            st.markdown(f"""
                            <div class="card">
                                <h3>👤 @usuario_ejemplo</h3>
                                <p>🚗 <b>Vehículo:</b> {resultado.get('vehiculo_interes')}</p>
                                <p>🔥 <b>Score IA:</b> {int(resultado.get('score_ia', 0)*100)}%</p>
                            </div>
                            """, unsafe_allow_html=True)
                    else:
                        st.warning("Escribe algo para analizar.")
            except Exception as e:
                st.error(f"Error al cargar el cerebro: {e}")

        elif menu == "Suscripción":
            st.title("💳 Mi suscripción")
            st.success(f"Tu plan {profile.get('plan').upper()} está activo.")
