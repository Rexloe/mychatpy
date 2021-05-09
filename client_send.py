import time
import argparse
import threading
import os
import colorama

from main import Client, screenclr


class InputOutputClient:
    def __init__(self, client, buffer):
        self.client = client
        self.buffer = buffer

        thread_receive = threading.Thread(target=self.receive_message, args=())
        thread_send = threading.Thread(target=self.send_message, args=())
        
        thread_receive.start()
        thread_send.start()


    def client_commands(self, msg):
        client_comm_dict: dict = {"/clear": 1, "/help": 2}

        new_s = msg.split()[0]

        msgindict = client_comm_dict.get(new_s, 0)

        if msgindict:
            if msgindict == 2:
                self.buffer += str("\n\n=============Lista de comandos================\n\n"
                "/clear - limpa a tela\n" "/quit - sai do chat\n" "/list - lista todas as pessoas que estão no servidor e\n" 
                "em qual sala estão\n" "/togchance - togs the great\n" "/listchannels - lista todos os canais\n" 
                "NÃO FOI ADICIONADO /private {pessoa} - mande uma mensagem privada para alguém\n" "/setchannel {canal} - mude de canal\n"
                "/help - mostra essa tela\n" "NÃO FOI ADICIONADO /game {pessoa} - um jogo de duas pessoas\n" 
                "/color {cor} {mensagem} - mostra uma mensagem com a cor escrita (obs: os nomes das cores só podem ser escritos em ingles\n"
                "e caso voce queria uma cor mais brilhante adicione l para o nome da cor, deste jeito: lred)\n"
                "/colorname {cor} - muda a cor do seu nome, as cores funcionam do mesmo jeito do /color\n")
                #"/setname {nome} - muda de nome, com os mesmo critério de antes: não pode ter espaços\n\n")
                screenclr()
                print(self.buffer)
                print("Digite: ", end='')
            if msgindict == 1:
                self.buffer = ''
                screenclr()
                print("Digite: ", end='')
            return msgindict
        return msgindict

    def send_message(self):
        while True:
            msgsend = input()
            if len(msgsend) >= 1:
                end = self.client_commands(msgsend)
                if end:
                    msgsend = ''
                    continue
            self.client.send(msgsend)


    def receive_message(self):
        while True:
            msgreceive = self.client.receive()

            if "/quit" in msgreceive:
                self.client.s.close()
                print("\n\n[LOCAL]: you left\n\n")
                time.sleep()
                os._exit(1)
                
            if len(msgreceive) >= 1:
                self.buffer += msgreceive + "\n"
                screenclr()
                print(self.buffer, end='')
                print("Digite: ", end='')

                

