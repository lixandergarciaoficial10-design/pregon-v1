# ============================================
# 🤖 AUTO SCAN - PREGÓN AI
# ============================================

import os
from supabase import create_client
from apify_client import ApifyClient
from ia_engine import analizar_lead

# ============================================
# 🔐 CONFIG (desde variables de entorno)
# ============================================

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
APIFY_TOKEN = os.getenv("APIFY_TOKEN")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
client = ApifyClient(APIFY_TOKEN)

ACTOR_ID = "clockworks/tiktok-scraper"

# ============================================
# 🔍 OBTENER CUENTAS A ESCANEAR
# ============================================

def obtener_cuentas():
    res = supabase.table("radar_config").select("*").execute()
    return res.data if res.data else []

# ============================================
# 💾 GUARDAR LEADS
# ============================================

def guardar_lead(user_id, lead):
    try:
        supabase.table("leads").insert({
            "user_id": user_id,
            "usuario": lead["usuario"],
            "comentario": lead["comentario"],
            "score_ia": lead["score_ia"],
            "intencion": lead["intencion"],
            "producto_interes": lead["producto_interes"],
            "fuente": "TikTok"
        }).execute()
    except:
        pass

# ============================================
# 🚀 SCAN PRINCIPAL
# ============================================

def ejecutar_scan():

    cuentas = obtener_cuentas()

    for c in cuentas:

        user_id = c["owner_id"]
        username = c["cuenta_instagram"]  # puedes renombrar luego

        run_input = {
            "profiles": [username],
            "resultsPerPage": 3,
            "shouldDownloadComments": True,
            "commentsPerPost": 20
        }

        try:
            run = client.actor(ACTOR_ID).call(run_input=run_input)
            dataset_id = run["defaultDatasetId"]

            items = list(client.dataset(dataset_id).iterate_items())

            for post in items:
                comentarios = post.get("comments", [])

                for c in comentarios:

                    texto = c.get("text")
                    user = c.get("authorMeta", {}).get("name")

                    if not texto:
                        continue

                    analisis = analizar_lead(texto)

                    if analisis["score_ia"] >= 0.6:
                        guardar_lead(user_id, {
                            "usuario": user,
                            "comentario": texto,
                            "score_ia": analisis["score_ia"],
                            "intencion": analisis["intencion"],
                            "producto_interes": analisis["producto_interes"]
                        })

        except Exception as e:
            print("Error:", e)

# ============================================
# ▶️ EJECUTAR
# ============================================

if __name__ == "__main__":
    ejecutar_scan()
