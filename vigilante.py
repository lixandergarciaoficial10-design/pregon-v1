import requests
import streamlit as st
import time
from ia_engine import analizar_lead

RAPIDAPI_KEY = st.secrets.get("RAPIDAPI_KEY", "FALTA_LA_LLAVE")

def limpiar_y_calificar(lista_comentarios, plataforma):
    leads_limpios = []
    if not lista_comentarios: 
        return []

    for c in lista_comentarios:
        # Buscamos el texto en cualquier posible llave (text, content, body)
        texto = c.get('text') or c.get('content') or c.get('body') or ""
        usuario = c.get('username') or c.get('author', {}).get('username') or "anonimo"
        
        if len(texto) < 3: continue # Ignoramos emojis solos o puntos

        # DEBUG: Para que veas en pantalla qué está analizando la IA
        # st.write(f"DEBUG: Analizando comentario de @{usuario}: {texto[:30]}...")

        analisis = analizar_lead(texto)
        score = analisis.get('score_ia', 0)
        
        # FILTRO ULTRA SENSIBLE (0.2)
        if score >= 0.2:
            leads_limpios.append({
                "usuario_ig": usuario,
                "comentario": texto,
                "score_ia": score,
                "vehiculo_interes": analisis.get('producto_interes', 'General'),
                "fuente": plataforma
            })
    return leads_limpios

# Las funciones espiar_instagram y espiar_tiktok se mantienen como las últimas 
# que te envié, ya que esas lograban el Status 200 (Conexión Exitosa).
