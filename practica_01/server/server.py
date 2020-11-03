from tkinter import *
import pickle
from PIL import ImageTk, Image
import socket
from os import listdir, walk, remove
from pathlib import Path
mypath="Files/"
PORT=5000
SEPARATOR = "<SEPARATOR>"

BUFFER_SIZE = 4096

# Function to get all the content of the server folder File
# *It return the information in form of bytes
def updateFileList():
    drive_content=[]
    for(dirpath, dirnames, filenames) in walk(mypath):
        drive_content.extend(dirnames)
        drive_content.extend(filenames)
        break
    drive_content = pickle.dumps(drive_content)
    return drive_content


if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((socket.gethostname(),PORT))
    s.listen()
    print("Waiting for clients ...")
    while True:
        clientsocket, address = s.accept()
        with clientsocket:

            #Every time that connect with a new client update the list of files
            drive_content= updateFileList()
            #And also send this information to the client
            clientsocket.send(drive_content)

            #Ip and port of the client
            print(f"Connection from {clientsocket.getpeername()[0]} : {clientsocket.getpeername()[1]}")

            #Once we stablish connection with the client we stay at a infinite loop
            #waiting for instructions
            while True:
                data = clientsocket.recv(1024)

                #If there is not response from the cliente then we break out of the loop
                if not data:
                    print("ay LMAO")
                    break

                #Download files
                data = int(data)
                if(data==1):
                    print("The request to download these files has been recived:")
                    send_this_items = clientsocket.recv(1024)
                    send_this_items = pickle.loads(send_this_items)
                    for item in send_this_items:
                        print(f'    -{item}')
                        full_path = mypath + item
                        # f = open(full_path, 'rb')


               #Upload file 
                elif(data==2):
                    print("The request to upload the files has been received")
                    clientsocket.send(b"Send the file/files")
                
                #Delete files
                elif(data==3):
                    print("The request to delete the following files has been received:")
                    delete_this_items = clientsocket.recv(1024)
                    delete_this_items = pickle.loads(delete_this_items)
                    for item in delete_this_items:
                        print(f'    -{item}')
                        full_path = mypath + item

                        #We call the function remove to delete the files from the server
                        remove(full_path)

                    #After deleting the files the server sents an content update
                    print("Sending updated content list...")
                    drive_content = updateFileList()
                    clientsocket.send(drive_content)

                #We send an update about the file list to the client
                elif(data==4):
                    print("The request to update the file list has been received")
                    drive_content = updateFileList()
                    clientsocket.send(drive_content)

                elif(data==5):
                    print("Conection finished")
                    break