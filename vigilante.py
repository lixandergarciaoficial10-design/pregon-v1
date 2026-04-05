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
    """Versión Final: Usa la URL directa del perfil para evitar errores de validación"""
    if client is None:
        return []

    # Limpiamos el nombre y armamos la URL completa
    usuario = cuenta_target.replace("@", "").strip()
    url_perfil = f"https://www.instagram.com/{usuario}/"
    
    # CONFIGURACIÓN QUE PIDE APIFY
    run_input = {
        "directUrls": [url_perfil],
        "resultsLimit": 20,      # Cuántos comentarios traer en total
        "searchLimit": 1,        # Cuántos posts revisar (1 para probar rápido)
        "searchType": "hashtag"  # Se deja así para que el scraper sepa que es una búsqueda
    }

    try:
        # Volvemos al scraper general que es más flexible con las URLs de perfiles
        run = client.actor("apify/instagram-scraper").call(run_input=run_input)
        
        datos_crudos = []
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            # Extraemos los comentarios si el item los trae
            comentarios = item.get("latestComments", [])
            for com in comentarios:
                datos_crudos.append({
                    "usuario_ig": com.get("ownerUsername"),
                    "comentario": com.get("text"),
                    "fuente": "Instagram (Apify)",
                    "vehiculo_interes": f"Post: {item.get('shortCode', 'N/A')}"
                })
        return datos_crudos
    except Exception as e:
        st.error(f"Error en Apify: {e}")
        return []

def espiar_tiktok(t): return [] 

def limpiar_y_calificar(datos, plataforma):
    """VERSIÓN DE PRUEBA: Deja pasar absolutamente TODO"""
    leads_finales = []
    for item in datos:
        # Le damos score alto a todo para que aparezca en el Dashboard
        item['score_ia'] = 0.99 
        leads_finales.append(item)
    return leads_finales
    
    for item in datos:
        texto = str(item['comentario']).lower()
        if any(p in texto for p in palabras_clave):
            item['score_ia'] = 0.95
            leads_finales.append(item)
        elif len(texto) > 10:
            item['score_ia'] = 0.45
            leads_finales.append(item)
            
    return leads_finales
