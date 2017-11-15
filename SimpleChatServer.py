from socket import socket, AF_INET, SOCK_STREAM
import threading, tkinter, queue

#-----Define Global Variables-----#
sem = threading.Semaphore(30)
pool = []
c_sockets = []
count = 0 # Client Indicator
HOST = ''
PORT = 10000

#-----Define function-----#
def run_client(new_sock, new_addr, count, c_sockets):
    try:
        for socket in c_sockets:
            socket.sendall(("From %s, User %d Connected." % (new_addr[0], count)).encode('utf-8'))
        print("From %s, User %d Connected." % (new_addr[0], count))
        new_sock.sendall(("Successfully connected to the server. \n You are 'User %d.'" % count).encode('utf-8'))
        while True:
            msg = new_sock.recv(1000).decode('utf-8')
            # if not msg: continue
            if msg == 'quit':
                # new_sock.sendall('quit'.encode('utf-8'))
                print("User %d disconnected." % count)
                c_sockets.remove(new_sock)
                for socket in c_sockets:
                    socket.sendall(("User %d is disconnected." % count).encode('utf-8'))
                exit(0)
            to_all_msg = "User %d : %s" % (count,msg)
            print(to_all_msg)
            for socket in c_sockets:
                socket.sendall(to_all_msg.encode('utf-8'))
    except Exception as e:
        print(e)
        if new_sock in c_sockets:
            print("User %d disconnected." % count)
            c_sockets.remove(new_sock)
        for socket in c_sockets:
            socket.sendall(("User %d is disconnected." % count).encode('utf-8'))
        exit(0)

#-----Network Ready-----#
s = socket(AF_INET, SOCK_STREAM)
s.bind((HOST,PORT))
s.listen()

#----Main-----#
while True:
    try:
        c_sock, c_addr = s.accept()
        c_sockets.append(c_sock)
        sem.acquire(); count+=1; sem.release()
        c_thread = threading.Thread(target=run_client,args=(c_sock, c_addr, count, c_sockets))
        c_thread.start()
        pool.append(c_thread)
    except Exception as e:
        print(e)
        for thread in pool:
            thread.join()
        continue