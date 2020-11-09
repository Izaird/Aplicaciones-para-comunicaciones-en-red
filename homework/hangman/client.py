import time
from string import ascii_uppercase
import socket
from tkinter import *
PORT = 5000
HOST = "127.0.0.1"
word_len = 0
guessed_letters=[]
tries = 0


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
        newGame(word_len)
        # top.destroy()

    def mediumDifficulty():
        s.send(b'1')
        time.sleep(0.05)
        print("medium difficulty choosed ...")
        s.send(b'medi')
        time.sleep(0.05)
        word_len = int(s.recv(1024).decode())
        print(word_len)
        newGame(word_len)
        # top.destroy()

    def hardDifficulty():
        s.send(b'1')
        time.sleep(0.05)
        print("hard difficulty choosed ...")
        s.send(b'hard')
        time.sleep(0.05)
        word_len = int(s.recv(1024).decode())
        print(word_len)
        newGame(word_len)
        # top.destroy()

    easy_b = Button(top, text="Easy", padx=30, pady=10, command=easyDifficulty)
    easy_b.grid(column=0, row=0, padx=10, pady=5)

    medium_b = Button(top, text="Medium", padx=30, pady=10, command=mediumDifficulty)
    medium_b.grid(column=0, row=1, padx=10, pady=5)

    hard_b = Button(top, text="Hard", padx=30, pady=10, command=hardDifficulty)
    hard_b.grid(column=0, row=2, padx=10, pady=5)


def guess(letter):
    global tries
    if(difficulty and tries<11):
        if(letter not in guessed_letters):
            s.send(b'2')
            time.sleep(0.05)
            guessed_letters.append(letter)
            print(f"Sending guest {letter}")
            s.send(letter.encode())
            time.sleep(0.05)
            word_completition = s.recv(1024).decode()
            if word_completition == 'no':
                tries +=1
                
                img_label.config(image=photos[tries])
                print(tries)
            else: 
                word_lbl.set(word_completition)
            
        else:
            print(f'Letter {letter} already guessed')
    else:
        print("You need to choose a difficulty")
        

def newGame(word_len):
    global tries
    global guessed_letters
    global difficulty
    tries =0
    guessed_letters = []
    difficulty = True
    word_lbl.set(" ".join("_" * word_len))
    img_label.config(image=photos[0])

if __name__ == "__main__":

    difficulty = False
    root = Tk()
    root.title('Hang man')
    root.geometry('1380x720')

    photos = [
        PhotoImage(file="images/hang0.png"),
        PhotoImage(file="images/hang1.png"),
        PhotoImage(file="images/hang2.png"),
        PhotoImage(file="images/hang3.png"),
        PhotoImage(file="images/hang4.png"),
        PhotoImage(file="images/hang5.png"),
        PhotoImage(file="images/hang6.png"),
        PhotoImage(file="images/hang7.png"),
        PhotoImage(file="images/hang8.png"),
        PhotoImage(file="images/hang9.png"),
        PhotoImage(file="images/hang10.png"),
        PhotoImage(file="images/hang11.png")
        ]



    i = 0
    for c in ascii_uppercase:
        Button(root, text=c, command=lambda c = c:guess(c), font=("Helvetica 18"),\
        width=4,).grid(row=1+i//3, column=i%3)
        i+=1

    word_lbl = StringVar()
    Label(root, textvariable=word_lbl, font=("Consolas 24 bold")).grid(row=0,\
    column=3, columnspan=7, padx=10)


    img_label= Label(root)
    img_label.grid(row=0, column=0, columnspan=3, padx=10, pady=40)
    img_label.config(image=photos[0])

    difficultyWindow()    
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
    s.connect((HOST,PORT))
    print('Connected to the server ...')
    

    root.mainloop()

