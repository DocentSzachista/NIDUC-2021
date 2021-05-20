from ResponsePacket import ResponsePacket
from DataPacket import DataPacket
from FileReading import FileReader
from CommunicationSettings import ARQType, CommunicationSettings

from threading import Thread
import time

#####################
#  DEPRECATED!!!!!  # 
#####################
#TODO:
#- Switch to a more sophisticated container solution
#- Complete Stop and wait with noise
#- Implement other methods

#Class that handles communication and ARQ
class Terminal:
    #Initializes the terminal
    def __init__(self, name: str, is_sender: bool) -> None:
        self.name = name
        self.package_queue = [] #Packages that are going to be send or are properly recieved (Change list to something else)
        self.is_sender = is_sender
        self.package_buffer = [] #Packages that are waiting to be evaluated by the algorithm (Change to something else???)
        self.thread = None
        self.last_send_packet = 0 #Debug will remove when package queue is no longer a list
        self.local_run = True #Should the terminal be running

    #Sets the terminal that this terminal will send messages to
    def bind(self, other_terminal) -> None:
        self.connected_terminal = other_terminal

    #Method for starting the terminal thread
    def start_terminal(self) -> None:
        self.thread = Thread(target=self.run_terminal) #Create and start the thread
        self.thread.start()

    #Stops the terminal
    def stop_terminal(self) -> None:
        self.local_run = False #Sets local_run to false. This stops the while loop and kills the thread

    #Sends the message to the connected terminal
    def send_message(self, message: str) -> None:
        self.connected_terminal.recieve_message(message)

    #Recieves the message and pushes it to the package_buffer
    def recieve_message(self, message: str) -> None:
        #TODO: What type of packet it is should be determinated based on the length of the message. No idea how to do it ATM
        #TODO: Here is a good place to scramble the packets
        if self.is_sender:
            packet = ResponsePacket()
            packet.to_packet(message)
            self.package_buffer.append(packet) #Send the decoded packet to the buffer for processing by the thread
            print(f"{self.name}: recieved a ResponsePacket\n")
        else:
            packet = DataPacket()
            packet.to_packet(message)
            self.package_buffer.append(packet)
            print(f"{self.name}: recieved a DataPacket\n")

    #Method that will run on a separate thread and controll the execution of the transmition
    def run_terminal(self) -> None:
        #TODO: Currently this utilizes active waiting. Should change to passive waiting using signals
        while CommunicationSettings.simulate and self.local_run:
            if not self.package_buffer: #If the buffer is empty the continue to wait
                continue
            
            #Based on the ARQ mode go to the specified method to process the package
            if CommunicationSettings.arg_mode is ARQType.Stop_and_wait:
                self.stop_and_wait()
            elif CommunicationSettings.arg_mode is ARQType.Go_back_n:
                self.go_back_n()
            elif CommunicationSettings.arg_mode is ARQType.Selective_repeat:
                self.selective_repeat()

    #TODO: Complete
    def stop_and_wait(self) -> None:
        packet = self.package_buffer.pop(0)
        if self.is_sender:
            #TODO: I have no idea why it doesn't work. When uncomented this doesn't send the first packet
            #if not packet.should_retransmit():
            #    self.last_send_packet += 1
            
            #TODO: Remember to change also those lines
            if self.last_send_packet < len(self.package_queue):
                self.send_message(self.package_queue.pop(0).to_binary())
            else:
                self.stop_terminal()
        else:
            response = ResponsePacket()
            if packet.get_valid(): #If the package is valid process it
                if packet.is_eot(): #If it is end of transmition package then create the file and stop the terminal
                    self.create_file("bee2.png")
                    self.stop_terminal()
                else:
                    #If not the push this packet to the end
                    #And send a confirmation that this 
                    self.package_queue.append(packet)
                    response.mark_as_not_retransmit()
                    self.send_message(response.to_binary())
            else:
                #If the packet is not valid ask for retransmition
                response.mark_as_retransmit()
                self.send_message(response.to_binary())

    #TODO: implement
    def selective_repeat(self) -> None:
        print("Selective repeat")

    #TODO: Implement
    def go_back_n(self) -> None:
        print("Go back n")

    #Method that starts the transmition
    def send_file(self, file_name: str) -> None:
        if self.is_sender is False:
            print("Reciever can't initiate the communication\n")
        else:
            self.create_packages(file_name) #Create the packages from the file
            #TODO: Change the way we start the transmition
            startPacket = ResponsePacket() #Make a start packet that asks for retransmition so we
            startPacket.mark_as_retransmit()
            self.package_buffer.append(startPacket)
            print(f"{self.name}: Data transmition started\n")
    
    #Method that creates packages from the file and adds them to the package queue
    def create_packages(self, file_name: str) -> None:
        byte_list = FileReader.read_file(file_name, CommunicationSettings.data_bytes)
        for index, data in enumerate(byte_list): #Convert words to packages
            self.package_queue.append(DataPacket(index, data))
        
        #Create an end of transmition packet and add it to the end of the queue
        end_packet = DataPacket()
        end_packet.mark_as_eot()
        self.package_queue.append(end_packet)
        print(f"Created {len(self.package_queue)} packages\n")

    #Method that recreates the file from the data that is in the package_queue
    def create_file(self, file_name: str) -> None:
        print(f"Packages recieved: {len(self.package_queue)}")
        print(f"Creating file {file_name}\n")
        #TODO: Maybe sort the list first to make shure that packages are in the correct order
        byte_list = []
        for package in self.package_queue:
            byte_list.append(package.get_data())
        FileReader.create_file(byte_list, file_name)
