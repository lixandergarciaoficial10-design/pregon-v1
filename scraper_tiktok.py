# ============================================
# 📡 SCRAPER REAL TIKTOK - APIFY
# ============================================

import streamlit as st
from apify_client import ApifyClient
from ia_engine import analizar_lead

# ============================================
# 🔐 CONFIG
# ============================================

APIFY_TOKEN = st.secrets.get("APIFY_TOKEN")

if not APIFY_TOKEN:
    raise Exception("Falta APIFY_TOKEN en secrets")

client = ApifyClient(APIFY_TOKEN)

# Actor oficial de TikTok scraping
ACTOR_ID = "clockworks/tiktok-scraper"

# ============================================
# 🎥 OBTENER POSTS + COMENTARIOS
# ============================================

def obtener_datos_tiktok(usuario):
    """
    Llama a Apify para obtener videos y comentarios reales
    """

    run_input = {
        "profiles": [usuario],
        "resultsPerPage": 3,
        "shouldDownloadComments": True,
        "commentsPerPost": 20
    }

    try:
        run = client.actor(ACTOR_ID).call(run_input=run_input)
        dataset_id = run["defaultDatasetId"]

        items = list(client.dataset(dataset_id).iterate_items())

        return items

    except Exception as e:
        print("Error Apify:", e)
        return []

# ============================================
# 🧠 PROCESAR COMENTARIOS
# ============================================

def procesar_comentarios(usuario):
    """
    Extrae comentarios reales y los analiza con IA
    """

    data = obtener_datos_tiktok(usuario)

    leads = []

    for post in data:

        comentarios = post.get("comments", [])

        for c in comentarios:

            texto = c.get("text")
            user = c.get("authorMeta", {}).get("name")

            if not texto:
                continue

            try:
                analisis = analizar_lead(texto)
                score = analisis.get("score_ia", 0)

                if score >= 0.6:
                    leads.append({
                        "usuario": user,
                        "comentario": texto,
                        "score_ia": score,
                        "intencion": analisis.get("intencion"),
                        "producto_interes": analisis.get("producto_interes"),
                        "fuente": "TikTok"
                    })

            except Exception as e:
                print("Error IA:", e)

    return leads
