from Statistics import Statistics
from FileReading import FileReader
from CommunicationSettings import CheckSum, CommunicationSettings
from DataPacket import DataPacket
from ResponsePacket import ResponsePacket

from threading import Thread

#Selective repeat reciever
class RecieverSR:
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
        self.last_response_key = 0
        self.current_window = []  # Packets recieved in this window

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

            if data_packet.get_valid():
                if message != data_packet.to_binary():
                    self.stats.undetected_errors += 1
            else:
                self.stats.detected_errors += 1

            if len(self.current_window) < CommunicationSettings.window_size:
                self.current_window.append(data_packet) #Append packet if window isn't full
            else:
                position = data_packet.get_key()
                #Set the packet in the correct place if it makes sense (position is good and the packet is valid)
                if position < CommunicationSettings.window_size and data_packet.get_valid():
                    self.current_window[position] = data_packet

            is_eot = data_packet.is_eot()

            #Evaluate window if is end of transmition or the window is full
            if len(self.current_window) == CommunicationSettings.window_size or is_eot:
                for i in range(len(self.current_window)):
                    #If the packet isn't valid ask for retransmition and break the check
                    if self.current_window[i].get_valid() == False:
                        if CommunicationSettings.logging:
                            print(f"{self.name}: Invalid window on packet {i}")
                        response = ResponsePacket(key=i)
                        response.mark_as_retransmit()
                        self.sender.recieve_packet(response)
                        return

                if CommunicationSettings.logging:
                    print(f"{self.name}: Valid window")

                #Add data
                for packet in self.current_window:
                    if packet.is_eot() == False:
                        self.good_packets.append(packet.get_data())
                    else:
                        is_eot = True

                #Clear the current window
                self.current_window.clear()

                #If end of transmition then stop the simulation end recreate the image
                if is_eot:
                    self.simulate = False
                    self.recreate_image()

                #Send a request for a new window
                response = ResponsePacket()
                response.mark_as_not_retransmit()
                response.set_max_key()
                self.sender.recieve_packet(response)

        else:
            #Is a response packet. That means that we should transmit our last response again
            response = ResponsePacket(self.last_response_key, self.last_response)
            self.sender.recieve_packet(response)
