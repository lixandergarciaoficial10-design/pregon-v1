# ============================================
# 🗄️ DATABASE - PREGÓN AI
# ============================================
# Este archivo maneja TODA la comunicación
# con Supabase:
# - conexión
# - insertar datos
# - consultar leads
# ============================================

import streamlit as st
from supabase import create_client

# ============================================
# 🔐 CONEXIÓN A SUPABASE
# ============================================

# Obtenemos credenciales desde Streamlit Secrets
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

# Creamos cliente de Supabase
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# ============================================
# 💾 GUARDAR LEADS
# ============================================

def guardar_leads(user_id, leads):
    """
    Guarda una lista de leads en la base de datos.

    user_id → ID del cliente (dueño de los leads)
    leads → lista de diccionarios
    """

    if not leads:
        return 0

    insertados = 0

    for lead in leads:
        try:
            # ====================================
            # 🧠 PREVENIR DUPLICADOS
            # ====================================
            existe = supabase.table("leads")\
                .select("id")\
                .eq("usuario", lead["usuario"])\
                .eq("comentario", lead["comentario"])\
                .execute()

            if existe.data:
                continue  # ya existe, lo saltamos

            # ====================================
            # 💾 INSERTAR NUEVO LEAD
            # ====================================
            supabase.table("leads").insert({
                "owner_id": user_id,
                "usuario": lead["usuario"],
                "comentario": lead["comentario"],
                "score_ia": lead["score_ia"],
                "intencion": lead["intencion"],
                "producto_interes": lead["producto_interes"],
                "fuente": lead["fuente"]
            }).execute()

            insertados += 1

        except Exception as e:
            print(f"Error guardando lead: {e}")

    return insertados


# ============================================
# 📊 OBTENER LEADS DE UN USUARIO
# ============================================

def obtener_leads(user_id):
    """
    Devuelve todos los leads del usuario ordenados
    por fecha más reciente.
    """

    try:
        res = supabase.table("leads")\
            .select("*")\
            .eq("owner_id", user_id)\
            .order("created_at", desc=True)\
            .execute()

        return res.data if res.data else []

    except Exception as e:
        print(f"Error obteniendo leads: {e}")
        return []


# ============================================
# 🧹 BORRAR LEADS (OPCIONAL)
# ============================================

def borrar_leads(user_id):
    """
    Borra todos los leads de un usuario.
    (Útil para pruebas)
    """

    try:
        supabase.table("leads")\
            .delete()\
            .eq("owner_id", user_id)\
            .execute()

        return True

    except Exception as e:
        print(f"Error borrando leads: {e}")
        return False
