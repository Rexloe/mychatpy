import socket
import threading
import time
import colorama
import random
import datetime
import queue
import os
import traceback

from dataclasses import dataclass
from abc import ABC, abstractmethod


def screenclr():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")


class Connection(ABC):
    FORMAT: str = "utf-8"
    HEADER: int = 1024

    def __init__(self, ADDR):
        self.ADDR: tuple = ADDR
        self.ip, self.port = ADDR 
        
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Socket connection
        colorama.init(autoreset=True)


    @abstractmethod
    def start(self) -> None: ...


class Client(Connection):
    def start(self):
        self.s.connect(self.ADDR)
    
    def send(self, msg):
        self.s.send(msg.encode(Connection.FORMAT))

    def receive(self):
        return self.s.recv(Connection.HEADER).decode(Connection.FORMAT)

class Server(Connection):
    client_list: list = list()
    channel_list: list = list()
    private_channel_list: list = list()
    server_output: str = str()

    def server_output_setter(self, *stro):
        Server.server_output = ''
        for i in stro:
            Server.server_output += i

    def start(self):
        self.still_listening = True

        self.s.bind(self.ADDR)
        self.s.listen(10)

        geral = Chat("geral", [])
        chat1 = Chat("chat1", [])
        chat2 = Chat("chat2", [])
        Server.channel_list.append(geral)
        Server.channel_list.append(chat1)
        Server.channel_list.append(chat2)

        self.server_output_setter(f"Server connected at {self.ADDR}\n\n")

    def listen(self):
        while self.still_listening:
            try:
                conn, addr = self.s.accept()
                name = conn.recv(Connection.HEADER).decode(Connection.FORMAT)

                conn.send(f"======================================\nBem vindo ao discord 2 {name}, digite /help para ver uma lista de commandos".encode(Connection.FORMAT))

                client_handle = ClientHandle(conn, addr, name)
                client_handle.channel.clients.append(client_handle)
                Server.client_list.append(client_handle)

                thread = threading.Thread(target=client_handle.receive, args=())
                thread.start()

                self.server_output_setter(f"[SERVER_LOCAL] connection from {addr}, name: {name}\n", 
                                          f"[SERVER_LOCAL] active connections {len(Server.client_list)}\n")
                self.send(f"[SERVER] {name} has joined the server, total of user: {len(Server.client_list)}")
            except Exception as e:
               self.server_output_setter(str(traceback.format_exc()) + '\n')
        s.close()

    def delete_client(self, name, addr):
        for j, i in enumerate(Server.client_list):
            if i.name == name and i.addr == addr:
                left_server = f"[SERVER] {name} left the server\n"
                self.server_output_setter(f"[SERVER] {name} | {addr} left the server\n")
                del Server.client_list[j]
                self.send(left_server)

    def send(self, msg):
        #try:
        for j, i in enumerate(Server.client_list):
            i.send_client(msg)
        #except Exception as e:
            #self.server_output_setter(str(traceback.format_exc()) + '\n')
            #self.delete_client(i.name, i.addr)

class ClientHandle(Server):
    def __init__(self, conn, addr, name):
        self.conn = conn
        self.addr = addr
        self.name = name
        self.color_name = ""
        self.channel = Server.channel_list[0]

    def receive(self):
        while True:
            try:
                msg = self.conn.recv(Connection.HEADER).decode(Connection.FORMAT)

                if "/quit" in msg:
                    self.send_client("/quit")
                    self.delete_client(self.name, self.addr)
                    break
                if len(msg) >= 1:
                    self.server_output_setter(f"[{self.addr[0]}, {self.name}, {self.channel.roomname}] {msg}\n")
                if len(msg) >= 1 and msg[0] == '/':
                    self.channel.user_commands(msg, self)
                    continue
                if len(msg) >= 1:
                    self.channel.send(self.channel.format_msg(msg, self.name, self.color_name))
                #self.send(packets(response, 50))
            except Exception:
                self.server_output_setter(str(traceback.format_exc()) + '\n')
        self.conn.close()

    def send_client(self, msg):
        self.conn.send(msg.encode(Connection.FORMAT))

    def close_conns(self):
        self.send("/quit")
    
