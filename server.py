import socket
from _thread import *
import sys
import random

server = socket.gethostname()
port = 5555
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)
    
s.listen(2)

powerups = [("Health",0),("Shield",0)]
pos = [(250, 437), (250, 62)]
shoot = [0,0]
# rooms = []
# waiter = None

print("Server is listening")

def threaded_client(conn, player):
    conn.sendall(str.encode(str(player)))    
    reply = ""
    while True:
        try:
            data = conn.recv(2048).decode("utf-8")
            if data:
                tokens = data.split(".")
                if tokens[0] == "move":
                    pos[player] = eval(tokens[1])
                    reply = str(pos[abs(player - 1)])
                    conn.sendall(str.encode(reply)) 
                elif tokens[0] == "shoot":
                    if shoot[player] == 0:
                        shoot[player] = int(tokens[1])
                    reply = str(shoot[abs(player - 1)])
                    shoot[abs(player - 1)] = 0
                    
                    conn.sendall(str.encode(reply)) 
                elif tokens[0] == "powerup":
                    if player == 0:
                        randX = random.randint(int(tokens[1]), int(tokens[2]))
                        power1 = random.choice(["Ammo", "Energy", "Health", "Shields"])
                        power2 = random.choice(["Ammo", "Energy", "Health", "Shields"])
                         
                        powerups[0] = (power1, randX)
                        powerups[1] = (power2, randX)
#  
                    reply = f"{powerups[0]}.{powerups[1]}"
                    conn.sendall(str.encode(reply))
#                 print("Received: ", data)
#                 print("Sended: " , reply)
                    
                   
#                 shoot[abs(player - 1)] = 0
        except:
            break
        
    print("lost connection")
    conn.close() 
    global currentPlayer
    currentPlayer -= 1

currentPlayer = 0
while True:
    conn, addr = s.accept()
    print(f"New connection {addr}")
    
    start_new_thread(threaded_client, (conn, currentPlayer))
    currentPlayer += 1
#     if (waiter):
#         rooms.append((waiter, clientsocket))
#     else:
#         waiter = clientsocket
#         
#     if len(rooms) >= 1:    
#         rooms[0][0].send(bytes("Welcome to server! Hi mother fucker", "utf-8" ))
        
#     waiter.send(bytes("loop message", "utf-8" ))