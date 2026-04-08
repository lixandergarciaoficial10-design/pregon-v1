# ============================================
# 🗄️ DATABASE - PREGÓN AI (VERSIÓN COMPLETA)
# ============================================
# ✔ Conexión a Supabase
# ✔ Guardar leads
# ✔ Obtener leads
# ✔ Control de demo (1 uso gratis)
# ✔ Manejo de errores seguro
# ============================================

import streamlit as st
from supabase import create_client

# ============================================
# 🔐 CONFIGURACIÓN
# ============================================

SUPABASE_URL = st.secrets.get("SUPABASE_URL")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise Exception("Faltan SUPABASE_URL o SUPABASE_KEY en secrets")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# ============================================
# 🧠 PERFIL / DEMO
# ============================================

def verificar_demo(user_id):
    """
    Verifica si el usuario ya usó su análisis gratis.
    Si no existe perfil, lo crea automáticamente.
    """
    try:
        res = supabase.table("profiles") \
            .select("*") \
            .eq("id", user_id) \
            .execute()

        if res.data:
            return res.data[0].get("uso_demo", False)

        # 🔥 Si no existe, lo creamos
        supabase.table("profiles").insert({
            "id": user_id,
            "uso_demo": False
        }).execute()

        return False

    except Exception as e:
        print("Error verificar_demo:", e)
        return True  # por seguridad bloqueamos


def marcar_demo_usado(user_id):
    """
    Marca que el usuario ya usó el demo
    """
    try:
        supabase.table("profiles") \
            .update({"uso_demo": True}) \
            .eq("id", user_id) \
            .execute()
    except Exception as e:
        print("Error marcar_demo:", e)

# ============================================
# 💾 GUARDAR LEADS
# ============================================

def guardar_leads(user_id, leads):
    """
    Guarda leads en la base de datos
    Evita duplicados por usuario + comentario
    """
    nuevos = 0

    for l in leads:
        try:
            # 🔎 Verificar duplicado
            check = supabase.table("leads") \
                .select("id") \
                .eq("user_id", user_id) \
                .eq("comentario", l.get("comentario")) \
                .execute()

            if check.data:
                continue  # ya existe

            supabase.table("leads").insert({
                "user_id": user_id,
                "usuario": l.get("usuario"),
                "comentario": l.get("comentario"),
                "score_ia": l.get("score_ia"),
                "intencion": l.get("intencion"),
                "producto_interes": l.get("producto_interes"),
                "fuente": l.get("fuente", "TikTok")
            }).execute()

            nuevos += 1

        except Exception as e:
            print("Error guardando lead:", e)

    return nuevos

# ============================================
# 📥 OBTENER LEADS
# ============================================

def obtener_leads(user_id):
    """
    Obtiene todos los leads del usuario
    """
    try:
        res = supabase.table("leads") \
            .select("*") \
            .eq("user_id", user_id) \
            .order("id", desc=True) \
            .execute()

        return res.data if res.data else []

    except Exception as e:
        print("Error obtener_leads:", e)
        return []
