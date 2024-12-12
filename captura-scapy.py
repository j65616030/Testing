from scapy.all import *
import csv
import psutil

def process_packet(packet):
    """
    Procesa un paquete capturado y extrae la información relevante.

    Args:
        packet: Un objeto Scapy representando el paquete capturado.
    """

    # Extraer información del paquete
    timestamp = packet.time
    memoria = psutil.virtual_memory().percent
    try:
        fuente = packet[IP].src
        destino = packet[IP].dst
    except IndexError:
        # Manejar casos donde no hay capa IP (por ejemplo, paquetes ARP)
        fuente = "N/A"
        destino = "N/A"
    protocolo = packet.proto
    longitud_paquete = len(packet)
    numero_paquete = capture.count()
    datos_paquete = str(packet[Raw].load)

    # Escribir datos en el archivo CSV
    with open('captura.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, memoria, fuente, destino, protocolo, longitud_paquete, numero_paquete, datos_paquete])

    # Identificar y guardar contenido HTML o JavaScript
    if b'<html>' in datos_paquete:
        # Guardar los datos en un archivo HTML
        with open('index.html', 'wb') as f:
            f.write(datos_paquete)
    elif b'<script>' in datos_paquete:
        # Guardar los datos en un archivo JavaScript
        with open('script.js', 'wb') as f:
            f.write(datos_paquete)

# Capturar paquetes en la interfaz 'wlan0' y procesarlos
capture = sniff(iface="wlan0", prn=process_packet)
