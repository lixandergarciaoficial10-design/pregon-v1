# ============================================
# 🧠 CONTROL DE DEMO
# ============================================

def verificar_demo(user_id):
    """
    Verifica si el usuario ya usó el análisis gratis
    """
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
        return True  # por seguridad bloqueamos


def marcar_demo_usado(user_id):
    """
    Marca que el usuario ya usó su demo
    """
    try:
        supabase.table("profiles")\
            .update({"uso_demo": True})\
            .eq("id", user_id)\
            .execute()

    except Exception as e:
        print("Error actualizando demo:", e)
