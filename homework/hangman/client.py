import time
import socket
from tkinter import *
PORT = 5000
HOST = "127.0.0.1"

def difficultyWindow():
    top = Toplevel()
    top.title('Chose a difficulty')

    def easyDifficulty():
        s.send(b'1')
        time.sleep(0.05)
        print("easy difficulty choosed ...")
        s.send(b'easy')
        time.sleep(0.05)
        word_len = int(s.recv(1024).decode())
        print(word_len)
        # top.destroy()

    def mediumDifficulty():
        s.send(b'1')
        time.sleep(0.05)
        print("medium difficulty choosed ...")
        s.send(b'medi')
        time.sleep(0.05)
        word_len = int(s.recv(1024).decode())
        print(word_len)
        # top.destroy()

    def hardDifficulty():
        s.send(b'1')
        time.sleep(0.05)
        print("hard difficulty choosed ...")
        s.send(b'hard')
        time.sleep(0.05)
        word_len = int(s.recv(1024).decode())
        print(word_len)
        # top.destroy()

    easy_b = Button(top, text="Easy", padx=30, pady=10, command=easyDifficulty)
    easy_b.grid(column=0, row=0, padx=10, pady=5)

    medium_b = Button(top, text="Medium", padx=30, pady=10, command=mediumDifficulty)
    medium_b.grid(column=0, row=1, padx=10, pady=5)

    hard_b = Button(top, text="Hard", padx=30, pady=10, command=hardDifficulty)
    hard_b.grid(column=0, row=2, padx=10, pady=5)


if __name__ == "__main__":

    root = Tk()
    root.title('Hang man')
    root.geometry('600x800')


    difficultyWindow()    



    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    s.connect((HOST,PORT))
    print('Connected to the server ...')
    

    root.mainloop()

