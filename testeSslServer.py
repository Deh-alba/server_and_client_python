import socket
import ssl

TCP_IP = 'localhost'
TCP_PORT = 30000
BUFFER_SIZE = 1024


def myreceive(connstream, EOFChar='\036'):
    msg = ''
    MSGLEN = 100
    # print("oi 1")
    while len(msg) < MSGLEN:
        # print("oi while")

        chunk = connstream.recv(MSGLEN-len(msg))
        print(chunk)
        if chunk.find(EOFChar) != -1:
            msg = msg + chunk
            # print(chunk)
            return msg
            # print(chunk)
            msg = msg + chunk
            if msg == '':
                msg = None
        # print("oi 2")
        return msg

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="ssl.crt", keyfile="ssl.key")

bindsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bindsocket.bind((TCP_IP, TCP_PORT))
bindsocket.listen(5)

while True:
    newsocket, fromaddr = bindsocket.accept()
    connstream = context.wrap_socket(newsocket, server_side=True)
    try:
        print("oi 1")
        myreceive(connstream)
        print("oi fim")
    finally:
        connstream.shutdown(socket.SHUT_RDWR)
        connstream.close()
