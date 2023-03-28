from typing import BinaryIO
import sys
import socket
import os

def stopandwait_server(iface:str, port:int, fp:BinaryIO) -> None:
    print("Hello, I am a server")
    server = None
    server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    IP = socket.getaddrinfo(iface,port)
    hostIP = IP[0][4]
    udp_connect(server,hostIP,fp.name)
    server.close()
    pass

def udp_connect(server,hostIP,fp):
    server.bind(hostIP)
    f = open(fp, "wb")
    while True:
        packet = server.recvfrom(1024)
        data = packet[0]
        addr = packet[1]
        actdata = data[1:]
        if actdata == b'':
            server.sendto(str(data[0]).encode(),addr)
            break
        f.write(actdata)
        server.sendto(str(data[0]).encode(),addr)
    f.close()

def stopandwait_client(host:str, port:int, fp:BinaryIO) -> None:
    print("Hello, I am a client")
    client = None
    client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    IP = socket.getaddrinfo(host,port)
    hostIP = IP[0][4]
    udp_connection(client,hostIP,fp)
    client.close()
    pass


def udp_connection(client,hostIP,fp):
    file_send = open(fp.name,"rb")
    read = True
    seq = b"0"
    client.settimeout(0.065)
    while True:
        if read:
            content = file_send.read(1023)
            if not content:
                read = False
                content = seq + content
                client.sendto(content,hostIP)
                try:
                    data = client.recvfrom(1024)
                    ack = data[0]
                    if int(ack) == ord(seq):
                        break
                except:
                    client.sendto(content,hostIP)
                    client.sendto(content,hostIP)
                    client.sendto(content,hostIP)
                    break
            else:
                read = False
                content = seq + content
                client.sendto(content,hostIP)
                try:
                    data = client.recvfrom(1024)
                    ack = data[0]
                    if int(ack) == ord(seq):
                        read = True
                except:
                    pass
        else:
            read = False
            client.sendto(content,hostIP)
            try:
                data = client.recvfrom(1024)
                ack = data[0]
                if int(ack) == ord(seq):
                    seq = str(1 - int(seq.decode())).encode()
                    read = True
            except:
                pass

    file_send.close()
