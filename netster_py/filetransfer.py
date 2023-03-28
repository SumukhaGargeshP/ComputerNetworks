from typing import BinaryIO
import sys
import socket
import os

def file_server(iface:str, port:int, use_udp:bool, fp:BinaryIO) -> None:
    print("Hello, I am a server")
    server = None
    if not use_udp:
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

    else:
        server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    IP = socket.getaddrinfo(iface,port)
    hostIP = IP[0][4]


    if not use_udp:
        tcp_connect(server,hostIP,fp.name)
    else:
        udp_connect(server,hostIP,fp.name)

def tcp_connect(server,hostIP,fp):

    server.bind(hostIP)
    server.listen(250)
    f = open(fp, "wb")
    conn, addr = server.accept()
    while True:
        fileSend = conn.recv(256)
        if not fileSend:
            break
        f.write(fileSend)
    f.close()
    conn.close()
    server.close()
   
def udp_connect(server,hostIP,fp):
    server.bind(hostIP)
    f = open(fp, "wb")
    while True:
        packet = server.recvfrom(256)
        data = packet[0]
        addr = packet[1]
        if data == b"":
            break
        f.write(data)
    f.close()
    server.close()


def file_client(host:str, port:int, use_udp:bool, fp:BinaryIO) -> None:
    print("Hello, I am a client")
    client = None
    if not use_udp:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        IP = socket.getaddrinfo(host,port)
        hostIP = IP[0][4]
        client.connect(hostIP)
        tcp_conneection(client,fp)
    else:
        client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        IP = socket.getaddrinfo(host,port)
        hostIP = IP[0][4]
        udp_connection(client,hostIP,fp)


def tcp_conneection(client,fp):
    file_send  = open(fp.name,"rb")
    while True:
        content = file_send.read(256)
        if not content:
            break
        client.send(content)
    file_send.close()
    client.close()
    

def udp_connection(client,hostIP,fp):
    file_send = open(fp.name,"rb")

    while True:
        content = file_send.read(256)
        if not content:
            client.sendto(b"",hostIP)
            break
        client.sendto(content,hostIP)

    file_send.close()
    client.close()
