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
.stApp {
    background-color: #F8FAFC;
}
h1, h2, h3 {
    color: #0F172A;
}
.card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 15px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
}
.metric {
    background: white;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0px 2px 10px rgba(0,0,0,0.05);
}
button {
    border-radius: 10px !important;
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
