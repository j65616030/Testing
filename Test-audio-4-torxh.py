import pyaudio
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim

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

# Definir la arquitectura de la red neuronal
class RedNeuronal(nn.Module):
    def __init__(self):
        super(RedNeuronal, self).__init__()
        self.conv1 = nn.Conv2d(1, 10, kernel_size=5)
        self.conv2 = nn.Conv2d(10, 20, kernel_size=5)
        self.conv2_drop = nn.Dropout2d()
        self.fc1 = nn.Linear(320, 50)
        self.fc2 = nn.Linear(50, 10)

    def forward(self, x):
        x = nn.functional.relu(nn.functional.max_pool2d(self.conv1(x), 2))
        x = nn.functional.relu(nn.functional.max_pool2d(self.conv2_drop(self.conv2(x)), 2))
        x = x.view(-1, 320)
        x = nn.functional.relu(self.fc1(x))
        x = self.fc2(x)
        return nn.functional.log_softmax(x, dim=1)

# Inicializar la red neuronal y el optimizador
red_neuronal = RedNeuronal()
optimizador = optim.SGD(red_neuronal.parameters(), lr=0.01)

while True:
    # Leer audio desde el stream de entrada
    data = np.frombuffer(stream_input.read(CHUNK), dtype=np.int16)

    # Convertir audio a valores que puedan ser leídos por la red neuronal
    valores = data.astype(np.float32) / 32768.0
    valores = valores.reshape((1, 1, 1024, 1))

    # Pasar los valores por la red neuronal
    salida = red_neuronal(torch.from_numpy(valores))

    # Seleccionar características específicas al azar
    indices_seleccionados = np.random.choice(len(salida[0]), size=5, replace=False)
    caracteristicas_seleccionadas = salida[0][indices_seleccionados]

    # Multiplicar y sumar las características seleccionadas
    resultado = torch.sum(caracteristicas_seleccionadas ** 2)

    # Imprimir el resultado
    print(resultado.item())

# Cerrar streams y PyAudio
stream_input.stop_stream()
stream_input.close()
audio.terminate()
