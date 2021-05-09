import threading
import time
import sys
import os

from main import Server, screenclr

class InputOutputServer:
    def __init__(self, addr, buffer):
        self.buffer = buffer
        self.server = Server(addr)
        self.server.start()

        self.threadlisten = threading.Thread(target=self.server.listen, args=())
        self.threadlisten.start()

        self.threadoutput = threading.Thread(target=self.printserveroutput, args=())
        self.threadoutput.start()

        self.threadinput = threading.Thread(target=self.adminput, args=())
        self.threadinput.start()
        ...



    def printserveroutput(self):
         while True:
            if self.server.server_output not in self.buffer:
                self.buffer += self.server.server_output
                screenclr()
                print(self.buffer)
                print("Say (server side): ", end="")


    def adminput(self) -> None:
        while True:
            strsay = "Say (server side): "
            print(strsay, end="")
            adm_input = input()

            strsay += adm_input

            self.buffer += strsay + '\n'

            if len(adm_input) >= 2 and adm_input[0] == '/':
                    split_msg = adm_input.split()
                    command = split_msg[0]
                    content = ''
                    if len(split_msg) >= 2:
                        content = " ".join(split_msg[1:])

                    self.admincomms(command, content)




    def admincomms(self, command, content):
        SERVER_COMMANDS: dict = {
                                 "/admpoweroff": 1, 
                                 "/admkick": 2, 
                                 "/admclear": 3,
                                 "/admlist": 4,
                                 "/admsend": 5,
                                 "/admlistchannels": 6,
                                 "/admhelp": 7,
                                }

        comm = SERVER_COMMANDS.get(command, 10)
        
        if comm == 1:
            self.buffer += self.admpoweroff()
            self.buffer += "[SERVER_LOCAL] server will turn off in 3 seconds\n"
            screenclr()
            print(self.buffer, end='')
            time.sleep(3)
            os._exit(1)
        if comm == 2:
            kickstr, hasbeen = self.admkick(content)
            self.buffer += kickstr
            if hasbeen:
                self.server.send(f"[SERVER]: {content} has been kicked")
        if comm == 3:
            self.buffer = ''
            self.server.server_output = ''
            self.buffer += self.admclear()
        if comm == 4:
            self.buffer += self.admlist()
        if comm == 5:
            self.buffer += self.admsend(content)
        if comm == 6:
            self.buffer += self.adm_channels()
        if comm == 7:
            self.buffer += self.admhelp(SERVER_COMMANDS)
        if comm == 10:
            self.buffer += "[SERVER_LOCAL]: command does not exist\n"
        

        screenclr()
        print(self.buffer, end="")

    def admclear(self):
        screenclr()
        return "[SERVER_LOCAL]: chat reset\n\n"

    def admkick(self, name):
        for i, j in enumerate(self.server.client_list):
            if name == j.name:
                j.send("/quit")
                return f"[SERVER_LOCAL]: {name} has been kicked\n", 1
        return f"[SERVER_LOCAL]: the client {name} does not exist\n", 0


    def admlist(self):
        listitems = "" 

        for i, j in enumerate(self.server.client_list):
            listitems += f"{i + 1}. {j.addr[0]} | {j.name}\n"
        if not len(listitems):
            return "[SERVER_LOCAL]: there are no clients online\n"
        return "[SERVER_LOCAL]: \n" + listitems

    
    def admpoweroff(self):
        self.server.send("/quit")
        self.server.still_listening = False
        self.server.s.close()
        return "[SERVER_LOCAL]: all clients have been disconnected. server has been been disconnected\n"

    def admsend(self, msg):
        strserver = f"[SERVER]: {msg}"
        self.server.send(strserver)
        return strserver + '\n'

    def adm_channels(self):
        listchannels = ''
        
        for i, j in enumerate(self.server.channel_list):
            listchannels += f"{i + 1} | name: {j.roomname} | people: {j.clients}\n"
        if not len(listchannels):
            return "[SERVER_LOCAL]: no channels\n"
        return "[SERVER_LOCAL]: \n" + listchannels

    def admhelp(self, commlist):
        listhelp = ''
        for i, j in enumerate(list(commlist.keys())):
            listhelp += f"{i + 1} | {j}\n"
        if not len(listhelp):
            return "[SERVER_LOCAL]: no commands\n"
        return "[SERVER_LOCAL]: \n" + listhelp
            

def main() -> None:
    admcomhis: list = list()
    buffer: str = str()

    ADDR = "192.168.1.104", 5050

    serverio = InputOutputServer(ADDR, buffer)

if __name__ == "__main__":
    main()