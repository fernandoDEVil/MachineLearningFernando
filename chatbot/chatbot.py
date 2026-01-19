import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

def preguntar_chatbot(texto, historial=None):
    mensajes = []

    if historial:
        mensajes.extend(historial)

    mensajes.append({
        "role": "user",
        "content": texto
    })

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=mensajes,
        temperature=0.7
    )

    return response.choices[0].message.content
