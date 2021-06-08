from Statistics import Statistics
from FileReading import FileReader
from CommunicationSettings import CommunicationSettings, CheckSum
from DataPacket import DataPacket
from ResponsePacket import ResponsePacket

from threading import Thread

#Stop and Wait reciever
class RecieverSAW:
    def __init__(self, name: str, stats: Statistics) -> None:
        self.name = name
        self.thread = None  # Thread that this terminal will run on
        self.recieved_packets = []  # List of the packets that this terminal recieved
        self.good_packets = [] # List of the valid recieved packets
        self.simulate = False
        self.sender = None
        self.image_name = "res.png"
        self.stats = stats
        self.last_response = "1" #By default the last response is set to retransmit the packet

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
            self.stats.undetected_errors -= 1 #Starting packet is marked as retransmition
        self.stats.ammount_of_packets -= 1 #Remove the starting packet it's not exchanged
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

        response = ResponsePacket()  # Create the response
        
        if isinstance(packet, DataPacket):
            #Scrable packet
            message = packet.to_binary()
            data_packet = DataPacket()
            data_packet.to_packet(CommunicationSettings.scramble_message(message))

            if data_packet.get_valid():
                if CommunicationSettings.logging:
                    print(f"{self.name}: Valid packet")

                if data_packet.is_eot():
                    self.simulate = False
                    self.recreate_image()
                else:
                    self.good_packets.append(data_packet.get_data()) #Add good data
                response.mark_as_not_retransmit() #Say that there is no need for retransmition

                #If the content isn't the same then the error wasn't detected
                if message != data_packet.to_binary():
                    self.stats.undetected_errors += 1
            else:
                self.stats.detected_errors += 1
                response.mark_as_retransmit()
                if CommunicationSettings.logging:
                    print(f"{self.name}: Invalid packet")

            #Save the last response
            self.last_response = response.get_data()
            self.sender.recieve_packet(response)
        else: 
            #Is a response packet. That means that we should transmit our last response again
            response = ResponsePacket(data=self.last_response)
            self.sender.recieve_packet(response)
