from Statistics import Statistics
from DataPacket import DataPacket
from ResponsePacket import ResponsePacket
from FileReading import FileReader
from CommunicationSettings import CommunicationSettings

from threading import Thread

#Go back N sender
class SenderGBN:
    def __init__(self, name: str, stats: Statistics) -> None:
        self.name = name
        self.thread = None  # Thread that this terminal will run on
        self.recieved_packets = []  # List of the packages that this terminal recieved
        self.packages_to_send = []  # List of the packages to send
        self.simulate = False
        self.reciever = None
        self.stats = stats

    #Bind the sender and the reciever
    def bind(self, reciever) -> None:
        self.reciever = reciever

    #Creates the packages to send
    def create_packages(self, file_name: str) -> None:
        byte_list = FileReader.read_file(file_name, CommunicationSettings.data_bytes)
        for index, data in enumerate(byte_list):  # Convert words to packages
            self.packages_to_send.append(DataPacket(index, data))

        #Create an end of transmition packet and add it to the end of the queue
        end_packet = DataPacket()
        end_packet.mark_as_eot()
        self.packages_to_send.append(end_packet)
        self.stats.min_packages = len(self.packages_to_send) + (len(self.packages_to_send) - 1) // 5
        if CommunicationSettings.logging:
            print(f"Created {len(self.packages_to_send)} packages")

    #Starts the transmition
    def send_image(self, image_name: str) -> None:
        self.create_packages(image_name)  # Create the packages from the file
        #To start the transmition make a response packet that asks for retransmition
        startPacket = ResponsePacket()
        startPacket.mark_as_retransmit()
        self.recieve_packet(startPacket)
        if CommunicationSettings.logging:
            print(f"{self.name}: Data transmition started")

    #Creates and starts the terminal thread
    def start(self) -> None:
        self.simulate = True
        self.thread = Thread(target=self.run)
        self.thread.start()

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
        packet: ResponsePacket = self.recieved_packets.pop(0)

        #Scramble the packet
        message = packet.to_binary()
        message = CommunicationSettings.scramble_message(message)
        response_packet = ResponsePacket()
        response_packet.to_packet(message)

        if response_packet.get_valid():
            # If no retransmition is needed then remove the current window of packets from the queue
            if response_packet.should_retransmit() == False:
                del self.packages_to_send[0:CommunicationSettings.window_size]

            if len(self.packages_to_send) == 0:
                self.simulate = False  # Every packet was send succesfuly
                return

            #If the content isn't the same then the error wasn't detected
            if message != response_packet.to_binary():
                self.stats.undetected_errors += 1

            #Send the required amount of packages
            for i in range(min(CommunicationSettings.window_size, len(self.packages_to_send))):
                self.reciever.recieve_packet(self.packages_to_send[i])
        else:
            #Ask for the retransmition of the response
            self.stats.detected_errors += 1
            response = ResponsePacket()
            response.mark_as_retransmit()
            self.reciever.recieve_packet(response)


