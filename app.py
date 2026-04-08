# ============================================
# 🚀 PREGÓN AI - APP FINAL PREMIUM
# ============================================

import streamlit as st
from database import guardar_leads, obtener_leads, verificar_demo, marcar_demo_usado
from scraper_tiktok import procesar_comentarios
from analisis_competencia import analizar_competencia, generar_insight
import plotly.express as px

# ============================================
# 🎨 CONFIGURACIÓN VISUAL
# ============================================

st.set_page_config(page_title="PREGÓN AI", layout="wide", page_icon="🚀")

st.markdown("""
<style>

/* ====== FONDO GENERAL ====== */
.stApp {
    background: linear-gradient(180deg, #F8FAFC 0%, #EEF2FF 100%);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}

/* ====== TITULOS ====== */
h1 {
    color: #0F172A;
    font-size: 42px;
    font-weight: 700;
    letter-spacing: -1px;
}

h2, h3 {
    color: #1E293B;
}

/* ====== TEXTO ====== */
p, label {
    color: #475569 !important;
    font-size: 15px;
}

/* ====== INPUTS ====== */
input, textarea {
    background: white !important;
    color: #0F172A !important;
    border-radius: 12px !important;
    border: 1px solid #E2E8F0 !important;
    padding: 10px !important;
    transition: all 0.2s ease;
}

input:focus, textarea:focus {
    border: 1px solid #6366F1 !important;
    box-shadow: 0px 0px 0px 3px rgba(99,102,241,0.2);
}

/* ====== BOTONES ====== */
.stButton > button {
    background: linear-gradient(135deg, #6366F1, #4F46E5);
    color: white;
    border-radius: 12px;
    padding: 10px 18px;
    font-weight: 600;
    border: none;
    transition: all 0.2s ease;
}

.stButton > button:hover {
    transform: translateY(-1px);
    box-shadow: 0px 6px 20px rgba(99,102,241,0.3);
}

/* ====== TARJETAS ====== */
.card {
    background: white;
    padding: 22px;
    border-radius: 18px;
    margin-bottom: 15px;
    border: 1px solid #E2E8F0;
    box-shadow: 0px 10px 30px rgba(0,0,0,0.05);
    transition: all 0.2s ease;
}

.card:hover {
    transform: translateY(-3px);
}

/* ====== MÉTRICAS ====== */
.metric {
    background: white;
    padding: 25px;
    border-radius: 18px;
    text-align: center;
    border: 1px solid #E2E8F0;
    box-shadow: 0px 6px 20px rgba(0,0,0,0.05);
}

/* ====== SIDEBAR ====== */
[data-testid="stSidebar"] {
    background: white !important;
    border-right: 1px solid #E2E8F0;
}

/* ====== SEPARADORES ====== */
hr {
    border: none;
    height: 1px;
    background: #E2E8F0;
    margin: 20px 0;
}

/* ====== ALERTAS ====== */
.stAlert {
    border-radius: 12px !important;
}

/* ====== SCROLL ====== */
::-webkit-scrollbar {
    width: 8px;
}
::-webkit-scrollbar-thumb {
    background: #CBD5F5;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# ============================================
# 🧠 SESIÓN
# ============================================

if "user_id" not in st.session_state:
    st.session_state.user_id = None

# ============================================
# 🔐 LOGIN
# ============================================

if st.session_state.user_id is None:

    st.title("🚀 PREGÓN AI")
    st.subheader("Detecta clientes listos para comprar en redes sociales")

    email = st.text_input("Correo electrónico")

    if st.button("Entrar"):
        if email:
            st.session_state.user_id = email
            st.rerun()
        else:
            st.warning("Introduce tu correo")

# ============================================
# 🧾 APP PRINCIPAL
# ============================================

else:

    user_id = st.session_state.user_id

    # SIDEBAR
    st.sidebar.title("🚀 PREGÓN AI")
    menu = st.sidebar.radio("Menú", ["Dashboard", "Escanear", "Análisis Competencia"])

    if st.sidebar.button("Cerrar sesión"):
        st.session_state.user_id = None
        st.rerun()

    # ========================================
    # 📊 DASHBOARD
    # ========================================
    if menu == "Dashboard":

        st.title("📊 Clientes Detectados")

        leads = obtener_leads(user_id)

        total = len(leads)
        calientes = len([l for l in leads if l["score_ia"] > 0.8])
        medios = len([l for l in leads if 0.5 <= l["score_ia"] <= 0.8])

        col1, col2, col3 = st.columns(3)

        col1.markdown(f"<div class='metric'><h2>{total}</h2><p>Total Leads</p></div>", unsafe_allow_html=True)
        col2.markdown(f"<div class='metric'><h2>{calientes}</h2><p>🔥 Calientes</p></div>", unsafe_allow_html=True)
        col3.markdown(f"<div class='metric'><h2>{medios}</h2><p>🧠 Interesados</p></div>", unsafe_allow_html=True)

        st.divider()

        if leads:
            for l in leads:
                score = int(l["score_ia"] * 100)

                st.markdown(f"""
                <div class="card">
                    <h3>👤 @{l['usuario']}</h3>
                    <p>💬 {l['comentario']}</p>
                    <p>🔥 <b>{score}% probabilidad de compra</b></p>
                    <p>🧠 {l['intencion']}</p>
                    <p>📦 {l['producto_interes']}</p>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Aún no tienes clientes detectados.")

    # ========================================
    # 📡 ESCANEAR CLIENTES
    # ========================================
    elif menu == "Escanear":

        st.title("📡 Buscar Clientes en TikTok")

        usuario = st.text_input("Usuario de TikTok (sin @)")

        if st.button("Buscar clientes 🔍"):

            if not usuario:
                st.warning("Escribe un usuario")
            else:
                with st.spinner("Analizando comentarios..."):

                    leads = procesar_comentarios(usuario)
                    nuevos = guardar_leads(user_id, leads)

                    if nuevos > 0:
                        st.success(f"🔥 {nuevos} clientes detectados")
                        st.balloons()
                    else:
                        st.warning("No se encontraron clientes listos para comprar")

    # ========================================
    # 📊 ANÁLISIS DE COMPETENCIA
    # ========================================
    elif menu == "Análisis Competencia":

        st.title("📊 Análisis de Competencia")

        ya_uso = verificar_demo(user_id)

        if ya_uso:
            st.warning("Ya usaste tu análisis gratuito")

            st.markdown("""
            ## 🔓 Desbloquea acceso completo

            Monitorea tu competencia automáticamente  
            Detecta tendencias virales  
            Encuentra oportunidades de venta  

            💰 Plan desde RD$1,500
            """)

            st.button("💳 Activar Plan")

        else:

            st.markdown("Introduce hasta 10 competidores")

            cuentas = st.text_area("Ejemplo: tienda1, tienda2, tienda3")

            if st.button("Analizar 🚀"):

                lista = [c.strip() for c in cuentas.split(",") if c.strip()]

                if not lista:
                    st.warning("Introduce al menos una cuenta")
                else:
                    with st.spinner("Analizando mercado..."):

                        ranking = analizar_competencia(lista)

                        if not ranking:
                            st.error("No se pudo analizar")
                        else:
                            # 📊 GRÁFICO
                            nombres = [r["usuario"] for r in ranking]
                            views = [r["promedio_views"] for r in ranking]

                            fig = px.bar(x=nombres, y=views, title="Rendimiento de Competencia")
                            st.plotly_chart(fig, use_container_width=True)

                            # 🏆 RANKING
                            st.subheader("🏆 Ranking")

                            for i, r in enumerate(ranking, 1):
                                st.write(f"{i}. @{r['usuario']} - {r['promedio_views']} views")

                            # 🧠 INSIGHT
                            insight = generar_insight(ranking)

                            st.subheader("🧠 Insight IA")
                            st.info(insight)

                            # 🔒 BLOQUEAR USO
                            marcar_demo_usado(user_id)
