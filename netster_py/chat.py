import sys
import socket
import select
import threading
import os


def chat_server(iface:str, port:int, use_udp:bool) -> None:
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
        tcp_connect(server,hostIP)
    else:
        udp_connect(server,hostIP)

def udp_connect(server,hostIP):
    server.bind(hostIP)

    while True:
        msg = server.recvfrom(256)
        message = msg[0].decode().lstrip()
        message = message.rstrip()
        addr =  msg[1]
        print("got message from ", addr)
        if message:
            if message == "hello":
                try:
                    world = "world\n".encode()
                    server.sendto(world, addr)
                except:
                    server.close()
                    break
            elif message == "goodbye":
                try:
                    word = "farewell\n"
                    word = word.encode()
                    server.sendto(word, addr)
                except:
                    server.close()
                    break
            elif message == "exit":
                try:
                    word = "ok\n"
                    word = word.encode()
                    server.sendto(word, addr)
                    os._exit(0)
                except:
                    print("ok")
                    server.close()
            else:
                try:
                    message  = message + "\n"
                    server.sendto(message.encode(), addr)
                except:
                    server.close()


def tcp_connect(server,hostIP):

    server.bind(hostIP)
    server.listen(250)
    i = 0
    while True:
        conn, addr = server.accept()
        print ('connection',i,'from',addr)
        i+=1
        server_thread = threading.Thread(target=tcpThread,args=(server,conn,addr))
        server_thread.start()

def tcpThread(server,conn,addr):
    while True:
        message = conn.recv(256)
        message = message.decode().lstrip()
        message = message.rstrip()
        print("got message from ", addr)
        if message:
            if message == "hello":
                try:
                    world = "world\n".encode()
                    conn.send(world)
                except:
                    conn.close()
                    break
            elif message == "goodbye":
                try:
                    word = "farewell\n"
                    conn.send(word.encode())
                    conn.close()
                    break
                except:
                    conn.close()
                    break
            elif message == "exit":
                try:
                    word = "ok\n"
                    conn.send(word.encode())
                    conn.close()
                    os._exit(0)
                except:
                    server.close()
                    break
            else:
                try:
                    message = message+ "\n"
                    conn.send(message.encode())
                except:
                    conn.close()

def chat_client(host:str, port:int, use_udp:bool) -> None:
    print("Hello, I am a client")
    
    client = None
    if not use_udp:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        IP = socket.getaddrinfo(host,port)
        hostIP = IP[0][4]
        client.connect(hostIP)
        tcp_conneection(client)
    else:
        client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        IP = socket.getaddrinfo(host,port)
        hostIP = IP[0][4]
        udp_connection(client,hostIP)

def udp_connection(client,hostIP):
    while True:
        userInput = sys.stdin.readline().lstrip()
        userInput = userInput.rstrip()
        client.sendto(userInput.encode(), hostIP)
        sys.stdout.flush()
        output = client.recv(256).decode().lstrip()
        output = output.rstrip()
        print(output)
        if output == "ok" or output == "farewell":
            client.close()
            break


def tcp_conneection(client): 
    while True:
        userInput = sys.stdin.readline().lstrip()
        userInput = userInput.rstrip()
        client.send(userInput.encode())
        sys.stdout.flush()
        output = client.recv(256).decode().lstrip()
        output = output.rstrip()
        print(output)
        if output == "ok" or output == "farewell":
            client.close()
            break

