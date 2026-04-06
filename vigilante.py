import requests
import streamlit as st
import json

def espiar_instagram(username):
    token = st.secrets["SCRAPE_DO_TOKEN"]
    # URL de Instagram para ver el perfil (pública)
    target_url = f"https://www.instagram.com/{username.replace('@', '')}/"
    
    # Le pedimos a Scrape.do que pase por nosotros
    api_url = f"http://api.scrape.do?token={token}&url={target_url}"
    
    try:
        response = requests.get(api_url, timeout=20)
        if response.status_code == 200:
            # Aquí vendría el parseo del HTML. 
            # Como Instagram es complejo, Scrape.do tiene un modo "render" si es necesario.
            # Por ahora, simulamos la captura de datos para que veas el flujo:
            return [
                {"usuario_ig": "cliente_interesado_1", "comentario": "Precio de la Hyundai 2022?"},
                {"usuario_ig": "user_rd_99", "comentario": "Donde estan ubicados? me interesa el civic"}
            ]
        else:
            st.error(f"Error Scrape.do: {response.status_code}")
            return []
    except Exception as e:
        st.error(f"Fallo de conexión: {e}")
        return []

def limpiar_y_calificar(datos, plataforma):
    from ia_engine import analizar_lead
    finales = []
    for d in datos:
        res = analizar_lead(d["comentario"])
        if res["score_ia"] > 0.3:
            d["score_ia"] = res["score_ia"]
            d["fuente"] = plataforma
            finales.append(d)
    return finales
