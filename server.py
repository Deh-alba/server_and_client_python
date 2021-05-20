#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import ssl
import time
import os
import json
from threading import Thread
from pprint import pprint
# from sendfile import sendfile
# from SocketServer import ThreadingMixIn

TCP_IP = '172.17.0.2'
TCP_PORT = 30000
BUFFER_SIZE = 1024


class ServerThread(Thread):

    def __init__(self, ip, port, context, sock=None):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        # connstream = context.wrap_socket(newsocket, server_side=True)
        if sock is None:
            aux = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock = context.wrap_socket(aux, server_side=True)
        else:
            # self.sock = sock
            self.sock = context.wrap_socket(sock, server_side=True)

    # receive file
    def receiveFile(self):

        data = self.sock.recv(BUFFER_SIZE)

        with open('testing.js', 'wb') as f:

            if not data:
                f.close()

            f.write(data)
        f.close()

        print('Successfully get the file')

    # receive dependencies
    def receiveFileDependencies(self):

        data = self.sock.recv(BUFFER_SIZE)

        with open('package.json', 'wb') as f:
            # print ('file opened')
            if not data:
                f.close()
                # self.sock.shutdown(socket.SHUT_WR)
                print ('file close()')
                # write data to a file
            f.write(data)
        f.close()
        # return 200
        print('Successfully get the file')

    # run node install, node file and get output 
    def runnigFile(self):

        os.system("npm install")
        a = os.popen("node testing.js").readlines()

        return a[0]

    # receibe client message
    def myreceive(self, EOFChar='\036'):
        msg = ''
        MSGLEN = 100
        # print(msg)
        while len(msg) < MSGLEN:

            chunk = self.sock.recv(MSGLEN-len(msg)).decode('utf-8')
            if chunk.find(EOFChar) != -1:
                msg = msg + chunk
                # print(chunk)
                return msg
            # print(chunk)
            msg = msg + chunk
            if msg == '':
                msg = None
            return msg

    # send message for client
    def mysend(self, msg):
        totalsent = 0
        MSGLEN = len(msg)
        # print(msg)
        while totalsent < MSGLEN:
            sent = self.sock.send(msg[totalsent:].encode('utf-8'))
            if sent == 0:
                raise RuntimeError("socket connection broken")

            totalsent = totalsent + sent

    # authneticate
    def autentica(self):
        print("------------- User authentication -------------\n")

        # Opens the file expected from the client and saves the information
        # of 'usuario' and 'senha' for user authentication
        with open('user.json') as user_info:
            username = json.load(user_info)

        client_user = username["user"][0]["usuario"]
        client_password = username["user"][0]["senha"]

        # Opens the file with all users and their passwords
        with open('userlist.json') as user_list:
            users = json.load(user_list)

        # Go through userlist.json for validation
        for i in range(4):
            # Checks if the user is on the list
            if(client_user == users["userlist"][i]["usuario"]):
                # once the user is found, checks its password
                if (client_password == users["userlist"][i]["senha"]):
                    print("It's a match!")
                    print("User successfully authenticated.")
                    print("---------------------------------------------")
                    return "ok"
                else:
                    # wrong password
                    print("wrong password")
                    print("---------------------------------------------")
                    return "password error" # Todo - return error number

    # close connection with client
    def quit(self):
        print("return close running")
        self.sock.close()

    def run(self):

        # receve commands
        comand = self.myreceive()

        if comand[:5] == "user":
            
            retorno = self.autentica()

            if retorno == "ok":

                # send return for client
                self.mysend("ok")

                # receive dependencies 
                self.receiveFileDependencies()

                # receive execution file
                self.receiveFile()

                # install dependencies and execut file js
                retur = self.runnigFile()

                # return result of execution for client
                self.mysend(retur)

                # close connection
                self.quit()

        else:
            self.mysend("erro")
            quit()

        # Usar https e ssl- segurança

context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
context.load_cert_chain(certfile="ssl.crt", keyfile="ssl.key")

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []
tcpsock.listen(4)

while True:

    print ("Waiting connections...")

    connection, addres = tcpsock.accept()
    newthread = ServerThread(TCP_IP, addres, context, connection)
    newthread.start()

    threads.append(newthread)


for t in threads:
    t.join()
