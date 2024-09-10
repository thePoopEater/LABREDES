import ssl
import socket
from dnslib import DNSRecord, DNSHeader, RR, A
import threading

# Configurar el contexto SSL con certificados
context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
context.load_cert_chain(certfile="certificate.pem", keyfile="private_key.pem")

# Función para manejar consultas DNS
def handle_client(connection, address):
    try:
        data = connection.recv(1024)  # Leer la consulta DNS
        if data:
            query = DNSRecord.parse(data)  # Decodificar la consulta
            print(f"Consulta DNS de {address}: {query.q.qname}")

            # Crear una respuesta DNS (aquí estamos respondiendo con una IP fija)
            reply = DNSRecord(DNSHeader(id=query.header.id, qr=1, aa=1, ra=1),
                              q=query.q)
            reply.add_answer(RR(query.q.qname, rdata=A("93.184.216.34")))

            # Enviar la respuesta DNS
            connection.sendall(reply.pack())
    except Exception as e:
        print(f"Error: {e}")
    finally:
        connection.close()

# Crear el socket TCP para escuchar en el puerto 853
with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as sock:
    sock.bind(('0.0.0.0', 853))
    sock.listen(5)
    print("Servidor DNS sobre TLS escuchando en el puerto 853")

    # Aceptar conexiones y manejar consultas
    with context.wrap_socket(sock, server_side=True) as ssock:
        while True:
            client_conn, client_addr = ssock.accept()
            threading.Thread(target=handle_client, args=(client_conn, client_addr)).start()
