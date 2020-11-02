from tkinter import *
from tkinter import filedialog
import socket 
import threading
import time
import pickle

def download():
    s.send(b'1')

def upload():
    s.send(b'2')

def delete():
    s.send(b'3')

def update():
    s.send(b"4")

if __name__ == "__main__":
    root = Tk()
    root.title('Cliente')
    root.geometry("530x800")


    # Button to download files from the server
    downloandButton = Button(root, text = "Download",padx= 30, pady= 10, command=download)
    downloandButton.grid(column=0, row=0, padx = 10, pady =5)

    # Button to upload files to the server
    uploadButton = Button(root, text = "Upload",padx= 30, pady= 10, command=upload)
    uploadButton.grid(column=1, row=0, padx = 10, pady = 5)

    # Button to delete files from the server
    deleteButton = Button(root, text = "Delete",padx= 30, pady= 10, command=delete)
    deleteButton.grid(column=2, row=0, padx=10, pady=5)

    # Button to update info from the server
    updateButton = Button(root, text = "Update",padx= 30, pady= 10, command=update)
    updateButton.grid(column=3, row=0, padx=10, pady=5)

    # List of the files and dyrectories on the server
    listServerFiles = Listbox(root, width=63, height=45)
    listServerFiles.grid(column=0, row=1, columnspan=4, pady= 10)


    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((socket.gethostname(), 5000))


    root.mainloop()