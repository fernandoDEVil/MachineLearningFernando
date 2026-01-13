from openai import OpenAI
import os

# Cliente OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def preguntar_chatbot(mensaje_usuario):
    """
    Envía un mensaje al modelo de IA y devuelve la respuesta
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "Eres un asistente útil y claro."},
            {"role": "user", "content": mensaje_usuario}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content
