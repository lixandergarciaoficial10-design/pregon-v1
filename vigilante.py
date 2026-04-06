import requests
import streamlit as st
import re

def espiar_instagram(username):
    """
    Intenta extraer datos de Instagram usando Scrape.do con protección de créditos.
    """
    if "SCRAPE_DO_TOKEN" not in st.secrets:
        st.error("Falta SCRAPE_DO_TOKEN en los Secrets.")
        return []

    token = st.secrets["SCRAPE_DO_TOKEN"]
    target = username.replace("@", "").strip()
    target_url = f"https://www.instagram.com/{target}/"
    
    # Usamos geoCode=do para parecer una conexión local de República Dominicana
    api_url = f"http://api.scrape.do?token={token}&url={target_url}&super=true&geoCode=do"
    
    try:
        response = requests.get(api_url, timeout=25)
        
        if response.status_code == 200:
            html = response.text
            
            # BLOQUEO DE SEGURIDAD: Si detecta login, corta la ejecución
            if any(x in html.lower() for x in ["login", "challenge", "checkpoint", "robot"]):
                st.error(f"🚫 Instagram bloqueó el acceso a @{target}. No gastes más créditos ahora.")
                return []

            # Buscamos patrones de texto de comentarios
            comentarios = re.findall(r'"text":"([^"]+)"', html)
            
            if comentarios:
                # Si hay datos reales, los devolvemos
                return [{"usuario_ig": f"lead_{target}", "comentario": c} for c in comentarios[:15]]
            
            # Si no hay comentarios reales pero entró, mandamos un aviso silencioso
            return []
        else:
            st.error(f"Error de Scrape.do: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Error de red: {e}")
        return []

def limpiar_y_calificar(datos, plataforma):
    """
    ESTA FUNCIÓN ES LA QUE FALTABA Y CAUSABA EL IMPORT ERROR.
    """
    from ia_engine import analizar_lead
    finales = []
    
    if not datos:
        return []

    for d in datos:
        # Usamos tu motor de IA que ya confirmamos que funciona
        res = analizar_lead(d["comentario"])
        
        # Solo leads con intención de compra (Score > 0.3)
        if res["score_ia"] > 0.3:
            d["score_ia"] = res["score_ia"]
            d["producto_interes"] = res.get("interes", "General")
            d["fuente"] = plataforma
            finales.append(d)
            
    return finales
