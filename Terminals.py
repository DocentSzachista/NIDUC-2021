from FileReading import FileReader

#Klasa odpowiadajaca za przesyłanie danych za pomoca roznych metod ARQ
class Terminal:
    connected_terminal = 0 #Referencja do terminala do którego mamy wysyłać inforamację
    name = "" #Nazwa terminala

    def __init__(self, name):
        self.name = name

    #Ustawienie docelowego terminala do komunikacji
    def bind(self, other_terminal):
        self.connected_terminal = other_terminal

    #Wysłanie wiadomość do docelowego terminala
    def send_message(self, message):
        self.connected_terminal.recieve_message(message)

    #Otrzymanie wiadomości przez ten terminal
    def recieve_message(self, message):
        reader = FileReader()
        reader.open_file("bee2.png", "wb")
        reader.write_whole(message)
