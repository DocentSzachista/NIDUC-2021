from FileReading import FileReader
from Container1  import Container1
from Packet1     import Packet1
from TerminalOptions import TerminalOptions
from EncodingOptions import EncodingOptions
from NoiseOptions   import NoiseOptions
#Klasa odpowiadajaca za przesyłanie danych za pomoca roznych metod ARQ
class Terminal:
   
    def __init__(self, name, terminal_option, encoding_option, noise_option, frame_size):
        self.name = name
        self.container= Container1()
        self.terminal_option = terminal_option
        self.encoding_option = encoding_option
        self.noise_option = noise_option
        self.frame_size = frame_size

    #Ustawienie docelowego terminala do komunikacji
    def bind(self, other_terminal):
        self.connected_terminal = other_terminal

    #Wysłanie wiadomość do docelowego terminala
    def send_message(self, file_name, arq_mode, control_mode):
        self.create_packages( file_name )
        if self.terminal_option is TerminalOptions.stop_and_wait:
                for i in range(self.container.length()):
                    self.connected_terminal.receive_packages(self.container.pop(), False)
                self.connected_terminal.receive_packages(None, True)
        elif self.terminal_option is TerminalOptions.go_back_N:
            print("go back N")
        elif self.terminal_option is TerminalOptions.selective_repeat:
            print("selective repeat")

    #Metoda do zaczytywania pakietow i tworzenia pliku
    def receive_packages(self, message, is_end):
        if is_end is False:
            self.container.push(message)
        else:
            for i in range(self.container.length()):
                self.byte_list.append(self.container.pop().get_value())    
            FileReader.create_file(self.byte_list, "bee2.png")
    
    # Metoda do stworzenia pakietow 
    def create_packages( self, file_name, encoding_option ):
      
        self.byte_list= FileReader.read_file(file_name,1024)
        for i in range(len(self.byte_list)):
              self.container.push(Packet1(i, self.byte_list[i], encoding_option ))  
    

            

        
