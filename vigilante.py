import streamlit as st
from apify_client import ApifyClient

# CONFIGURACIÓN SEGURA
try:
    APIFY_TOKEN = st.secrets["APIFY_TOKEN"]
    client = ApifyClient(APIFY_TOKEN)
except Exception as e:
    st.error("⚠️ Error: No se encontró el APIFY_TOKEN en los Secrets de Streamlit.")
    client = None

def espiar_instagram(cuenta_target):
    """Llama al motor de Apify configurado para perfiles completos"""
    if client is None:
        return []

    # Limpiamos el nombre por si viene con @ o espacios
    usuario = cuenta_target.replace("@", "").strip()
    
    # NUEVA CONFIGURACIÓN: Buscamos por nombre de usuario, no por URL
    run_input = {
        "usernames": [usuario],
        "commentsLimit": 30, # Traer 30 comentarios en total
        "resultsLimit": 5    # Revisar los últimos 5 posts del perfil
    }

    try:
        # Ejecutamos el scraper de comentarios
        run = client.actor("apify/instagram-comment-scraper").call(run_input=run_input)
        
        datos_crudos = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            # Apify nos devuelve el texto y el dueño del comentario
            datos_crudos.append({
                "usuario_ig": item.get("ownerUsername"),
                "comentario": item.get("text"),
                "fuente": "Instagram (Apify)",
                "vehiculo_interes": "Radar Pregon-v1"
            })
        return datos_crudos
    except Exception as e:
        st.error(f"Error en Apify: {e}")
        return []

def espiar_tiktok(t): return [] 

def limpiar_y_calificar(datos, plataforma):
    """Filtro de Intención de Compra"""
    leads_finales = []
    palabras_clave = ["precio", "cuanto", "info", "disponible", "donde", "ubicacion", "venden", "numero", "whatsapp", "interesa", "interesado"]
    
    for item in datos:
        texto = str(item['comentario']).lower()
        
        # Si tiene palabra clave -> Score 0.95 (Caliente)
        if any(p in texto for p in palabras_clave):
            item['score_ia'] = 0.95
            leads_finales.append(item)
        # Si es un comentario con sustancia (más de 15 letras) -> Score 0.45 (Tibio)
        elif len(texto) > 15:
            item['score_ia'] = 0.45
            leads_finales.append(item)
            
    return leads_finales
