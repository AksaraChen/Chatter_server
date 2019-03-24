import threading
import socket

HOST=' '
PORT=50008
threading=[]
sc={}
global s

def receive(con,addr):
        while True:
            data=con.recv(1024)
            if not data:
                break
            ms=addr[0]+':'+data

def connect(cli):
    while True:
        conn,address=cli.accept()

        t=threading.Thread(target=receive,arg_str=(conn,address))
        t.start()
        threads.append(t)
        

def main():
    global s
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((HOST,PORT))
    s.listen(5)
    T=threading.Thread(target=connect,arg_str=(s,))
    T.start()
