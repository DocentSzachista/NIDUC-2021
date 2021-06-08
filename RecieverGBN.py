from Statistics import Statistics
from FileReading import FileReader
from CommunicationSettings import CheckSum, CommunicationSettings
from DataPacket import DataPacket
from ResponsePacket import ResponsePacket

from threading import Thread

#Go back N reciever
class RecieverGBN:
    def __init__(self, name: str, stats: Statistics) -> None:
        self.name = name
        self.thread = None  # Thread that this terminal will run on
        self.recieved_packets = []  # List of the packets that this terminal recieved
        self.good_packets = []  # List of the valid recieved packets
        self.simulate = False
        self.sender = None
        self.image_name = "res.png"
        self.stats = stats
        self.last_response = "1"
        self.all_packets_valid = True
        self.current_window = [] #Packets recieved in this window

    #Name of the image after recreation
    def set_recreated_image_name(self, name: str) -> None:
        self.image_name = name

    #Bind the sender and the reciever
    def bind(self, sender) -> None:
        self.sender = sender

    #Creates and starts the terminal thread
    def start(self) -> None:
        self.simulate = True
        self.thread = Thread(target=self.run)
        self.thread.start()

    #Recreate the image
    def recreate_image(self) -> None:
        if CommunicationSettings.logging:
            print(f"{self.name}: recieved {len(self.good_packets)} packages")

        FileReader.create_file(self.good_packets, self.image_name)
        if CommunicationSettings.logging:
            print(f"{self.name}: Image {self.image_name} created")

        if CommunicationSettings.check_sum != CheckSum.Hamming_code:
            self.stats.undetected_errors -= 1  # Starting packet is marked as retransmition
        # Remove the starting packet it's not exchanged
        self.stats.ammount_of_packets -= 1
        print(self.stats.get_statistics())

    #Adds the packet to the recieved packet list
    def recieve_packet(self, packet) -> None:
        self.recieved_packets.append(packet)
        self.stats.ammount_of_packets += 1

    #Runs the thread loop
    def run(self) -> None:
        while self.simulate:
            if not self.recieved_packets:
               continue

            self.handle_packets()

    #Determines what to do with the packet
    def handle_packets(self) -> None:
        packet = self.recieved_packets.pop(0)

        if isinstance(packet, DataPacket):
            #Scrable packet
            message = packet.to_binary()
            data_packet = DataPacket()
            data_packet.to_packet(CommunicationSettings.scramble_message(message))
            
            is_eot = False
            if data_packet.get_valid():
                #If this is the end of transmition and all packets in the window are valid then recreate the image
                if data_packet.is_eot() and self.all_packets_valid:
                    is_eot = True

                #If the content isn't the same then the error wasn't detected
                if message != data_packet.to_binary():
                    self.stats.undetected_errors += 1
            else:
                self.stats.detected_errors += 1
                self.all_packets_valid = False #Not all packets in this window were valid

            if is_eot == False:
                self.current_window.append(data_packet.get_data()) #Add data to the current window if not end of transmition

            #Send a response when the amount of recieved packets is equal to the window size or eot
            if len(self.current_window) == CommunicationSettings.window_size or is_eot:
                response = ResponsePacket()
                #If all packets in the window were valid add the to the good data
                if self.all_packets_valid:
                    if CommunicationSettings.logging:
                        print(f"{self.name}: Valid window")

                    response.mark_as_not_retransmit()
                    self.good_packets.extend(self.current_window)
                else:
                    if CommunicationSettings.logging:
                        print(f"{self.name}: Invalid window")

                    response.mark_as_retransmit()
                
                #Clear the window after sending the response
                self.current_window.clear()
                #Reset window retransmition flag
                self.all_packets_valid = True

                if is_eot:
                    self.simulate = False
                    self.recreate_image()

                self.sender.recieve_packet(response)

        else:
            #Is a response packet. That means that we should transmit our last response again
            response = ResponsePacket(data=self.last_response)
            self.sender.recieve_packet(response)
