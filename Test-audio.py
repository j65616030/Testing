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

# Leer audio desde el stream de entrada
data = np.frombuffer(stream_input.read(CHUNK), dtype=np.int16)

# Convertir audio a características que pueden ser leídas por una red neuronal
fft = np.fft.fft(data)

# Reconstruir el audio a partir de la transformada de Fourier
audio_reconstruido_fft = np.real(np.fft.ifft(fft))

# Reproducir el audio reconstruido en el stream de salida
stream_output.write(audio_reconstruido_fft.astype(np.float32).tobytes())

# Cerrar streams y PyAudio
stream_input.stop_stream()
stream_input.close()
stream_output.stop_stream()
stream_output.close()
audio.terminate()
