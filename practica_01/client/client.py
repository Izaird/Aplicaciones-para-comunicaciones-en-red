from tkinter import *
from tkinter import filedialog
import socket 
import threading
import time
import pickle
mypath = "Files/"
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"

#Function to download a files from the server
def download():
    reslist = list()
    seleccion = listServerFiles.curselection()

    for i in seleccion:
        entrada = listServerFiles.get(i)
        reslist.append(entrada)
    print(reslist)

    #If the user doesn't pick any item then we won't sent anything
    if not reslist:
        print("You need to select at least an item")
    else:
        s.send(b'1')
        time.sleep(.05)
        number_of_files = len(reslist)
        reslist = pickle.dumps(reslist)
        s.send(reslist)
        time.sleep(.05)
        for x in range(number_of_files):
            total_recv=0
            #Recive the file infos
            received = s.recv(BUFFER_SIZE).decode()
            filename, filesize = received.split(SEPARATOR)
            #remove abslute path if there is
            # filename = os.path.basename(filename)

            #convert to integer
            filesize = int(filesize)

            print(f"Downloading {filename} with a size of {filesize}B")

            # start receiving the file from the socket 
            # and writing to the file stream
            full_path = mypath + filename
            f = open(full_path, "wb")
            while True:
                #read 4096 Bytes from the socket(receive)
                bytes_read = s.recv(BUFFER_SIZE)
            #     if not bytes_read:
            # #         #nothing is received
            # #         #file transmiting is done 
            #         break
                #write to the file the byestes we just received
                f.write(bytes_read)
                total_recv += len(bytes_read)
                print("{:.2f}".format((total_recv/float(filesize))*100) + "% Done")

                if(total_recv >= filesize):
                    f.close()
                    print("File received")
                    break
            time.sleep(.05)

#Function to upload a file to the server
def upload():
    files = filedialog.askopenfilenames(initialdir="~/Documents",\
        title="Select the files you want to upload", \
        filetypes=(("All Files", "*.*"), ("Png", "*.png"))) 
    print (root.tk.splitlist(files))

#Function to delete a file from the server
def delete():
    reslist = list()
    seleccion = listServerFiles.curselection()

    for i in seleccion:
        entrada = listServerFiles.get(i)
        reslist.append(entrada)
    print(reslist)

    #If the user doesn't pick any item then we won't sent anything
    if not reslist:
        print("You need to select at least an item")
    else:
        s.send(b'3')
        time.sleep(.05)
        reslist = pickle.dumps(reslist)
        s.send(reslist)
        drive_content = s.recv(1024)
        drive_content = pickle.loads(drive_content)
        updateFileList(drive_content)

#Funciton to update the content list of the server    
def update():
    s.send(b"4")
    drive_content = s.recv(1024)
    drive_content = pickle.loads(drive_content)
    print(drive_content)
    updateFileList(drive_content)

#Function to update the listbox it needs the list of the files
def updateFileList(drive_content):
    listServerFiles.delete(0,END)
    for x in drive_content:
        listServerFiles.insert(END,x)


if __name__ == "__main__":
    root = Tk()
    root.title('Client')
    root.geometry("630x800")


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
    listServerFiles = Listbox(root, width=75, height=45, selectmode='multiple')
    listServerFiles.grid(column=0, row=1, columnspan=4, pady= 10, padx=10)


    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.connect((socket.gethostname(), 5000))

    drive_content = s.recv(1024)
    drive_content = pickle.loads(drive_content)
    print("Connected to the server...")
    updateFileList(drive_content)
    root.mainloop()