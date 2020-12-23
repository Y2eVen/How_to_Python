import socket

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = socket.gethostname()
        self.port = 5555
        self.addr = (self.server, self.port)
        self.connect()
      
    def getPlayer(self):
        return self.player
    
    def connect(self):
        try:
            self.client.connect(self.addr)
            self.player = int(self.client.recv(2048).decode())
        except:
            pass
        
    def send(self, data):
        try:
            self.client.send(str.encode(data))
            res = self.client.recv(2048).decode()
            return res
        except socket.error as e:
            print(e)
        
# n = Network()
# tup = (20,20)
# print(n.send(f"move.{tup}"))
