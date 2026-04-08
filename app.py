# ============================================
# 🚀 PREGÓN AI - PREMIUM UI
# ============================================

import streamlit as st
from database import guardar_leads, obtener_leads
from scraper_tiktok.py import procesar_comentarios
from analisis_competencia import analizar_competencia, generar_insight
import plotly.express as px
from database import verificar_demo, marcar_demo_usado

# ============================================
# 🎨 CONFIGURACIÓN VISUAL
# ============================================

st.set_page_config(page_title="PREGÓN AI", layout="wide", page_icon="🚀")

# 🎨 CSS PREMIUM
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #020617, #0F172A);
}
h1, h2, h3, p {
    color: #F9FAFB;
}
.card {
    background: linear-gradient(145deg, #111827, #1F2937);
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 15px;
    border: 1px solid #374151;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.5);
}
.metric {
    background: #111827;
    padding: 15px;
    border-radius: 10px;
    text-align: center;
}
button {
    border-radius: 8px !important;
}
</style>
""", unsafe_allow_html=True)

# ============================================
# 🧠 LOGIN SIMPLE
# ============================================

if "user_id" not in st.session_state:
    st.session_state.user_id = None

# ============================================
# 🔐 LOGIN
# ============================================

if st.session_state.user_id is None:

    st.title("🚀 PREGÓN AI")
    st.subheader("Detecta clientes listos para comprar")

    email = st.text_input("Correo")

    if st.button("Entrar"):
        if email:
            st.session_state.user_id = email
            st.rerun()
        else:
            st.warning("Escribe tu correo")

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

        st.title("📊 Panel de Clientes Detectados")

        leads = obtener_leads(user_id)

        total = len(leads)
        calientes = len([l for l in leads if l["score_ia"] > 0.8])
        medios = len([l for l in leads if 0.5 <= l["score_ia"] <= 0.8])

        # 🔥 MÉTRICAS
        col1, col2, col3 = st.columns(3)

        col1.markdown(f"<div class='metric'><h2>{total}</h2><p>Leads Totales</p></div>", unsafe_allow_html=True)
        col2.markdown(f"<div class='metric'><h2>{calientes}</h2><p>Clientes Calientes 🔥</p></div>", unsafe_allow_html=True)
        col3.markdown(f"<div class='metric'><h2>{medios}</h2><p>Interesados 🧠</p></div>", unsafe_allow_html=True)

        st.divider()

        # 🔥 LISTA DE LEADS
        if leads:
            for l in leads:

                score = int(l["score_ia"] * 100)

                st.markdown(f"""
                <div class="card">
                    <h3>👤 @{l['usuario']}</h3>
                    <p>💬 {l['comentario']}</p>
                    <p>🔥 <b>Probabilidad de compra:</b> {score}%</p>
                    <p>🧠 {l['intencion']}</p>
                    <p>📦 {l['producto_interes']}</p>
                </div>
                """, unsafe_allow_html=True)

        else:
            st.info("No hay clientes detectados aún.")

    # ========================================
    # 📡 ESCANEAR
    # ========================================
    elif menu == "Escanear":

        st.title("📡 Radar de Clientes")

        cuenta = st.text_input("Usuario de TikTok")

        if st.button("Buscar clientes 🔍"):

            if not cuenta:
                st.warning("Escribe un usuario")

            else:
                with st.spinner("Analizando mercado..."):

                    leads = procesar_comentarios(cuenta)
                    nuevos = guardar_leads(user_id, leads)

                    if nuevos > 0:
                        st.success(f"🔥 {nuevos} clientes detectados")
                        st.balloons()
                    else:
                        st.warning("No se detectaron clientes relevantes")
elif menu == "Análisis Competencia":

    st.title("📊 Análisis de Competencia")

    # ===============================
    # 🔒 VERIFICAR SI YA USÓ DEMO
    # ===============================
    ya_uso = verificar_demo(user_id)

    if ya_uso:
        # 🚫 BLOQUEO PREMIUM
        st.warning("Ya usaste tu análisis gratuito")

        st.markdown("""
        ## 🔓 Desbloquea el acceso completo

        Obtén análisis ilimitados, monitoreo automático
        y detección de clientes en tiempo real.

        💰 Plan desde RD$1,500
        """)

        st.button("💳 Activar Plan")

    else:
        # ✅ DEMO DISPONIBLE

        st.markdown("Ingresa hasta 10 cuentas de TikTok")

        cuentas = st.text_area("Ejemplo: tienda1, tienda2, tienda3")

        if st.button("Analizar 🚀"):

            lista = [c.strip() for c in cuentas.split(",") if c.strip()]

            if not lista:
                st.warning("Ingresa al menos una cuenta")

            else:
                with st.spinner("Analizando competencia..."):

                    ranking = analizar_competencia(lista)

                    if not ranking:
                        st.error("No se pudo obtener información")
                    else:
                        # ===============================
                        # 📊 GRÁFICO
                        # ===============================
                        import plotly.express as px

                        nombres = [r["usuario"] for r in ranking]
                        views = [r["promedio_views"] for r in ranking]

                        fig = px.bar(
                            x=nombres,
                            y=views,
                            title="Rendimiento de Competencia"
                        )

                        st.plotly_chart(fig, use_container_width=True)

                        # ===============================
                        # 🏆 RANKING
                        # ===============================
                        st.subheader("🏆 Ranking")

                        for i, r in enumerate(ranking, 1):
                            st.write(f"{i}. @{r['usuario']} - {r['promedio_views']} views")

                        # ===============================
                        # 🧠 INSIGHT
                        # ===============================
                        insight = generar_insight(ranking)

                        st.subheader("🧠 Insight")
                        st.info(insight)

                        # ===============================
                        # 🔒 MARCAR COMO USADO
                        # ===============================
                        marcar_demo_usado(user_id)
