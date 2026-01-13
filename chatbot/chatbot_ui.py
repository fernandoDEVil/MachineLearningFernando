import tkinter as tk
import threading
from .chatbot import preguntar_chatbot



def abrir_chatbot():
    ventana = tk.Toplevel()
    ventana.title("Chatbot IA")
    ventana.geometry("400x500")

    area_chat = tk.Text(ventana, wrap="word")
    area_chat.pack(expand=True, fill="both")

    entrada = tk.Entry(ventana)
    entrada.pack(fill="x", padx=5, pady=5)

    def enviar():
        mensaje = entrada.get()
        if not mensaje:
            return

        area_chat.insert(tk.END, f"Tú: {mensaje}\n")
        entrada.delete(0, tk.END)

        def responder():
            respuesta = preguntar_chatbot(mensaje)
            area_chat.insert(tk.END, f"IA: {respuesta}\n\n")

        threading.Thread(target=responder).start()

    btn = tk.Button(ventana, text="Enviar", command=enviar)
    btn.pack(pady=5)
