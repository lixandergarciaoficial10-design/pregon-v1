from groq import Groq
import json
import streamlit as st

# Esto busca la llave que acabas de guardar en el cuadro de Secrets
GROQ_KEY = st.secrets["GROQ_API_KEY"]

def analizar_lead(comentario):
    """
    Toma un comentario de Instagram y lo convierte en datos para tu tabla.
    """
    prompt = f"""
    Eres un experto en ventas de vehículos en República Dominicana.
    Analiza este comentario de Instagram: "{comentario}"
    
    Determina:
    1. score_ia: Probabilidad de compra del 0.0 al 1.0.
    2. vehiculo_interes: Qué vehículo menciona (ej: 'Honda Civic', 'CRV', 'N/A').
    
    Responde estrictamente en este formato JSON:
    {{"score_ia": 0.0, "vehiculo_interes": "nombre"}}
    """

    try:
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama3-8b-8192",
            response_format={"type": "json_object"}
        )
        return json.loads(response.choices[0].message.content)
    except Exception as e:
        print(f"Error en IA: {e}")
        return {"score_ia": 0, "vehiculo_interes": "Error"}

        # --- AGREGA ESTO AL FINAL DE TU MENÚ DE NAVEGACIÓN ---
        elif menu == "Laboratorio IA":
            st.title("🧠 Probador de Cerebro (Groq)")
            st.info("Escribe un comentario para ver cómo la IA lo analiza en tiempo real.")
            
            from ia_engine import analizar_lead # Importamos tu archivo nuevo
            
            test_input = st.text_input("Escribe un comentario de prueba (ej: 'Me interesa la Hilux'):")
            
            if st.button("Analizar con Llama 3"):
                if test_input:
                    with st.spinner("Pensando..."):
                        resultado = analizar_lead(test_input)
                        st.json(resultado) # Muestra el JSON que genera la IA
                        
                        # Prueba visual de cómo se vería la card
                        st.divider()
                        st.subheader("Vista previa de la Card:")
                        st.markdown(f"""
                        <div class="card">
                            <h3>👤 @usuario_prueba</h3>
                            <p>🚗 <b>Vehículo:</b> {resultado.get('vehiculo_interes')}</p>
                            <p>🔥 <b>Score:</b> {int(resultado.get('score_ia', 0)*100)}%</p>
                        </div>
                        """, unsafe_allow_html=True)
                else:
                    st.warning("Escribe algo primero, Lixander.")

# --- PRUEBA DE FUEGO ---
if __name__ == "__main__":
    resultado = analizar_lead("Dime el precio de esa Hilux 2022 que publicaste hoy")
    print(resultado)
