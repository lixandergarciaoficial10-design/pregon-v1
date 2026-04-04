from groq import Groq
import json

# PEGA TU LLAVE AQUÍ
GROQ_KEY = "TU_LLAVE_DE_GROQ_AQUI"

client = Groq(api_key=GROQ_KEY)

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

# --- PRUEBA DE FUEGO ---
if __name__ == "__main__":
    resultado = analizar_lead("Dime el precio de esa Hilux 2022 que publicaste hoy")
    print(resultado)
