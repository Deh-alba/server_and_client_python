import socket
import ssl

TCP_IP = 'localhost'
TCP_PORT = 30000
BUFFER_SIZE = 1024


def mysend(conn, msg):
    totalsent = 0
    MSGLEN = len(msg)
    print(msg)
    while totalsent < MSGLEN:
        sent = conn.send(msg[totalsent:])
        if sent == 0:
            raise RuntimeError("socket connection broken")

        totalsent = totalsent + sent
    print(totalsent)

context = ssl.create_default_context()
context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
context.verify_mode = ssl.CERT_REQUIRED
context.check_hostname = True
context.load_verify_locations("ssl.crt")
aux = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn = context.wrap_socket(aux, server_hostname=TCP_IP)
conn.connect((TCP_IP, TCP_PORT))
# cert = conn.getpeercert()
# pprint.pprint(cert)
print("oi 1")
mysend(conn, "HEAD")
print("oi 2")
