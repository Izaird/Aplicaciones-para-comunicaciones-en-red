import socket
from tkinter import *
PORT = 5000
HOST = "127.0.0.1"

if __name__ == "__main__":

    root = Tk()
    root.title('Hang man')
    root.geometry('600x800')

    top = Toplevel()
    top.title('Chose a difficulty')


    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    s.connect((HOST,PORT))
    print('Connected to the server ...')
    

    root.mainloop()

