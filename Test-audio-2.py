import pyaudio
import numpy as np

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

# Abrir stream de salida
stream_output = audio.open(format=FORMAT,
                              channels=CHANNELS,
                              rate=RATE,
                              output=True)

while True:
    # Leer audio desde el stream de entrada
    data = np.frombuffer(stream_input.read(CHUNK), dtype=np.int16)

    # Convertir audio a valores que puedan ser leídos por una red neuronal
    valores = data.astype(np.float32) / 32768.0

    # Seleccionar elementos al azar con una función específica
    indices_seleccionados = np.random.choice(len(valores), size=int(0.5 * len(valores)), replace=False)
    valores_seleccionados = valores[indices_seleccionados]

    # Multiplicar al cuadrado los elementos seleccionados
    valores_seleccionados_al_cuadrado = valores_seleccionados ** 2

    # Rearmar el audio
    audio_rearmado = np.zeros_like(valores)
    audio_rearmado[indices_seleccionados] = valores_seleccionados_al_cuadrado

    # Escalar el audio rearmado para que esté en el rango de 16 bits
    audio_rearmado_16_bits = (audio_rearmado * 32768.0).astype(np.int16)

    # Reproducir el audio rearmado
    stream_output.write(audio_rearmado_16_bits.tobytes())

# Cerrar streams y PyAudio
stream_input.stop_stream()
stream_input.close()
stream_output.stop_stream()
stream_output.close()
audio.terminate()