class Chat(Server):
    def __init__(self, roomname, clients):
        self.roomname = roomname
        self.clients = clients

        self.USER_COMMANDS: dict = {
                                    "/quit": 1, 
                                    "/setname": 2,
                                    "/color": 3, 
                                    "/list": 4,
                                    "/togchance": 5, 
                                    "/listchannels": 6, 
                                    "/private": 7, # falta
                                    "/setchannel": 8, 
                                    "/help": 9, 
                                    "/game": 10, # falta
                                    "/clear": 11, 
                                    "/colorname": 12,
                                    "/whereami": 13.
                                   }
                                   
    @staticmethod
    def color_text(colortype, msgcontent):
        color = {
                 "BLACK": 30,
                 "RED": 31,
                 "GREEN": 32,
                 "YELLOW": 33,
                 "BLUE": 34,
                 "MAGENTA": 35,
                 "CYAN": 36,
                 "WHITE": 37,
                 "LBLACK": 90,
                 "LRED": 91,
                 "LGREEN": 92,
                 "LYELLOW": 93,
                 "LBLUE": 94,
                 "LMAGENTA": 95,
                 "LCYAN": 96,
                 "LWHITE": 97,
                 "RESET": 37,
                }
        return f"\033[{color.get(colortype, 37)}m" + msgcontent + '\033[39m'

    @staticmethod
    def timestamp():
        day_week = datetime.datetime.now().weekday()
        weeks_day = {
                     0: "Monday",
                     1: "Tuesday",
                     2: "Wednesday",
                     3: "Thursday",
                     4: "Friday",
                     5: "Saturday",
                     6: "Sunday",   
                    }
        week_day = weeks_day[day_week]
        hour = str(datetime.datetime.now().time())
        hour = hour[:5]
        return f"[{week_day[:3]} {hour}]"

    def format_msg(self, msg, name, color):
        filtered_str = Chat.timestamp() + f"[{Chat.color_text(color, name)}]: " + msg
        return filtered_str

    def send(self, msg):
        try:
            for i in self.clients:
                i.send_client(msg)
        except Exception as e:
            self.server_output_setter(str(traceback.format_exc()) + '\n')
            self.delete_client(i.name, i.addr)

    def user_commands(self, msg, client):
        split_msg = msg.split()
        comm = split_msg[0]

        if len(split_msg) >= 2:
            msgcontent = split_msg[1:]
            msgcontent = " ".join(msgcontent)
        
        typecomm: int = self.USER_COMMANDS.get(comm, 100)
            
        if typecomm == 2:
            self.setname(client, msgcontent)
        if typecomm == 3:
            msg = self.color(msgcontent)
        if typecomm == 4:
            self.list_all(client)
        if typecomm == 5:
            self.tog_chance(msg, client)
        if typecomm == 6:
            self.list_channels(client)
        if typecomm == 7:
            ... # private
        if typecomm == 8:
            self.set_channel(client, msgcontent)
        if typecomm == 9:
            ... # help
        if typecomm == 10:
            ... # game
        if typecomm == 11:
            ... # clear
        if typecomm == 12:
            client.color_name = self.color_name(msgcontent)
        if typecomm == 13:
            self.whereami(client)
        self.send(self.format_msg(msg, client.name, client.color_name))

    def setname(self, client, name):
        client.name = name.replace(' ', '')

    def color(self, msg_content):
        msg_split: list = msg_content.split()
        if len(msg_split) >= 2:
            color: str = msg_split[0].upper()
            text: str = " ".join(msg_split[1:])
            return Chat.color_text(color, text)

    def list_all(self, client):
        list_data = "[SERVER]: \n"
        for i, j in enumerate(Server.client_list):
            list_data += f"{i + 1}. | Name: {j.name} | Addres: {j.addr[0]} | Channel: {j.channel.roomname}\n"
        client.send_client(list_data)

    def tog_chance(self, msg, client):
        #self.server_output_setter(self.format_msg(msg, client.name, client.color_name))
        togs_str = f"[TOGS]: Chance de {random.randint(0, 100)}% fellas"
        self.server_output_setter(togs_str)
        self.send(togs_str)

    def list_channels(self, client):
        list_server = "[SERVER]: \n"
        for i, j in enumerate(Server.channel_list):
            list_server += f"{i + 1} | Channel: {j.roomname} | People: {[i.name for i in j.clients]}\n"
        client.send_client(list_server)

    def whereami(self, client):
        client.send_client("[SERVER]: " + client.channel.roomname)

    def color_name(self, name):
        return name.upper()

    def set_channel(self, client, msg_content):
        for i in Server.channel_list:
            if client.channel.roomname == msg_content:
                client.send_client(f"[SERVER]: you are already at {msg_content}")
                break
            if i.roomname == msg_content and client.channel.roomname != i.roomname:
                client.channel.send(f"[SERVER]: {client.name} left the channel and joined {i.roomname}\n")
                i.send(f"[SERVER]: {client.name} left {client.channel.roomname} and joined\n")
                client.channel.clients.remove(client)
                client.channel = i
                client.channel.clients.append(client)
                self.server_output_setter(f"[SERVER_LOCAL]: {client.name} left {client.channel.roomname} and joined {i.roomname}\n")
                return 1
        client.send_client(f"[SERVER]: the channel {msg_content} doesn't exist\n")

    

class PrivateChat(Chat): #depois
    ...

class Game(PrivateChat): #depois
    ...


# ini file for settings
# A FAZER: chat do admin
# A FAZER: ver aula de threading
# A FAZER: ver aula de sockets dnv
# A FAZER: ler docs do sockets
# https://github.com/AgonisingPeach/FyreFlyMessaging/blob/996746d4f6016ff5f057a5e2bad009a74c109427/FyreFlyServer.py#L157
# https://www.techwithtim.net/tutorials/socket-programming/
# https://www.youtube.com/watch?v=3QiPPX-KeSc
# https://www.youtube.com/watch?v=IEEhzQoKtQU
# https://www.youtube.com/watch?v=KQasIwElg3w
# /whisper
# https://www.youtube.com/watch?v=BHNBAwU1Sr4
# /setchannel
# /games
# VER AULA DE REDES
# VER aula de programção orientada a objetos
# https://www.youtube.com/watch?v=fKl2JW_qrso
# https://stackoverflow.com/questions/1278705/when-i-catch-an-exception-how-do-i-get-the-type-file-and-line-number
# Criptografia entre bate papos privados
# historia de chat