def start():
    dormir = 0.1
    lines = (
        r"""
░░░░░░░░░░░░░░░▓▓███████▓▒░░░░░░░░░░░░░░░
░░░░░░░░░░░▓██████▓▓▓▓▓██████▓░░░░░░░░░░░
░░░░░░░░░████▒░░░░░░░░░░░░░▓████░░░░░░░░░
░░░░░░░███▓░░░░░░░░░░░░░░░░░░░▓██▒░░░░░░░
░░░░░░██▓░░░░░░░░░░░░░░░░░░░░░░░██▓░░░░░░
░░░░▒██░░░░░░░░░░░░░░░░░░░░░░░░░░░██░░░░░
░░░░██░░░▒▒▒░░░░░░░░░░░░░░░▒▓███▓░░█▓░░░░
░░░██░░▓▓▓▓▓▓▓▒░░░░░░░░░░▒▓███████▓░█▒░░░
░░██░▒███████▓▒▒░░░░░░░░▒██████████▓▓█░░░
░░█░▒██████████▓░░░░░░░▒██████▓▒▒▓██░██░░
░██░██░░░░░▓▓▓███▒░░░░░█████░░░░░░░██░█░░
░█░██░░░░░░░░▓▓██▓░░░░░░██▒░░░░░░░░░▓░██░
▒█░▓░░░░░░░░░░▓██░░░░░░█▓░░░░░░░░░░░░░▓█░
▓█░░░░░░░░░░░░░░██░░░░█▓░░░░░▒▒▒░░░░▒░░█░
█▓░░░░░░░▓███▓▓░░▒█░░░█░░░▒██▓▓▓█░░░░▓░█░
█▒▒░░░░░█▓░▒▒▒▓█▓░▒▒░░▓░░█▓▓▓██▓▓█░░░▓░█▒
█░▒▒░░░█▓▓████▓░█▒░▒░░▓░█▓███████▓▓░░█░█▓
█░░▓░░▒█████████▓█░▒░░▒░█▓███████▒███░░█▓
█░░█▒▓█▓█████▓▓▓█░░▒░░▒░░█▓▒▒▒░░░▒███░░▓█
█░░▒███▓▓▓▓▓▓▓▒░░░░▒░░▒░░░░▓▓▓▓▓▓▒░▒██░░█
█▒░▓▓░░░░░░░░░░░░░░▒░░▒▒░░░░░░░░░░░░░█▓░█
█▓░▒░░░░░░░░░░░░░░░▒░░░▒░░░░░░░░░░░░░░▓░█
█▓░░░░░░░░░░░░░░░░░▒░░░▒░░░░░░░░░░░░░░▒░█
▓█░░░░░░░░░░░░░░▒░░░░░░░░░█░░░░░░░░░░░░░█
▓█░░░░░░░░░░░░░█░░░░░░░░░░▒█░░░░░░░░░░░░█
▓█░░░░░░░░░░░░█▓░░░░░░░░░░░██░░░░░░░░░▓░█
▓█░░░░░░░░░░▓██▒░▓░░░░░░░█░▓▓██░░░░░░░█░█
▒█░▒░░░░░░▓██░░█░██▓░░░░███▓░░██▓░░░░█▓░█
░█░░█░░░▓██▓░░░▒▓▒███▓▓██░▒░░░░░██▓▓█▓░░█
░█░░░█████░░░░░░░░███████░░░░░░░░████░▓░█
░█▒░░░▓███▒░░░░░░████▒▓███▒░░░░░▓███░░▓░█
░█▓░░░▓▒███▒░▒▓█████▒░░█████████████░▒▓██
░██░░░░▓░██████████▒░░░░█████████▒█░░▓█▓█
░▓█░░░░░▓░██████████████████████▒▓█░░█░▒█
░▒█░░░░░▓▓░░░░░░░░░░░░░░░░░░░░░░▒█░░██░█▓
░░█░░░░░░██░░░░░░░░░░░░░░░░░░░░▓█▒░▒█░░█▓
░░█▓░▒░░░░█████████▓▓▓▓▓██████▓▓█░░█▒░░█░
░░▓█░▒▓░░░▒█░░▒▒▓▓▓██████▒░░░░░█░░█▓░░▒█░
░░░█░░▓█░░░▓▓░░░░░░░▓███▒░░░░░▓▓░▒█░░░██░
░░░██░░██░░░█▒░░░░░░░███░░░░░░█░░█░░░░█▒░
░░░░█▓░░██░░░█▒░░░░░▓███▒░░░░█▒░█▒░░░██░░
░░░░▒█▒░░██░░░█░░░░░████▓░░░▒▓░▓▓░░░▓█░░░
░░░░░▓█▓░░▓▓░░░█░░░░█████░░░░░░▓░░░▓█▒░░░
░░░░░░▓██░░▒░░░░▓░░░▓███▓░░░░░▓░░░▓█▓░░░░
░░░░░░░░██▒░░░░░░░░░▒███▓░░░░▒░░░██▓░░░░░
░░░░░░░░░███░░░░░░░░░███▒░░░░░░░██▒░░░░░░
░░░░░░░░░░▒██▓░░░░░░░███░░░░░░▓██░░░░░░░░
░░░░░░░░░░░░▓██▓░░░░░▓██░░░░░██▓░░░░░░░░░
░░░░░░░░░░░░░░███▒░░░░█▒░░▒███░░░░░░░░░░░
░░░░░░░░░░░░░░░░████▓▓█▓████░░░░░░░░░░░░░

        DISCORD 2 PARA HACKERS!!
        """
        "CARREGAMENTO RAPIDO",
        "Conectando com bancos de dados da deep web",
        "Baixando VIRUS",
        "Comprando BITCOINS com o SEU cartao",
        "Bebendo o pre-treino",
        "Conectando com o IP do servidor",
        "print(Hello World)",
        "Não olhe para trás",
        "Deletando o servidor de discord (1)",
        "Ativando seu microfone",
        "Vendendo seu ip para os chineses",
        "Jogando Darkrp",
        "Conectando com bancos de dados clandestinos",
        "Clonando o seu cartão",
        "Vendendo sua alma para o raiam santos",
        "Carregando modulos",
        "Mandando (1301239) bytes para a12szpy1092xd357.onion",

        "Pronto\n\n============\n\n",
    )

    for i in lines:
        print(i)
        time.sleep(dormir)



def main():
    ADDR = input("Digite o ip do servidor: "), input("Digite a porta do servidor: ")
    client = Client(ADDR)
    client.start()
    name = " "
    start()
    while " " in name:
        name = input("Digite um nome para entrar no canal(letras e numeros e _(under line) com o nome sem espaços): ")
    client.send(name)
    clientio = InputOutputClient(client, "")


if __name__ == "__main__":
    main()