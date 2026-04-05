import instaloader
import pandas as pd

# Inicializamos el robot
L = instaloader.Instaloader()

def espiar_instagram(cuenta_target):
    """Esta función es la que llama tu app.py al darle a ESCANEAR"""
    resultados = []
    try:
        perfil = instaloader.Profile.from_username(L.context, cuenta_target)
        # Escaneamos los últimos 2 posts
        for i, post in enumerate(perfil.get_posts()):
            if i >= 2: break
            for comentario in post.get_comments():
                resultados.append({
                    "usuario_ig": comentario.owner.username,
                    "comentario": comentario.text,
                    "fuente": "Instagram",
                    "vehiculo_interes": "Detectado por Radar"
                })
        return resultados
    except Exception as e:
        print(f"Error en Instagram: {e}")
        return []

def espiar_tiktok(cuenta_target):
    # Por ahora devolvemos vacío para que no explote la app
    return []

def limpiar_y_calificar(datos, plataforma):
    """Lógica simple para que aparezcan leads de una vez"""
    leads_finales = []
    palabras_clave = ["precio", "cuanto", "info", "donde", "disponible", "interesa"]
    
    for item in datos:
        texto = item['comentario'].lower()
        # Si tiene una palabra clave, le damos score alto
        score = 0.85 if any(p in texto for p in palabras_clave) else 0.10
        
        # Solo mandamos a la base de datos los que tienen interés (score > 0.3)
        if score > 0.3:
            item['score_ia'] = score
            leads_finales.append(item)
            
    return leads_finales
