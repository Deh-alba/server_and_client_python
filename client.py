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
        return_server = self.s.recv(BUFFER_SIZE).decode()
        self.s.close()
        return return_server

    def clientThreadConnect(self):
        self.s.connect((TCP_IP, TCP_PORT))

    def clientReconnect(self):
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
print ("Iniciando client.... ")
print ("")
# print (socket.gethostbyaddr('10.13.239.210'))

client = Client()
# conect client
client.clientThreadConnect()
# send commando for autenticate
client.send("user")
# receive return
return_server = client.receive()

if return_server == "ok":

    filename = "test.js"
    fileDependencies = "pack.json"
    # send file for dependencies
    client.sendArquive(fileDependencies)
    # send file for execution
    client.sendArquive(filename)
    # receive return 
    return_server = client.receive()
    print(return_server)

    # close connection
    client.clientThreadCloseConection()

else:
    print(return_server)
    client.clientThreadCloseConection()

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

    entrance = input("Digit your option: ")
    print ("")

    # get and validate user command
    if entrance[:5] == "user ":

        # open connect with server
        client.clientThreadConnect()

        # test if the file is json
        if entrance[len(entrance)-5:] == ".json":
            print ("Login in server...")
            print ("")
            user_login = entrance[5:]
            print ("====================================")
            print ("")
            print ("File sent: ", user_login)
            print ("")
            


            # autenthicate user with user.json 
            # revise
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
                        print ("User or passwor invelid")
            print ("")
        else:
            print("[ERROR 303] - format invalid.")
    # SEND
    elif entrance[:5] == "send ":
        # send name file for server
        entrance = "send test.js"

        #print("valida 1")
        client.sendCommandServer(entrance[:5])
        #print("valida 2")
        validate = client.recevCommandServer()
        validate = "ok"
        # validate file
        #print("valida 3")

        if validate == "ok":
            #print("valida 3")
            if entrance[len(entrance)-3:] == ".js":
                # get namo for validation
                filename = entrance[5:]
                print (filename)
                # get information file
                filestat = os.stat(filename)
                
                filesize = filestat.st_size
                print ("This file has", filesize, "bytes.")
                # test file size
                if filesize > 3000000:     
                    print ("The file is too large.")
                else:
                    print ("Size correct.")
                    client.clientThreadSendFile(filename)

                    # client.clientThreadCloseConection()

    # RUN
    elif entrance == "run":

        print ("====================================")
        print ("")
        print ("Trying to run application...")
        print ("")
        client.sendCommandServer("run")
        # print("parou 1")
        client.recevCommandServer()
        # print("parou 2")
        # insert return here
    # QUIT
    elif entrance == "quit":
        print ("====================================")
        print ("")
        print ("Closing client!")
        print ("")
        print ("====================================")
        client.sendCommandServer("quit")
        client.clientThreadCloseConection()
        quit = 1
    else:
        print ("====================================")
        print ("")
        print ("inválid command")
        print ("")
