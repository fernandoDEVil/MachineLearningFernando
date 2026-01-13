import tensorflow as tf
from sklearn.cluster import KMeans
import numpy as np

# -------------------------------------------------------------
# 1. Cargar y normalizar datos
# -------------------------------------------------------------
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

x_train = x_train / 255.0
x_test = x_test / 255.0

# Aplanar imágenes para clustering
x_train_flat = x_train.reshape(-1, 784)
x_test_flat = x_test.reshape(-1, 784)

# -------------------------------------------------------------
# 2. Clustering NO SUPERVISADO (KMeans)
# -------------------------------------------------------------
print("Aplicando KMeans...")

kmeans = KMeans(n_clusters=10, random_state=42)
clusters_train = kmeans.fit_predict(x_train_flat)

# También asignamos clusters al test
clusters_test = kmeans.predict(x_test_flat)

print("Clustering completado.")

# -------------------------------------------------------------
# 3. Agregar el número de cluster como feature adicional
# -------------------------------------------------------------
x_train_aug = np.hstack([x_train_flat, clusters_train.reshape(-1, 1)])
x_test_aug = np.hstack([x_test_flat, clusters_test.reshape(-1, 1)])

print("Dimensión original:", x_train_flat.shape)
print("Dimensión con cluster:", x_train_aug.shape)

# -------------------------------------------------------------
# 4. Construcción del modelo supervisado
# -------------------------------------------------------------
model = tf.keras.Sequential([
    tf.keras.layers.Input(shape=(785,)),  # 784 pixeles + 1 cluster
    tf.keras.layers.Dense(128, activation='relu'),
    tf.keras.layers.Dense(10, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# -------------------------------------------------------------
# 5. Entrenamiento supervisado
# -------------------------------------------------------------
print("Entrenando el modelo supervisado...")
model.fit(
    x_train_aug,
    y_train,
    epochs=5,
    validation_split=0.1
)

# -------------------------------------------------------------
# 6. Evaluación
# -------------------------------------------------------------
loss, acc = model.evaluate(x_test_aug, y_test)
print("Precisión en test:", acc)

# Guardar modelo
model.save("mi_modelo.h5")
print("Modelo guardado como mi_modelo.h5")

import joblib

joblib.dump(kmeans, "kmeans.pkl")
print("KMeans guardado como kmeans.pkl")