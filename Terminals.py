from FileReading     import FileReader
from Container1      import Container1
from Packet1         import Packet1
from Packet2         import Packet2
from TerminalOptions import TerminalOptions
from EncodingOptions import EncodingOptions
from NoiseOptions    import NoiseOptions

import time
#Klasa odpowiadajaca za przesyłanie danych za pomoca roznych metod ARQ
class Terminal:
   
    def __init__(self, name, terminal_option, encoding_option, noise_option, frame_size, is_sender):
        self.name = name
        self.container= Container1()
        self.terminal_option = terminal_option
        self.encoding_option = encoding_option
        self.noise_option = noise_option
        self.frame_size = frame_size
        self.byte_list = []
        self.is_sender = is_sender
        self.package_buffer = None
    #Ustawienie docelowego terminala do komunikacji
    def bind(self, other_terminal):
        self.connected_terminal = other_terminal

    #Wysłanie wiadomość do docelowego terminala
    def send_message(self, file_name):
        self.create_packages( file_name)
        if self.terminal_option is TerminalOptions.stop_and_wait:
              self.receive_packages("000000000000000")
        elif self.terminal_option is TerminalOptions.go_back_N:
            print("go back N")
        elif self.terminal_option is TerminalOptions.selective_repeat:
            print("selective repeat")

    #Metoda do zaczytywania pakietow i tworzenia pliku
    def receive_packages(self, message):
        if self.is_sender is True:
            self.sender_receive( message)
        else:
            self.receiver_receive(message)

      
    
    # Metoda do stworzenia pakietow 
    def create_packages( self, file_name):
        Packet1.encoding_option = self.encoding_option
        Packet1.data_length = self.frame_size
        self.byte_list= FileReader.read_file(file_name, self.frame_size)
        for i in range(len(self.byte_list)):
              self.container.push(Packet1(i, self.byte_list[i] ))  
        print(self.container.length())

    def sender_receive(self, message ):       
        time.sleep(3)
        packet2 = Packet2()
        packet2.convert_to_packet(message)

        if packet2.should_retransmit() is False:
            if self.container.length() is 0:
                self.package_buffer = Packet1 (0, "10")
            else:    
                self.package_buffer = self.container.pop()
               
        print( self.package_buffer.key )  
                
        self.connected_terminal.receive_packages(self.package_buffer.convert_to_bin())

    def receiver_receive(self, message ):
          
          
            packet = Packet1()
            if packet.convert_to_packet(message) is False:
                packet2 = Packet2(self.container.length(), "11111111")
                
             
                self.connected_terminal.receive_packages(packet2.convert_to_bin())
            else:
              
                if packet.is_last() is False: 
                    packet2 = Packet2(self.container.length(), "00000000")
                    self.connected_terminal.receive_packages(packet2.convert_to_bin())
                    self.container.push(packet)
                else :
                    for i in range(self.container.length()):
                        self.byte_list.append(self.container.pop().get_value())    
                    FileReader.create_file(self.byte_list, "bee2.png")