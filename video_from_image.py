import cv2
import numpy as np
from PIL import Image


def imagen_a_video(ruta_imagen, salida="video.mp4", fps=24):
    # Cargar imagen
    img = Image.open(ruta_imagen).convert("RGB")
    img = np.array(img)

    h, w, _ = img.shape
    total_frames = fps * 3  # 3 segundos

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    video = cv2.VideoWriter(salida, fourcc, fps, (w, h))

    for i in range(total_frames):
        scale = 1 + i * 0.002
        resized = cv2.resize(img, None, fx=scale, fy=scale)

        y = (resized.shape[0] - h) // 2
        x = (resized.shape[1] - w) // 2
        frame = resized[y:y+h, x:x+w]

        video.write(frame)

    video.release()
    return salida
