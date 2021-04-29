from FileReading import FileReader
from Container1  import Container1
from Packet1 import Packet1
#Klasa odpowiadajaca za przesyłanie danych za pomoca roznych metod ARQ
class Terminal:
    connected_terminal = 0 #Referencja do terminala do którego mamy wysyłać inforamację
    name = "" #Nazwa terminala

    def __init__(self, name):
        self.name = name
        self.container= Container1()
        self.reads = None
    #Ustawienie docelowego terminala do komunikacji
    def bind(self, other_terminal):
        self.connected_terminal = other_terminal

    #Wysłanie wiadomość do docelowego terminala
    def send_message(self, message, is_end):
        self.container.push(message)
     #   self.connected_terminal.recieve_message(message)
        self.connected_terminal.receive_packages(message, is_end)
        
    #Otrzymanie wiadomości przez ten terminal
    def recieve_message(self, message):
        self.container.push(message)
        reader = FileReader()
        reader.open_file("bee2.png", "wb")
        print(message.get_value())
        reader.write_whole(message.get_value())

    #Metoda to zaczytywania pakietow i wrzucania ich do contenera
    def receive_packages(self, message, is_end):
        self.container.push(message)
        if is_end is True:
            self.reads= FileReader()
            self.reads.open_file("bee2.png", "wb")
            for i in self.container.length():
                self.reads.write_to_file(self.container.get_beginning())
            self.reads.close_file()
        
            

        
