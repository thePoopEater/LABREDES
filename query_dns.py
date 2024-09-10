import ssl
import socket
from dnslib import DNSRecord

# IP de tu servidor DNS en la máquina virtual
SERVER_IP = '192.168.0.10'  # Reemplaza con la IP de tu máquina virtual
PORT = 853

# Dominio que quieres consultar
domain = 'example.com'

# Construir la consulta DNS
query = DNSRecord.question(domain)

# Convertir la consulta DNS a bytes
query_data = query.pack()

# Configurar la conexión SSL para DoT
context = ssl.create_default_context()

# Crear una conexión SSL sobre TCP
with socket.create_connection((SERVER_IP, PORT)) as sock:
    with context.wrap_socket(sock, server_hostname=SERVER_IP) as ssock:
        # Enviar la consulta DNS
        ssock.sendall(query_data)
        
        # Leer la respuesta (máximo 1024 bytes)
        response = ssock.recv(1024)

# Decodificar y mostrar la respuesta DNS
dns_response = DNSRecord.parse(response)
print(dns_response)
