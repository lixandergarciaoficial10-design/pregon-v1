import streamlit as st
from instagrapi import Client
import os

def espiar_instagram(cuenta_target):
    cl = Client()
    
    # Intentamos usar una sesión guardada para que no te bloqueen
    # Debes poner tu usuario y clave de IG en los Secrets de Streamlit
    IG_USER = st.secrets["IG_USER"]
    IG_PASS = st.secrets["IG_PASS"]
    
    try:
        # 1. Login automático en la nube
        cl.login(IG_USER, IG_PASS)
        
        # 2. Buscamos al dealer
        user_id = cl.user_id_from_username(cuenta_target.replace("@", ""))
        
        # 3. Traemos el último post
        posts = cl.user_medias(user_id, 1)
        if not posts:
            return []
            
        media_id = posts[0].id
        
        # 4. Traemos los comentarios (esto es lo que vale dinero)
        comments = cl.media_comments(media_id, 20)
        
        datos_crudos = []
        for com in comments:
            datos_crudos.append({
                "usuario_ig": com.user.username,
                "comentario": com.text,
                "fuente": "Instagram Cloud",
                "vehiculo_interes": "Post Reciente"
            })
        return datos_crudos

    except Exception as e:
        st.error(f"Error de Conexión Instagram: {e}")
        return []

def limpiar_y_calificar(datos, plataforma):
    leads_finales = []
    # Palabras de dinero en RD
    palabras = ["precio", "cuanto", "info", "disponible", "donde", "ubicacion", "numero", "whatsapp", "interesa"]
    
    for item in datos:
        texto = item['comentario'].lower()
        if any(p in texto for p in palabras):
            item['score_ia'] = 0.95
            leads_finales.append(item)
    return leads_finales
