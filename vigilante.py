import streamlit as st
import instaloader
import pandas as pd

# Creamos el robot
L = instaloader.Instaloader()

def buscar_clientes_potenciales(cuenta_dealer):
    datos_finales = []
    try:
        # Entramos a la cuenta del dealer
        perfil = instaloader.Profile.from_username(L.context, cuenta_dealer)
        
        # Revisamos solo los 2 posts más nuevos para que sea rápido
        for i, post in enumerate(perfil.get_posts()):
            if i >= 2: break
            
            # Sacamos los comentarios
            for comentario in post.get_comments():
                datos_finales.append({
                    "Usuario": comentario.owner.username,
                    "Mensaje": comentario.text,
                    "Link del Carro": f"https://www.instagram.com/p/{post.shortcode}/"
                })
        return pd.DataFrame(datos_finales)
    except Exception as e:
        st.error(f"Hubo un problema: {e}")
        return pd.DataFrame()

# Esto es lo que verás en la pantalla de Streamlit
st.title("🚀 PREGÓN AI - Buscador de Leads")
cuenta = st.text_input("Escribe el Instagram del Dealer (sin el @):", "autorepuestomicarro27")

if st.button("Buscar Clientes Ahora"):
    resultado = buscar_clientes_potenciales(cuenta)
    if not resultado.empty:
        st.success("¡Encontramos gente interesada!")
        st.table(resultado) # Te lo muestra como una lista limpia
    else:
        st.warning("No hay comentarios nuevos todavía.")
