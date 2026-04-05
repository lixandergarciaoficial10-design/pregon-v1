import streamlit as st
from apify_client import ApifyClient

# CONFIGURACIÓN DE CLIENTE
try:
    APIFY_TOKEN = st.secrets["APIFY_TOKEN"]
    client = ApifyClient(APIFY_TOKEN)
except:
    client = None

def espiar_instagram(cuenta_target):
    """
    Versión 'Navegador Real': Obliga a Apify a cargar el JavaScript 
    para que los comentarios no aparezcan vacíos.
    """
    if client is None: return []
    usuario = cuenta_target.replace("@", "").strip()
    
    # INPUT PARA FORZAR CARGA DE DATOS REALES
    run_input = {
        "directUrls": [f"https://www.instagram.com/{usuario}/"],
        "resultsLimit": 1, 
        "resultsType": "details", # Entra al detalle del post
        "searchLimit": 1,
        "searchType": "hashtag",
        "proxyConfiguration": { "useApifyProxy": True }, # USA PROXY RESIDENCIAL
        "commentsLimit": 50
    }

    try:
        # Ejecutamos el actor
        run = client.actor("apify/instagram-scraper").call(run_input=run_input)
        
        datos_crudos = []
        items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

        for item in items:
            # Buscamos en todas las rutas posibles del JSON de Apify
            comentarios = item.get("latestComments", [])
            if not comentarios:
                comentarios = item.get("comments", [])

            for com in comentarios:
                # Extraemos usuario y texto
                user_ig = com.get("ownerUsername") or com.get("owner", {}).get("username")
                texto_com = com.get("text")
                
                if user_ig and texto_com:
                    datos_crudos.append({
                        "usuario_ig": user_ig,
                        "comentario": texto_com,
                        "fuente": "Instagram",
                        "vehiculo_interes": f"Post: {item.get('shortCode', 'Reciente')}"
                    })
        
        return datos_crudos
    except Exception as e:
        st.error(f"Error en la consulta: {e}")
        return []

def espiar_tiktok(t): 
    return [] # Próxima fase

def limpiar_y_calificar(datos, plataforma):
    """
    FILTRO DE PRUEBA: Deja pasar todo para confirmar que el 'tubo' 
    de datos ya no está vacío.
    """
    leads_finales = []
    for item in datos:
        # Forzamos que aparezcan en el Dashboard
        item['score_ia'] = 0.95 
        leads_finales.append(item)
    return leads_finales
