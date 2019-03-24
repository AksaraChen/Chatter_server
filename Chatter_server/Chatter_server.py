import threading
import socket
import sys

HOST=' '
PORT=50008
threads=[]
sc={}
ID={}
global s,user_num


#def receive(conn,addr):
#        while True:
#            data=conn.recv(1024)
#            if not data:
#                break
#            ms=addr[0]+':'+data


def connect(cli):
    while True:
        conn,address=cli.accept()#在收到連線要求後准許連線，conn為client產生出的socket物件，address為客戶端地址
        print(address+"已成功連線\n")
        t=threading.Thread(target=receive,arg_str=(conn,address))
        t.start()
        threads.append(t)
        sc[addr]=conn
        
def recieve_send(conn_1,mes):                         #conn_1為寄出方，mes為傳遞之訊息
    while True:
        try:
            data=conn_1.recv(1024)                    #收到conn_1寄出的訊息
        except:
            print("Send Error")
        for key in sc:                                #由於最多只會有兩個client，因此使用for loop將所有的client都發一遍
            if key==conn_1.getsockname():             #跳過自己
                continue
            sc[key].send(conn_1.getsockname()+mes)    #發出訊息

def register(client_addr,id):
    while True:
        try:
            ID[client_addr]=id
        except:
            print("Register Error")

def search(client_addr):
    try:
        return ID[client_addr]
    except:
        print("can't find user")

def main():
    global s,user_num
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM) #設定socket的參數
    s.bind((HOST,PORT))                                #設定address跟port
    s.listen(2)                                        #最多同時連線2個
    T=threading.Thread(target=connect,args=(s,))    #透過threading來跑connect函式
    T.start()
    temp_2=0
    while True:
        temp=input("欲搜尋用戶ID請按1，欲離開請按0：")
        if temp=='1':
            if ID=={}:
                print("現在無任何已連線用戶\n2")
            for key in ID:
                print(key+":"+ID[key]+"\n")
                temp_2+=1
            user_num=temp_2
        elif temp=='0':
            sys.exit(0)
        else:
            print("錯誤的輸入，請重新輸入\n")

if __name__=='__main__':
    main()

        