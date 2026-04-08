# ============================================
# 📊 ANÁLISIS DE COMPETENCIA - PREGÓN AI
# ============================================
# ✔ No depende de APIs externas
# ✔ Genera datos realistas (modo demo)
# ✔ Calcula métricas clave
# ✔ Genera insight con IA
# ============================================

import random
import statistics
from ia_engine import analizar_lead


# ============================================
# 🎥 GENERAR VIDEOS (SIMULACIÓN REALISTA)
# ============================================

def generar_videos_fake(usuario):
    """
    Genera videos con métricas realistas
    """

    videos = []

    for i in range(5):
        views = random.randint(500, 50000)
        likes = int(views * random.uniform(0.05, 0.2))

        videos.append({
            "views": views,
            "likes": likes,
            "descripcion": f"Video {i+1} de {usuario}"
        })

    return videos


# ============================================
# 📊 ANALIZAR UNA CUENTA
# ============================================

def analizar_cuenta(usuario):
    """
    Calcula métricas clave de una cuenta
    """

    videos = generar_videos_fake(usuario)

    if not videos:
        return None

    views = [v["views"] for v in videos]

    promedio = int(statistics.mean(views))
    maximo = max(views)

    # detectar videos virales (más de 70% del máximo)
    virales = [v for v in videos if v["views"] >= maximo * 0.7]

    return {
        "usuario": usuario,
        "promedio_views": promedio,
        "max_views": maximo,
        "videos": videos,
        "virales": virales
    }


# ============================================
# 🏆 ANALIZAR TODA LA COMPETENCIA
# ============================================

def analizar_competencia(lista_usuarios):
    """
    Procesa múltiples cuentas y devuelve ranking
    """

    resultados = []

    for user in lista_usuarios:
        data = analizar_cuenta(user)

        if data:
            resultados.append(data)

    # ordenar por rendimiento
    ranking = sorted(resultados, key=lambda x: x["promedio_views"], reverse=True)

    return ranking


# ============================================
# 🧠 GENERAR INSIGHT CON IA
# ============================================

def generar_insight(ranking):
    """
    Genera conclusión inteligente usando IA
    """

    if not ranking:
        return "No hay datos suficientes para analizar."

    resumen = ""

    for r in ranking[:3]:
        resumen += f"{r['usuario']} tiene promedio de {r['promedio_views']} views. "

    prompt = f"""
    Analiza estos datos de redes sociales:

    {resumen}

    Dame una conclusión clara, corta y estratégica
    sobre qué tipo de contenido está funcionando mejor.
    """

    try:
        respuesta = analizar_lead(prompt)
        return respuesta.get("intencion", "No disponible")
    except:
        return "Los videos con mayor alcance suelen tener mejor engagement."
