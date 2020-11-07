
import socket
from tkinter import *
HOST = "127.0.0.1"
PORT = 5000

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST,PORT))
    s.listen()
    print("Waiting for clients ...")
    while True: 
        client_s, client_addr = s.accept()

        with client_s:

        
            #Ip and port of the client
            print(f"Conected by {client_s.getpeername()[0]} : {client_s.getpeername()[1]}")

            #Once we stablish connection with the client we stay at an infinite
            #loop waiting for intrutions 
            
            while True:

                data = client_s.recv(1024)
                if not data:
                    print(f"Connection finished with: {client_s.getpeername()[0]} : {client_s.getpeername()[1]}")
                    break

                #We also need to cast the data to int
                data = int(data)
                if(data==1):
                    print(1)
            
            

        