import requests
import streamlit as st

def espiar_instagram(username):
    token = st.secrets["SCRAPE_DO_TOKEN"]
    target = username.replace("@", "").strip()
    
    # CAMBIO CRÍTICO: Usamos la URL de búsqueda o una publicación específica si la tienes
    # Pero para perfiles, vamos a forzar el parámetro de 'extraHeaders'
    target_url = f"https://www.instagram.com/{target}/"
    
    # Agregamos 'geoCode=do' para que use IPs de República Dominicana (más natural para cuentas locales)
    # Y quitamos el 'render=true' por un momento para probar si el HTML estático pasa el muro
    api_url = f"http://api.scrape.do?token={token}&url={target_url}&super=true&geoCode=do"
    
    try:
        # Si ya falló muchas veces, lanzamos un error antes de gastar
        response = requests.get(api_url, timeout=25)
        
        if response.status_code == 200:
            html = response.text
            
            # Si vemos 'login', 'cuestión de seguridad' o 'challenge', paramos en seco
            if any(x in html.lower() for x in ["login", "challenge", "checkpoint", "robot"]):
                st.error(f"🚫 Instagram bloqueó el acceso a @{target}. NO sigas intentando con esta cuenta ahora.")
                return []

            # Si el HTML parece real, buscamos los comentarios
            import re
            comentarios = re.findall(r'"text":"([^"]+)"', html)
            
            if comentarios:
                return [{"usuario_ig": f"lead_{target}", "comentario": c} for c in comentarios[:15]]
            
            # Si llegamos aquí y no hay nada, devolvemos una lista VACÍA para que el bucle de app.py se detenga
            return []
        else:
            st.error(f"Error de Scrape.do: {response.status_code}")
            return []
    except:
        return []
