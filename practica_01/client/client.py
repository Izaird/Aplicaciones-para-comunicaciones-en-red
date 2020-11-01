from tkinter import *
from PIL import ImageTk, Image
import socket 
import threading



def thread_interface():
    root = Tk()
    root.title('Servidor archivos')
    root.mainloop()


def thread_socket():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((socket.gethostname(), 5001))
    full_msg = ''
    while True:
        msg = s.recv(8)
        if len(msg) <= 0:
            break
    full_msg += msg.decode("utf-8")
    print(msg.decode("utf-8"))




if __name__ == "__main__":
    interface = threading.Thread(target=thread_interface)
    interface.start()
    socket_server = threading.Thread(target = thread_socket)
    socket_server.start()
    print("xd")