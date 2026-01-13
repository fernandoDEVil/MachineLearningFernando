from dotenv import load_dotenv
load_dotenv()
import numpy as np
import tkinter as tk
from tkinter import filedialog, Label, Button, messagebox
from PIL import Image, ImageTk
from tensorflow.keras.models import load_model
import joblib
import threading
from chatbot.chatbot_ui import abrir_chatbot
from tkinter import Button


from video_from_image import imagen_a_video


# -------------------------------
# Cargar modelo y KMeans
# -------------------------------
model = load_model("mi_modelo.h5")
kmeans = joblib.load("kmeans.pkl")


# -------------------------------
# Variable global para la imagen cargada
# -------------------------------
ruta_imagen_actual = None


# -------------------------------
# Preprocesar imagen y agregar cluster
# -------------------------------
def preparar_imagen(ruta):
    # 1. Escala de grises
    img = Image.open(ruta).convert("L")
    img = img.resize((28, 28))

    # 2. Normalizar
    img_array = np.array(img) / 255.0
    img_array = 1 - img_array  # MNIST: blanco sobre negro

    # 3. Aplanar
    img_flat = img_array.reshape(784)

    # 4. Calcular cluster
    cluster = kmeans.predict([img_flat])[0]

    # 5. Agregar cluster
    img_aug = np.append(img_flat, cluster)

    # 6. Batch
    img_aug = np.expand_dims(img_aug, axis=0)

    return img_aug


# -------------------------------
# Cargar imagen y predecir
# -------------------------------
def cargar_imagen():
    global ruta_imagen_actual

    ruta = filedialog.askopenfilename(
        filetypes=[("Imágenes", "*.png *.jpg *.jpeg")]
    )
    if not ruta:
        return

    ruta_imagen_actual = ruta

    # Mostrar imagen
    img = Image.open(ruta)
    img = img.resize((200, 200))
    img_tk = ImageTk.PhotoImage(img)

    label_imagen.config(image=img_tk)
    label_imagen.image = img_tk

    # Predicción
    entrada = preparar_imagen(ruta)
    pred = model.predict(entrada)
    numero = np.argmax(pred)

    label_resultado.config(text=f"Predicción: {numero}")


# -------------------------------
# Crear video desde la imagen cargada
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
ventana.title("Reconocedor MNIST con Clustering")
ventana.geometry("320x480")

label_titulo = Label(ventana, text="Reconocer Número", font=("Arial", 18))
label_titulo.pack(pady=10)

label_imagen = Label(ventana)
label_imagen.pack()

btn_cargar = Button(
    ventana,
    text="Cargar Imagen",
    command=cargar_imagen
)
btn_cargar.pack(pady=10)

label_resultado = Label(
    ventana,
    text="Predicción: -",
    font=("Arial", 16)
)
label_resultado.pack(pady=15)

btn_video = Button(
    ventana,
    text="Crear video",
    command=lambda: threading.Thread(target=crear_video).start()
)
btn_video.pack(pady=10)

btn_chatbot = Button(
    ventana,
    text="Abrir Chatbot IA",
    command=abrir_chatbot
)
btn_chatbot.pack(pady=10)


ventana.mainloop()
