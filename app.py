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
# 🚀 APP PRINCIPAL (CON MURO DE PAGO Y LÓGICA DE ACTIVACIÓN)
# =========================================

if st.session_state.user is None:
    st.title("🚀 PREGÓN AI")
    st.subheader("Sistema inteligente de captación de clientes")
    st.info("Inicia sesión para continuar")
    login_form()

else:
    # 1. BUSCAR EL PERFIL DEL USUARIO
    try:
        user_id = st.session_state.user.id
        # Consultamos directamente a la tabla profiles
        profile_res = supabase.table("profiles").select("*").eq("id", user_id).single().execute()
        profile = profile_res.data
    except Exception as e:
        st.error(f"Error cargando perfil: {e}")
        profile = None

    # 2. VERIFICAR SI EL USUARIO ESTÁ ACTIVO O PENDIENTE
    if profile and profile.get("status") == "pendiente":
        st.title(f"¡Bienvenido, {profile.get('full_name', 'Emprendedor')}! 👋")
        
        # BOTÓN CRÍTICO: Para refrescar la sesión después de pagar o cambiar en Supabase
        if st.button("🔄 YA PAGUÉ, ACTUALIZAR MI ACCESO"):
            st.rerun()

        st.warning("🔒 Tu cuenta está en espera de activación. Elige un plan y envía tu comprobante.")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""<div class="card"><h3>🛡️ BÁSICO</h3><p>RD$ 500 / mes</p></div>""", unsafe_allow_html=True)
            if st.button("Elegir Básico", key="plan_basico"):
                supabase.table("profiles").update({"plan": "basico"}).eq("id", user_id).execute()
                st.success("Plan Básico seleccionado. Envía el comprobante por WhatsApp.")

        with col2:
            st.markdown("""<div class="card"><h3>🔥 PRO</h3><p>RD$ 1,500 / mes</p></div>""", unsafe_allow_html=True)
            if st.button("Elegir Pro", key="plan_pro"):
                supabase.table("profiles").update({"plan": "pro"}).eq("id", user_id).execute()
                st.success("Plan Pro seleccionado. Envía el comprobante por WhatsApp.")

        with col3:
            st.markdown("""<div class="card"><h3>🦅 ELITE</h3><p>RD$ 3,500 / mes</p></div>""", unsafe_allow_html=True)
            if st.button("Elegir Elite", key="plan_elite"):
                supabase.table("profiles").update({"plan": "elite"}).eq("id", user_id).execute()
                st.success("Plan Elite seleccionado. Envía el comprobante por WhatsApp.")
            
        st.divider()
        st.info("Escríbenos para confirmar tu pago y activar tu radar hoy mismo.")
        st.link_button("📲 Enviar Comprobante (WhatsApp)", "https://wa.me/1809XXXXXXX") # Pon tu número real aquí
        
        if st.sidebar.button("Cerrar Sesión"):
            supabase.auth.sign_out()
            st.session_state.user = None
            st.rerun()

    elif profile and profile.get("status") == "activo":
        # =========================================
        # DASHBOARD REAL (ESTO SOLO SE VE SI STATUS == 'ACTIVO')
        # =========================================
        st.sidebar.title("🚀 PREGÓN AI")
        st.sidebar.write(f"🏢 **{profile.get('business_name', 'Mi Negocio')}**")
        st.sidebar.write(f"👤 {st.session_state.user.email}")

        menu = st.sidebar.selectbox("Menú", ["Dashboard", "Radar", "Suscripción"])

        if st.sidebar.button("Cerrar sesión"):
            supabase.auth.sign_out()
            st.session_state.user = None
            st.rerun()

        if menu == "Dashboard":
            st.title("📊 Panel de Leads en Vivo")
            try:
                # Filtrar leads que pertenezcan a este usuario
                res_leads = supabase.table("leads").select("*").eq("owner_id", user_id).execute()
                data = res_leads.data if res_leads.data else []
                
                c1, c2, c3 = st.columns(3)
                c1.metric("Leads", len(data))
                c2.metric("Plan", profile.get("plan", "N/A").upper())
                c3.metric("Estado", "ONLINE")
                st.divider()

                if data:
 for lead in data:
    st.markdown(f"""
    <div class="card">
        <h3>👤 @{lead.get('usuario_ig','usuario')}</h3>
        <p>🚗 Vehículo: {lead.get('vehiculo_interes','N/A')}</p>
        <p>💬 {lead.get('comentario','Sin comentario')}</p>
        <p>🔥 Intención: {round(lead.get('score_ia', 0) * 100)}%</p>
    </div>
    """, unsafe_allow_html=True)
                else:
                    st.info("Buscando leads... Tu radar está trabajando 24/7.")
            except Exception as e:
                st.error(f"Error al cargar datos: {e}")
       # ==================================================================================

        elif menu == "Radar":
            st.title("📡 Configuración del Radar")
            
            # 1. Definir límites según el plan
            limites = {
                "basico": 1,
                "estandar": 5,
                "pro": 15,
                "elite": 30,  # Asegúrate de incluir todos tus planes
                "ninguno": 0
            }
            
            plan_usuario = profile.get("plan", "ninguno").lower()
            limite_actual = limites.get(plan_usuario, 0)
            
            # 2. Contar cuántas cuentas ya tiene registradas
            res_conteo = supabase.table("radar_config").select("id", count="exact").eq("owner_id", user_id).execute()
            cuentas_actuales = res_conteo.count if res_conteo.count is not None else 0
            
            st.info(f"📊 Plan: **{plan_usuario.upper()}** | Cuentas: **{cuentas_actuales} / {limite_actual}**")

            # 3. Lógica del candado
            if cuentas_actuales >= limite_actual:
                st.error("🚫 Has alcanzado el límite de cuentas de tu plan.")
                st.warning("Sube de nivel para monitorear más competidores.")
            else:
                with st.form("nuevo_radar"):
                    cuenta = st.text_input("Usuario de Instagram (ej: @dealer_premium)")
                    if st.form_submit_button("Activar Monitoreo"):
                        if cuenta:
                            # Limpiamos el @ si el usuario lo pone
                            cuenta_limpia = cuenta.replace("@", "").strip()
                            supabase.table("radar_config").insert({
                                "owner_id": user_id,
                                "cuenta_instagram": cuenta_limpia,
                                "esta_activo": True
                            }).execute()
                            st.success(f"✅ Radar apuntado a @{cuenta_limpia}")
                            st.rerun()
                        else:
                            st.error("Escribe una cuenta válida.")

            # 4. Mostrar lista de cuentas actuales
            if cuentas_actuales > 0:
                st.divider()
                st.subheader("Tu Lista de Radar")
                res_lista = supabase.table("radar_config").select("*").eq("owner_id", user_id).execute()
                for r in res_lista.data:
                    st.write(f"📡 @{r['cuenta_instagram']}")

        elif menu == "Suscripción":
            st.title("💳 Mi Plan")
            st.success(f"Tu plan actual: **{profile.get('plan', 'Básico').upper()}**")
            st.write("Estado: **ACTIVO** ✅")
            st.info("Para mejorar tu plan o cancelar, contacta a soporte.")
