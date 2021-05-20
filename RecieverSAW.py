from os import stat
from Statistics import Statistics
from FileReading import FileReader
from CommunicationSettings import CommunicationSettings
from DataPacket import DataPacket
from ResponsePacket import ResponsePacket

from threading import Thread

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
            packet.to_packet(CommunicationSettings.scramble_message(message))

            response = ResponsePacket() #Create the response
            if packet.get_valid():
                if CommunicationSettings.logging:
                    print(f"{self.name}: Valid packet")
                if packet.is_eot():
                    self.simulate = False
                    self.recreate_image()
                else:
                    self.good_packets.append(packet.get_data()) #Add good data
                response.mark_as_not_retransmit() #Say that there is no need for retransmition

                if message == packet.to_binary():
                    self.stats.detected_errors += 1
                else:
                    self.stats.undetected_errors += 1
            else:
                response.mark_as_retransmit()
                if CommunicationSettings.logging:
                    print(f"{self.name}: Invalid packet")

            self.sender.recieve_packet(response)
        else:
            pass #TODO: Is response packet, act accordingly
