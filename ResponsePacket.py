from CommunicationSettings import CommunicationSettings

#Class that is used to respond to the sender with the information about the packets validity
class ResponsePacket:
    data_length: int = 8 #Data length of the response packet. 8 should be enought

    def __init__(self, key: int = 0, data: str = "0") -> None:
        self.key = key
        self.data = data
        self.valid = True
        self.retransmit = False

    #Method that converts the packet data to it's binary representation
    #and encodes it with the method selected in CommunicationSettings
    def to_binary(self) -> str:
        binary = ""
        binary += bin(self.key)[2:].zfill(CommunicationSettings.key_size)
        binary += self.data
        return CommunicationSettings.encode_message(binary)

    def to_packet(self, message: str) -> None:
        #TODO: Change this convertion to include the ability to decode hamming code
        self.key = int(message[0:CommunicationSettings.key_size], 2)
        self.data = message[CommunicationSettings.key_size: CommunicationSettings.key_size + ResponsePacket.data_length] 
        self.is_valid = CommunicationSettings.is_message_valid(message)

        #Count the amount of ones and zeros in data
        am0 = 0
        am1 = 0
        for c in self.data:
            if c == "0":
                am0 += 1
            else:
                am1 += 1
        
        self.retransmit = am1 >= am0 #If thera are more ones that means that the packet should be retransmited

    #Returns true if the packet contains valid data
    def get_valid(self) -> bool:
        return self.valid

    #Returns the key of the packet
    def get_key(self) -> int:
        return self.key

    #Returns the data that the packet contains
    def get_data(self) -> str:
        return self.data

    #Should this packet say that retransmition is needed
    def mark_as_retransmit(self) -> None:
        self.data = "".rjust(ResponsePacket.data_length, "1") #All ones in data mean that the packet should be retransmited

    #Should this packet say that retransmition is NOT needed
    def mark_as_not_retransmit(self) -> None:
        self.data_length = "".rjust(ResponsePacket.data_length, "0") #All zeros in data mean that the packet shouldn't be retrasmited

    #Checks if the packet calls for retransmition
    def should_retransmit(self) -> bool:
        return self.retransmit
