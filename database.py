# ============================================
# 🗄️ BASE DE DATOS - PREGÓN AI
# ============================================

import streamlit as st
from supabase import create_client

# ============================================
# 🔐 CONEXIÓN A SUPABASE
# ============================================

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ============================================
# 💾 GUARDAR LEADS
# ============================================

def guardar_leads(user_id, leads):
    nuevos = 0

    for l in leads:
        try:
            supabase.table("leads").insert({
                "user_id": user_id,
                "usuario": l.get("usuario"),
                "comentario": l.get("comentario"),
                "score_ia": l.get("score_ia"),
                "intencion": l.get("intencion"),
                "producto_interes": l.get("producto_interes")
            }).execute()
            nuevos += 1
        except:
            pass  # evita duplicados

    return nuevos

# ============================================
# 📥 OBTENER LEADS
# ============================================

def obtener_leads(user_id):
    try:
        res = supabase.table("leads")\
            .select("*")\
            .eq("user_id", user_id)\
            .execute()

        return res.data if res.data else []

    except Exception as e:
        print("Error obteniendo leads:", e)
        return []

# ============================================
# 🧠 CONTROL DE DEMO
# ============================================

def verificar_demo(user_id):
    try:
        res = supabase.table("profiles")\
            .select("uso_demo")\
            .eq("id", user_id)\
            .execute()

        if res.data:
            return res.data[0].get("uso_demo", False)
        return False

    except Exception as e:
        print("Error verificando demo:", e)
        return True


def marcar_demo_usado(user_id):
    try:
        supabase.table("profiles")\
            .update({"uso_demo": True})\
            .eq("id", user_id)\
            .execute()

    except Exception as e:
        print("Error actualizando demo:", e)
