import streamlit as st
from instagrapi import Client
import time

def espiar_instagram(cuenta_target):
    """Escaneo directo desde la nube usando una sesión de Instagram"""
    cl = Client()
    
    # Credenciales desde los Secrets
    usuario_ig = st.secrets["IG_USER"]
    clave_ig = st.secrets["IG_PASS"]
    
    try:
        # 1. Login (La nube simula un dispositivo real)
        cl.login(usuario_ig, clave_ig)
        
        # 2. Buscamos al dealer por su nombre de usuario
        target = cuenta_target.replace("@", "").strip()
        user_id = cl.user_id_from_username(target)
        
        # 3. Obtenemos el último post publicado
        medias = cl.user_medias(user_id, 1)
        if not medias:
            return []
            
        media_id = medias[0].id
        
        # 4. Extraemos los últimos 30 comentarios de ese post
        comments = cl.media_comments(media_id, 30)
        
        datos_crudos = []
        for c in comments:
            datos_crudos.append({
                "usuario_ig": c.user.username,
                "comentario": c.text,
                "fuente": "Instagram Cloud",
                "vehiculo_interes": f"Post: {medias[0].code}"
            })
        return datos_crudos

    except Exception as e:
        st.error(f"Error de conexión con Instagram: {e}")
        return []

def espiar_tiktok(t):
    return [] # Próxima actualización

def limpiar_y_calificar(datos, plataforma):
    """IA de calificación basada en intención de compra"""
    leads_finales = []
    # Diccionario de palabras 'calientes' para el mercado dominicano
    keywords = ["precio", "cuanto", "info", "informacion", "donde", "ubicacion", "disponible", "whatsapp", "numero", "venden"]
    
    for item in datos:
        texto = item['comentario'].lower()
        # Si tiene una keyword, le damos score alto
        if any(k in texto for k in keywords):
            item['score_ia'] = 0.98
            leads_finales.append(item)
        # Si el comentario es largo, quizás tiene interés aunque no use la palabra exacta
        elif len(texto) > 15:
            item['score_ia'] = 0.50
            leads_finales.append(item)
            
    return leads_finales
