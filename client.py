#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import json
import os
import ssl
# from sendfile import sendfile


TCP_IP = '172.17.0.2'
TCP_PORT = 30000
BUFFER_SIZE = 1024


class Client:

    def __init__(self, sock=None):
        # self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        context = ssl.create_default_context()
        context = ssl.SSLContext(ssl.PROTOCOL_SSLv23)
        context.verify_mode = ssl.CERT_REQUIRED
        context.check_hostname = True
        context.load_verify_locations("ssl.crt")

        if sock is None:
            aux = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s = context.wrap_socket(aux, server_hostname=TCP_IP)
        else:

            self.s = context.wrap_socket(sock, server_hostname=TCP_IP)

    # Sendo data fron server.
    def sendCommandServer(self, command):
        self.s.send(command.encode())

    def recevCommandServer(self):
        retorno = self.s.recv(BUFFER_SIZE).decode()
        self.s.close()
        return retorno

    def clientThreadConnect(self):
        self.s.connect((TCP_IP, TCP_PORT))

    def clienteReconnect(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def clientThreadCloseConection(self):
        self.s.close()

    def send(self, msg):
        totalsent = 0
        MSGLEN = len(msg)
        # print(msg)
        while totalsent < MSGLEN:
            sent = self.s.send(msg[totalsent:].encode('utf-8'))
            if sent == 0:
                raise RuntimeError("socket connection broken")

            totalsent = totalsent + sent

    def receive(self, EOFChar='\036'):
        msg = ''
        MSGLEN = 100
        while len(msg) < MSGLEN:

            chunk = self.s.recv(MSGLEN-len(msg)).decode('utf-8')
            if chunk.find(EOFChar) != -1:
                msg = msg + chunk
                # print(chunk)
                return msg
            # print(chunk)
            msg = msg + chunk
            return msg

    def sendArquive(self, filename):
        f = open(filename, 'rb')
        self.s.sendfile(f)
        print('Successfully put the file')

print ("====================================")
print ("")
print ("Iniciando cliente.... ")
print ("")
# print (socket.gethostbyaddr('10.13.239.210'))

cliente = Client()
# conect client
cliente.clientThreadConnect()
# send commando for autenticate
cliente.send("user")
# receive return
retorno = cliente.receive()

if retorno == "ok":

    filename = "test.js"
    fileDependencies = "pack.json"
    # send file for dependencies
    cliente.sendArquive(fileDependencies)
    # send file for execution
    cliente.sendArquive(filename)
    # receive return 
    retorno = cliente.receive()
    print(retorno)

    # close connection
    cliente.clientThreadCloseConection()

else:
    print(retorno)
    cliente.clientThreadCloseConection()

# quit
quit = 1    



while quit != 1:
    print ("====================================")
    print ("")
    print ("Chose intstuction:")
    print ("")
    print ("USER - user myfile.json")
    print ("SEND - send myfile.js")
    print ("RUN  - run")
    print ("QUIT - quit")
    print ("")
    print ("====================================")
    print ("")

    entrada = input("Digit your option: ")
    print ("")

    # Analisa os 5 primeiros caracteres e confere se o que foi digitado
    # pelo usuário corresponde aos comandos aceitos.
    if entrada[:5] == "user ":

        # Contecta no servidor
        cliente.clientThreadConnect()

        # Verifica se o arquivo de entrada possui a extensão json
        if entrada[len(entrada)-5:] == ".json":
            print ("Login in server...")
            print ("")
            user_login = entrada[5:]
            print ("====================================")
            print ("")
            print ("File sent: ", user_login)
            print ("")
            # cliente.clientThreadConnect()


            # TODO autenticar usuário de acordo com o arquivo userlist.json
            # Autenticacao direta - deve ser enviado arquivo chamado user.json
            with open(user_login) as f:
                json_dict = json.load(f)
                users = json_dict["userlist"]
                for item in users:
                    if item["usuario"] == "grupo01" and item["senha"] == "01234":
                        print("grupo01 autenticado")
                    elif item["usuario"] == "grupo02" and item["senha"] == "12345":
                        print("grupo02 autenticado")
                    elif item["usuario"] == "grupo03" and item["senha"] == "23456":
                        print ("grupo03 autenticado")
                    elif item["usuario"] == "grupo04" and item ["senha"] == "34567":
                        print ("grupo04 autenticado")
                    else:
                        print ("")
                        print ("Usuário/senha inválido(s), verifique \nseu arquivo .json e envie-o novamente.")
            print ("")
        else:
            print("[ERRO 303] - Arquivo em formato inválido.")
    # SEND
    elif entrada[:5] == "send ":
        # manda string para o servidor
        entrada = "send test.js"

        #print("valida 1")
        cliente.sendCommandServer(entrada[:5])
        #print("valida 2")
        validate = cliente.recevCommandServer()
        validate = "ok"
        # Verifica se é um arquivo no formato JS
        #print("valida 3")

        if validate == "ok":
            #print("valida 3")
            if entrada[len(entrada)-3:] == ".js":
                # Pega o nome do arquivo enviado para validação
                filename = entrada[5:]
                print (filename)
                # Pega as informações referentes ao arquivo
                filestat = os.stat(filename)
                # print (filestat)
                filesize = filestat.st_size
                print ("This file has", filesize, "bytes.")
                if filesize > 3000000:     # TODO maior que 2Mb descarta
                    print ("The file is too large.")
                else:
                    print ("Size correct.")
                    cliente.clientThreadSendFile(filename)

                    # cliente.clientThreadCloseConection()

    # RUN
    elif entrada == "run":

        print ("====================================")
        print ("")
        print ("Trying to run application...")
        print ("")
        cliente.sendCommandServer("run")
        # print("parou 1")
        cliente.recevCommandServer()
        # print("parou 2")
        # insert return here
    # QUIT
    elif entrada == "quit":
        print ("====================================")
        print ("")
        print ("Closing client!")
        print ("")
        print ("====================================")
        cliente.sendCommandServer("quit")
        cliente.clientThreadCloseConection()
        quit = 1
    else:
        print ("====================================")
        print ("")
        print ("inválid command")
        print ("")
