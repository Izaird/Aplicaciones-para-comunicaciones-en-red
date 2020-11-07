import socket
import random
import time
HOST = "127.0.0.1"
PORT = 5000

if __name__ == "__main__":
    hard_words = ["hipopotomostrosesquipedaliofobia"\
                    ,"parangaricutirimicuaro"\
                    ,"superescalifragilisticoespialidos"\
                    ,"hexakosioihexekontahexafobia"\
                    ,"desanparangaricutirimicuarizador"\
                    ,"paralelepipedos"\
                    ,"zsoltbaumgartnerismo"\
                    ,"esternocleidomastoideo"\
                    ,"homopedonecrozoofilico"\
                    ,"neotromponolomeonilopolonouta"\
                    ,"dihidroxifenilalaninasa"\
                    ,"ugarterragaicoecheapaturri"\
                    ,"metilendioximetanfetamina"\
                    ,"caravincuntincuadrado"\
                    ,"octangolonoplasentaiconósico"\
                    ,"linfogranulomatosis inginalis"\
                    ,"narainkarthikeyanismo"\
                    ,"dimetilnitrosamina"]

    medium_words = ["bosniaca"\
                    ,"bosniaco"\
                    ,"bosniaca"\
                    ,"bosniaco"\
                    ,"botanica"\
                    ,"bramador"\
                    ,"bretonas"\
                    ,"bretones"\
                    ,"bridones"\
                    ,"brumador"\
                    ,"brujulas"\
                    ,"bulgaras"\
                    ,"bulgaros"\
                    ,"cinetico"\
                    ,"cisteína"\
                    ,"coaligas"\
                    ,"cobrizas"]

    easy_words = ["mala"\
                ,"mece"\
                ,"medi"\
                ,"trae"\
                ,"tuve"\
                ,"orzo"\
                ,"osas"\
                ,"osea"\
                ,"osos"\
                ,"dañe"\
                ,"dome"]

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

                #If there is not response from the client then we shutdown
                #the communication with that client
                if not data:
                    print(f"Connection finished with: {client_s.getpeername()[0]} : {client_s.getpeername()[1]}")
                    break

                #We also need to cast the data to int
                data = int(data)
                choosen_word = ''
                #Request to choose a difficulty      
                if(data==1):
                    print("Request to choose a difficulty has been received")
                    difficulty = client_s.recv(1024).decode()
                   
                    if(difficulty=='easy'):
                        print(" easy diffilculty chosen")
                        choosen_word = random.choice(easy_words)
                        len_choosen_word = str(len(choosen_word)).encode()
                        client_s.send(len_choosen_word)
                        time.sleep(0.05)

                    elif(difficulty=='medi'):
                        print(" medium diffilculty chosen")
                        choosen_word = random.choice(medium_words)
                        len_choosen_word = str(len(choosen_word)).encode()
                        client_s.send(len_choosen_word)
                        time.sleep(0.05)

                    elif(difficulty=='hard'):
                        print(" hard diffilculty chosen")
                        choosen_word = random.choice(hard_words)
                        len_choosen_word = str(len(choosen_word)).encode()
                        client_s.send(len_choosen_word)
                        time.sleep(0.05)