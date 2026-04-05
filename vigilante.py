import instaloader
import pandas as pd

L = instaloader.Instaloader()

def espiar_instagram(cuenta_target):
    resultados = []
    try:
        # Esto limpia el nombre por si acaso
        cuenta_limpia = cuenta_target.replace("@", "").strip()
        perfil = instaloader.Profile.from_username(L.context, cuenta_limpia)
        
        # Vamos a revisar los últimos 5 posts para asegurar que pescamos algo
        for i, post in enumerate(perfil.get_posts()):
            if i >= 5: break
            
            for comentario in post.get_comments():
                resultados.append({
                    "usuario_ig": comentario.owner.username,
                    "comentario": comentario.text,
                    "fuente": "Instagram",
                    "vehiculo_interes": f"Post: {post.shortcode}"
                })
        return resultados
    except Exception as e:
        print(f"Error en Instagram: {e}")
        return []

def espiar_tiktok(cuenta_target):
    return []

def limpiar_y_calificar(datos, plataforma):
    """VERSIÓN DE PRUEBA: Deja pasar TODO"""
    leads_finales = []
    
    for item in datos:
        # Por ahora, le damos un score de 0.95 a TODO para ver si llegan a Supabase
        item['score_ia'] = 0.95
        leads_finales.append(item)
            
    return leads_finales
