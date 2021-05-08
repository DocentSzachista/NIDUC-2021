from FileReading import FileReader
from Container1  import Container1
from Packet1     import Packet1
#Klasa odpowiadajaca za przesyłanie danych za pomoca roznych metod ARQ
class Terminal:
    connected_terminal = 0 #Referencja do terminala do którego mamy wysyłać inforamację
    name = "" #Nazwa terminala
    byte_list =[]
    def __init__(self, name):
        self.name = name
        self.container= Container1()
        
    #Ustawienie docelowego terminala do komunikacji
    def bind(self, other_terminal):
        self.connected_terminal = other_terminal

    #Wysłanie wiadomość do docelowego terminala
    def send_message(self, file_name, arq_mode, control_mode):
        self.create_packages( file_name )
        for i in range(self.container.length()):
            self.connected_terminal.receive_packages(self.container.pop(), False)
        self.connected_terminal.receive_packages(None, True)

    #Metoda do zaczytywania pakietow i tworzenia pliku
    def receive_packages(self, message, is_end):
        if is_end is False:
            self.container.push(message)
        else:
            for i in range(self.container.length()):
                self.byte_list.append(self.container.pop().get_value())    
            FileReader.create_file(self.byte_list, "bee2.png")
    
    # Metoda do stworzenia pakietow 
    def create_packages( self, file_name ): 
        self.byte_list= FileReader.read_file(file_name,1024)
        for i in range(len(self.byte_list)):
              self.container.push(Packet1(i, self.byte_list[i] ))  
            

        
