import socket

class Terminal:
    connected_terminal = 0
    name = ""

    def __init__(self, name):
        self.name = name

    def bind(self, other_terminal):
        self.connected_terminal = other_terminal

    def send_message(self, message):
        self.connected_terminal.recieve_message(message)

    def recieve_message(self, message):
        print(self.name + ": " + message)