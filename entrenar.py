import tensorflow as tf
from tensorflow.keras import layers, models

# Cargar dataset MNIST
(x_train, y_train), (x_test, y_test) = tf.keras.datasets.mnist.load_data()

# Normalizar
x_train = x_train / 255.0
x_test = x_test / 255.0

# Construcción del modelo
model = models.Sequential([
    layers.Input(shape=(28, 28)),
    layers.Flatten(),
    layers.Dense(128, activation='relu'),
    layers.Dense(10, activation='softmax')
])

# Compilar modelo
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Entrenar
model.fit(x_train, y_train, epochs=5, validation_split=0.1)

# Evaluar
test_loss, test_acc = model.evaluate(x_test, y_test)
print("Precisión en test:", test_acc)

# Guardar modelo
model.save("mi_modelo.h5")
print("Modelo guardado como mi_modelo.h5")
