from tkinter import *
from PIL import ImageTk, Image
import socket 
from os import listdir, walk 
from pathlib import Path



if __name__ == "__main__":
    PORT = 5000
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((socket.gethostname(),PORT))
    s.listen()
    print("Waiting for clients ...")
    while True:
        clientsocket, address = s.accept()
        with clientsocket:
            print(f"Connection from {clientsocket.getpeername()[0]} : {clientsocket.getpeername()[1]}")
            while True:
                data = clientsocket.recv(1024)
                data = int(data)
                if(data==1):
                    print(1)
                elif(data==2):
                    print(2)
                elif(data==3):
                    print(3)
                elif(data==4):
                    print("Conection finished")
                    break