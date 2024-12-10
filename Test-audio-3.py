 import pyaudio
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

# Parámetros de grabación
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# Inicializar PyAudio
audio = pyaudio.PyAudio()

# Abrir stream de entrada
stream_input = audio.open(format=FORMAT,
                              channels=CHANNELS,
                              rate=RATE,
                              input=True,
                              frames_per_buffer=CHUNK)

# Definir la arquitectura de la CNN
model = Sequential()
model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(1024, 1, 1)))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Conv2D(128, (3, 3), activation='relu'))
model.add(MaxPooling2D((2, 2)))
model.add(Flatten())
model.add(Dense(128, activation='relu'))
model.add(Dense(10, activation='softmax'))

# Compilar el modelo
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

while True:
    # Leer audio desde el stream de entrada
    data = np.frombuffer(stream_input.read(CHUNK), dtype=np.int16)

    # Convertir audio a valores que puedan ser leídos por la CNN
    valores = data.astype(np.float32) / 32768.0
    valores = valores.reshape((1, 1024, 1, 1))

    # Pasar los valores por la CNN
    atributos = model.predict(valores)

    # Imprimir los atributos extraídos
    print(atributos)

# Cerrar streams y PyAudio
stream_input.stop_stream()
stream_input.close()
audio.terminate()
