from tkinter import *
from PIL import ImageTk, Image
import socket 
import threading
from os import listdir, walk 
from pathlib import Path

def thread_interface():
    root = Tk()
    root.title('Servidor archivos')
    root.geometry("800x600")


    def updateFileList():
        file_names = []
        directory_names = [] 


        for (dirpath, dirnames, filenames) in walk(mypath):
            file_names.extend(filenames)
            break        

        for (dirpath, dirnames, filenames) in walk(mypath):
            directory_names.extend(dirnames)

        listFilesDir = Listbox(root)
        listFilesDir.grid(column = 0, row = 0)
        listFilesDir.delete(0, 'END')
        for x in directory_names:
            listFilesDir.insert(END,x)
        for x in file_names:
            listFilesDir.insert(END,x)

    updateFileList()
    updateButton = Button(root, text = "actualizar", command = updateFileList)
    updateButton.grid(column=0, row = 1)


    root.mainloop()


def thread_socket():
    PORT = 5001
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((socket.gethostname(),PORT))
    s.listen()
    while True:
        clientsocket, address = s.accept()
        print(f"Connection from {clientsocket.getpeername()} : {clientsocket.getpeername()}")
        clientsocket.send(bytes("Welcome to the server!", "utf-8"))
        clientsocket.close()



if __name__ == "__main__":
    mypath = "Files/"
    interface = threading.Thread(target=thread_interface)
    interface.start()
    socket_server = threading.Thread(target = thread_socket)
    socket_server.start()