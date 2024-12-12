import pyshark
import csv
import datetime
import psutil
import os

# Especificar el path de TShark
tshark_path = '/usr/local/bin/tshark'

# Crear un objeto LiveCapture con el path de TShark
capture = pyshark.LiveCapture(interface='wlan0', tshark_path=tshark_path)

# Creación del archivo CSV
csv_file = 'captura.csv'
with open(csv_file, 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['Timestamp', 'Memoria', 'Fuente', 'Destino', 'Protocolo', 'Longitud del paquete', 'Número de paquete', 'Datos del paquete'])  # Encabezado

try:
    # Ciclo para procesar los paquetes capturados
    for packet in capture:
        timestamp = packet.timestamp
        memoria = psutil.virtual_memory().percent
        fuente = packet.ip.src
        destino = packet.ip.dst
        protocolo = packet.transport_layer
        longitud_paquete = packet.length
        numero_paquete = capture.packet_number
        datos_paquete = packet.payload

        # Escritura de los datos en el archivo CSV
        with open(csv_file, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([timestamp, memoria, fuente, destino, protocolo, longitud_paquete, numero_paquete, datos_paquete])

        # Identificar el tipo de contenido
        if b'<html>' in datos_paquete:
            # Guardar los datos en un archivo HTML
            with open('index.html', 'wb') as f:
                f.write(datos_paquete)

            # Abrir el archivo en un navegador
            os.startfile('index.html')
        elif b'<script>' in datos_paquete:
            # Guardar los datos en un archivo JavaScript
            with open('script.js', 'wb') as f:
                f.write(datos_paquete)

            # Abrir el archivo en un navegador
            os.startfile('script.js')
        else:
            print(f'Timestamp: {timestamp}, Memoria: {memoria}%, Fuente: {fuente}, Destino: {destino}, Protocolo: {protocolo}, Longitud del paquete: {longitud_paquete}, Número de paquete: {numero_paquete}, Datos del paquete: {datos_paquete}')

except Exception as e:
    print(f'Error: {e}')
