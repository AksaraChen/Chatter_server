import threading
import socket
import sys

HOST=' '
PORT=50000
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
def recieve_send(conn_1,address_1):                         #conn_1為寄出方
    while True:
        try:
            data=conn_1.recv(1024)                    #收到conn_1寄出的訊息
            if data==str.encode("ID_register"):
                register(conn_1,address_1)
                continue
            elif data==str.encode("\myip"):
                ask_for_ip(address_1,address_1)
                continue
            elif data==str.encode("\herip"):
                temp=0
                for key in ID:
                    temp+=1
                if temp==1:
                    ask_for_ip()
                else:
                    for key in sc:                                
                        if key==address_1:                        
                            continue
                        ask_for_ip(address_1,key)
                continue
        except:
            print("\nLost connection")
            break
        temp=0
        for key in ID:
            temp+=1
        if temp==1:
            sc[address_1].send(str.encode("現在只有一個用戶"))
        else:
            for key in sc:                                #由於最多只會有兩個client，因此使用for loop將所有的client都發一遍
                if key==address_1:                        #跳過自己
                    continue
                sc[key].send(data)

def ask_for_ip(addr_1,addr_2):
    sc[addr_1].send(str.encode(addr_2[0]+str(addr_2[1])+":"+str(ID[addr_2])+"\n"))
def connect(cli):
    while True:
        conn,address=cli.accept()#在收到連線要求後准許連線，conn為client產生出的socket物件，address為客戶端地址
        t=threading.Thread(target=recieve_send,args=(conn,address))
        t.start()
        threads.append(t)
        sc[address]=conn
        
   #發出訊息

def register(conn,address):
        try:
            data=conn.recv(1024)                    #收到conn_1寄出的訊息
        except:
            print("\nrecivev ID Error")
            exit()
        try:
            ID[address]=data
        except:
            print("\nRegister Error")
            exit()

def search(client_addr):
    try:
        return ID[client_addr]
    except:
        print("can't find user")
        exit()

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
            for key in ID:
                print(key[0]+str(key[1])+":"+str(ID[key])+"\n")
                temp_2+=1
            if temp_2==0:
                print("現在無任何已連線用戶\n")
        elif temp=='0':
            break
        else:
            print("錯誤的輸入，請重新輸入\n")
    sys.exit(0)

if __name__=='__main__':
    main()

        