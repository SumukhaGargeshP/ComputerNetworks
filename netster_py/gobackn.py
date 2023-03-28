from typing import BinaryIO
import sys
import socket
import os

def gbn_server(iface:str, port:int, fp:BinaryIO) -> None:
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
    ack = b"0"
    gobackn = True
    while gobackn:
        winPack = 0
        while True:
            packet = server.recvfrom(1024)
            dataFrame = packet[0]
            addr = packet[1]
            temp = dataFrame.split(b"-",2)
            seq = temp[0]
            l = int(temp[1].decode())
            data = temp[2]
            #print("expected","actual",ack,seq)
            if data == b'' and seq == ack:
                #seq = str(int(ack.decode()) +1).encode()
                ack_msg = b"ackF"
                data = seq + b"-"+ack_msg
                server.sendto(data,addr)
                server.sendto(data,addr)
                server.sendto(data,addr)
                server.sendto(data,addr)
                server.sendto(data,addr)
                server.sendto(data,addr)
                #ack = str(int(ack.decode()) +1).encode()
                gobackn = False
                break

            elif seq == ack:
                ack = str(int(seq.decode()) +1).encode()
                winPack +=1
                f.write(data)
                if winPack == l:
                    #ack = str(int(ack.decode()) +1).encode()
                    ackmsg = b"ack"
                    data = seq + b"-"+ackmsg
                    server.sendto(data,addr)
                    break
            else:
                print("expected","actual",ack,seq)
                #ack = str(int(ack.decode()) -1).encode()
                nack = b"nack"
                data = ack + b"-"+nack
                server.sendto(data,addr)
                break

    f.close()


def gbn_client(host:str, port:int, fp:BinaryIO) -> None:
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
    windowsize = 4
    f_data = []
    FinalWindowSize = 0
    f_content = file_send.read(1000)
    while f_content:
        f_data.append(f_content)
        f_content = file_send.read(1000)
        FinalWindowSize += 1
    fp.close()
    packW = 0
    seq_exp = b"0"
    emptycontent = True
    
    while packW < FinalWindowSize:
        print("*****************************************")
        for i in range(packW, min((packW+windowsize),FinalWindowSize)):
            data = f_data[i]
            data =  seq_exp + b"-" + str(windowsize).encode()+ b"-" + data
            print(seq_exp)
            print("----------------------")
            client.sendto(data,hostIP)
            seq_exp = str(int(seq_exp.decode()) +1).encode()

        
        client.settimeout(0.06)

        try:
            packet = client.recvfrom(1024)
            print(packet)
            temp = packet[0].split(b"-",1)
            msg = temp[1]
            seq = temp[0]

            print("---------------------------------",seq)
            if msg == b"ack":
                packW = int(seq.decode())+1
                windowsize+=1
                seq_exp = str(int(seq.decode()) +1).encode()
                client.settimeout(0)
            elif msg == b"ackF":
                client.settimeout(0)
                break
            
            else:
                print("NACK")
                if windowsize //2 >1:
                    windowsize =  windowsize //2
                print("fbbdubfdbfbifbdif",seq)
                packW = int(seq.decode())
                print(packW)
                seq_exp = str(int(seq.decode())).encode()
                client.settimeout(0)
        except socket.timeout:
            print("TIME")
            if windowsize //2 >1:
                windowsize =  windowsize //2
            seq_exp = str(packW).encode()
            continue

    msg = seq_exp +b"-" +b'1'+b"-"+b''
    client.sendto(msg,hostIP)
    client.sendto(msg,hostIP)
    client.sendto(msg,hostIP)
    client.sendto(msg,hostIP)
    client.sendto(msg,hostIP)
