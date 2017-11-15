from src.configure import HOST
from socket import socket, AF_INET, SOCK_STREAM
import threading
import tkinter as tk


# Thread class to connect with server
class Connector(threading.Thread):
    def __init__(self, text):
        threading.Thread.__init__(self)
        self.text = text
        self.HOST = HOST
        self.PORT = 10000
        self.s = socket(AF_INET,SOCK_STREAM)
        self.s.connect((self.HOST, self.PORT))

    def run(self):
        try:
            while True:
                msg = self.s.recv(1000).decode('utf-8')
                self.text.insert('end',msg)
                self.text.insert('end','\n')
        except Exception as e:
            print(e)

    def get_socket(self):
        return self.s

# Main GUI class using tkinter
class ChatClient(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)

        #GUI definitions
        self.top_frame = tk.Frame(self,width=100); self.top_frame.pack()
        self.change_button = tk.Button(self.top_frame,text='Start Chat',command=self.start_and_quit_chat,background='green2')
        self.change_button.pack(side='left')
        self.msg_label = tk.Label(self.top_frame,text='Message : '); self.msg_label.pack(side='left')
        self.entry = tk.Entry(self.top_frame,bd=5,width=40); self.entry.pack(side='left')
        self.entry.bind('<Return>',self.send_msg_by_enter)
        self.send_button = tk.Button(self.top_frame,text='Send',command=self.send_msg, state='disabled')
        self.send_button.pack(side='left')

        self.bottom_frame = tk.Frame(self,width=100); self.bottom_frame.pack()
        self.text = tk.Text(self.bottom_frame); self.text.pack()
        self.text.insert('end','Messages will be printed here...\n')

        #Other definitions
        self.threads = []

    # Start & Quit button Event Handler
    def start_and_quit_chat(self):
        if self.change_button.cget('text') == 'Start Chat':
            self.send_button.configure(state='normal')
            self.change_button.configure(text='Quit Chat',background='red')
            self.t = Connector(self.text)
            self.t.daemon=True
            self.t.start()
            self.threads.append(self.t)
        else:
            self.send_quit_msg()
            self.destroy()
            exit(0)

    def send_msg(self):
        s = self.t.get_socket()
        msg = self.entry.get()
        encoded_msg = msg.encode('utf-8')
        try:
            s.sendall(encoded_msg)
        except Exception as e:
            print(e)

        self.entry.delete(0,'end')

        if(msg=='quit'): exit(0)

    def send_msg_by_enter(self, event):
        s = self.t.get_socket()
        msg = self.entry.get()
        encoded_msg = msg.encode('utf-8')
        try:
            s.sendall(encoded_msg)
        except Exception as e:
            print(e)

        self.entry.delete(0, 'end')

        if(msg=='quit'): exit(0)

    def send_quit_msg(self):
        s = self.t.get_socket()
        encoded_msg = 'quit'.encode('utf-8')
        try:
            s.sendall(encoded_msg)
            exit(0)
        except Exception as e:
            print(e)

if __name__ =='__main__':
    my_app = ChatClient()
    my_app.mainloop()

    # for t in my_app.threads:
    #     t.join()
