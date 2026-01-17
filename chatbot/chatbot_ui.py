import tkinter as tk
from tkinter import scrolledtext
import threading

from chatbot.chatbot import preguntar_chatbot
from chatbot.chat_storage import (
    inicializar_db,
    guardar_mensaje,
    obtener_conversaciones,
    obtener_mensajes_por_fecha
)


def abrir_chatbot():
    inicializar_db()

    ventana = tk.Toplevel()
    ventana.title("Chatbot IA")
    ventana.geometry("700x500")

    # ===============================
    # Layout principal
    # ===============================
    frame_izquierdo = tk.Frame(ventana, width=180, bg="#f0f0f0")
    frame_izquierdo.pack(side="left", fill="y")

    frame_derecho = tk.Frame(ventana)
    frame_derecho.pack(side="right", fill="both", expand=True)

    # ===============================
    # Lista de conversaciones
    # ===============================
    tk.Label(
        frame_izquierdo,
        text="Conversaciones",
        bg="#f0f0f0",
        font=("Arial", 12, "bold")
    ).pack(pady=10)

    lista_conversaciones = tk.Listbox(frame_izquierdo)
    lista_conversaciones.pack(fill="both", expand=True, padx=5, pady=5)

    # ===============================
    # Área de chat
    # ===============================
    area_chat = scrolledtext.ScrolledText(
        frame_derecho,
        wrap=tk.WORD,
        font=("Arial", 11)
    )
    area_chat.pack(expand=True, fill="both", padx=10, pady=10)
    area_chat.config(state="disabled")

    # ===============================
    # Entrada inferior
    # ===============================
    frame_input = tk.Frame(frame_derecho)
    frame_input.pack(fill="x", padx=10, pady=10)

    entrada = tk.Entry(frame_input, font=("Arial", 12))
    entrada.pack(side="left", fill="x", expand=True, padx=(0, 10))

    boton_enviar = tk.Button(frame_input, text="Enviar", width=10)
    boton_enviar.pack(side="right")

    # ===============================
    # Funciones
    # ===============================
    def cargar_conversaciones():
        lista_conversaciones.delete(0, "end")
        for fecha in obtener_conversaciones():
            lista_conversaciones.insert("end", fecha)

    def mostrar_conversacion(event):
        seleccion = lista_conversaciones.curselection()
        if not seleccion:
            return

        fecha = lista_conversaciones.get(seleccion[0])
        mensajes = obtener_mensajes_por_fecha(fecha)

        area_chat.config(state="normal")
        area_chat.delete("1.0", "end")

        for rol, contenido in mensajes:
            if rol == "user":
                area_chat.insert("end", f"Tú: {contenido}\n")
            else:
                area_chat.insert("end", f"Bot: {contenido}\n")

        area_chat.insert("end", "\n")
        area_chat.config(state="disabled")
        area_chat.see("end")

    def enviar_mensaje(event=None):
        texto = entrada.get().strip()
        if not texto:
            return

        entrada.delete(0, "end")

        area_chat.config(state="normal")
        area_chat.insert("end", f"Tú: {texto}\n")
        area_chat.config(state="disabled")
        area_chat.see("end")

        guardar_mensaje("user", texto)

        threading.Thread(
            target=procesar_respuesta,
            args=(texto,),
            daemon=True
        ).start()

    def procesar_respuesta(texto):
        respuesta = preguntar_chatbot(texto)
        guardar_mensaje("bot", respuesta)

        area_chat.config(state="normal")
        area_chat.insert("end", f"Bot: {respuesta}\n\n")
        area_chat.config(state="disabled")
        area_chat.see("end")

        cargar_conversaciones()

    # ===============================
    # Eventos
    # ===============================
    boton_enviar.config(command=enviar_mensaje)
    entrada.bind("<Return>", enviar_mensaje)
    lista_conversaciones.bind("<<ListboxSelect>>", mostrar_conversacion)

    cargar_conversaciones()
