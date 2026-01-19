from dotenv import load_dotenv
load_dotenv()

import numpy as np
import tkinter as tk
from tkinter import filedialog, Label, Button, messagebox
from PIL import Image, ImageTk
import joblib
import threading

from chatbot.chatbot_ui import abrir_chatbot
from video_from_image import imagen_a_video


# -------------------------------
# Cargar SOLO KMeans (opcional)
# -------------------------------
try:
    kmeans = joblib.load("kmeans.pkl")
except FileNotFoundError:
    kmeans = None
    print("⚠️ kmeans.pkl no encontrado. Clustering deshabilitado.")


# -------------------------------
# Variable global
# -------------------------------
ruta_imagen_actual = None


# -------------------------------
# Preprocesar imagen (sin modelo)
# -------------------------------
def preparar_imagen(ruta):
    img = Image.open(ruta).convert("L")
    img = img.resize((28, 28))

    img_array = np.array(img) / 255.0
    img_array = 1 - img_array
    img_flat = img_array.reshape(784)

    if kmeans:
        cluster = kmeans.predict([img_flat])[0]
        img_flat = np.append(img_flat, cluster)

    return img_flat


# -------------------------------
# Cargar imagen
# -------------------------------
def cargar_imagen():
    global ruta_imagen_actual

    ruta = filedialog.askopenfilename(
        filetypes=[("Imágenes", "*.png *.jpg *.jpeg")]
    )
    if not ruta:
        return

    ruta_imagen_actual = ruta

    img = Image.open(ruta).resize((200, 200))
    img_tk = ImageTk.PhotoImage(img)

    label_imagen.config(image=img_tk)
    label_imagen.image = img_tk

    label_resultado.config(text="Imagen cargada correctamente")


# -------------------------------
# Crear video
# -------------------------------
def crear_video():
    if ruta_imagen_actual is None:
        messagebox.showerror("Error", "Primero carga una imagen")
        return

    imagen_a_video(ruta_imagen_actual)
    messagebox.showinfo("Listo", "Video creado como video.mp4")


# -------------------------------
# Interfaz gráfica
# -------------------------------
ventana = tk.Tk()
ventana.title("Reconocedor MNIST con Chatbot IA")
ventana.geometry("320x480")

Label(ventana, text="Reconocer Número", font=("Arial", 18)).pack(pady=10)

label_imagen = Label(ventana)
label_imagen.pack()

Button(
    ventana,
    text="Cargar Imagen",
    command=cargar_imagen
).pack(pady=10)

label_resultado = Label(
    ventana,
    text="Estado: -",
    font=("Arial", 14)
)
label_resultado.pack(pady=15)

Button(
    ventana,
    text="Crear video",
    command=lambda: threading.Thread(target=crear_video).start()
).pack(pady=10)

Button(
    ventana,
    text="Abrir Chatbot IA",
    command=abrir_chatbot
).pack(pady=10)

ventana.mainloop()
