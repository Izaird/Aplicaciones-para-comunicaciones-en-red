from tkinter import *
import pickle
import socket
import os
from pathlib import Path
import tqdm
import time
mypath="Files/"
PORT=5000
SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096

# Function to get all the content of the server folder File
# *It return the information in form of bytes
def updateFileList():
    drive_content=[]
    for(dirpath, dirnames, filenames) in os.walk(mypath):
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
                    print("Conection finished")
                    break

                #Download files
                data = int(data)
                if(data==1):
                    print("The request to download these files has been recived:")
                    send_this_items = clientsocket.recv(1024)
                    send_this_items = pickle.loads(send_this_items)

                    for item in send_this_items:
                        total_recv = 0
                        full_path = mypath + item
                        #Get the file size
                        filesize = os.path.getsize(full_path)
                        #Send the filename and filesize
                        clientsocket.send(f"{item}{SEPARATOR}{filesize}".encode())
                        time.sleep(.05)
                        #start sending the file
                        f = open(full_path, 'rb')
                        while True:
                            #read the bytes from the file
                            bytes_read = f.read(BUFFER_SIZE)
                            # if not bytes_read:
                            #     #File transmitting is done
                            #     break
                            #We use sendall to assue trasnmission in
                            #busy networks
                            clientsocket.sendall(bytes_read)
                            
                            total_recv += len(bytes_read)
                            print("{:.2f}".format((total_recv/float(filesize))*100) + "% Done")

                            if(total_recv >= filesize):
                                f.close()
                                print("File sent")
                                break
                        time.sleep(.05)

               #Upload file 
                elif(data==2):
                    print("The request to upload the files has been received")
                    number_of_files = clientsocket.recv(1024).decode()
                    time.sleep(0.05)
                    for _ in range(int(number_of_files)):
                        total_recv = 0
                        #receive the file infos
                        received = clientsocket.recv(BUFFER_SIZE).decode()
                        filename, filesize = received.split(SEPARATOR)

                        #convert to integer
                        filesize = int(filesize)

                        print(f"Uploading {filename} with a size of {filesize}B")

                        #Start receiving the file from the socket
                        #and writing to the file stream

                        full_path = mypath + filename
                        f = open(full_path, 'wb')

                        while True:
                            #Read 4096 Bytes from the socket(receive)
                            bytes_read = clientsocket.recv(BUFFER_SIZE)

                            #write to the file the bytes that we just received
                            f.write(bytes_read)
                            total_recv += len(bytes_read)
                            print("{:.2f}".format((total_recv/float(filesize))*100) + "% Done")

                            if(total_recv >= filesize):
                                f.close()
                                print("File received")
                                break
                        time.sleep(0.05)


                    #After upload the files the server sents an content update
                    print("Sending updated content list...")
                    drive_content = updateFileList()
                    clientsocket.send(drive_content)
                    time.sleep(0.05)

                    
                #Delete files
                elif(data==3):
                    print("The request to delete the following files has been received:")
                    delete_this_items = clientsocket.recv(1024)
                    delete_this_items = pickle.loads(delete_this_items)
                    for item in delete_this_items:
                        print(f'    -{item}')
                        full_path = mypath + item

                        #We call the function remove to delete the files from the server
                        os.remove(full_path)

                    #After deleting the files the server sents an content update
                    print("Sending updated content list...")
                    drive_content = updateFileList()
                    clientsocket.send(drive_content)

                #We send an update about the file list to the client
                elif(data==4):
                    print("The request to update the file list has been received")
                    drive_content = updateFileList()
                    clientsocket.send(drive_content)