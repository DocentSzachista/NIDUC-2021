from Hamming import Hamming
from CommunicationSettings import CommunicationSettings, CheckSum

#Class that is used to respond to the sender with the information about the packets validity
class ResponsePacket:
    def __init__(self, key: int = 0, data: str = "0") -> None:
        self.key = key
        self.data = data
        self.valid = True
        self.retransmit = False

    #Method that converts the packet data to it's binary representation
    #and encodes it with the method selected in CommunicationSettings
    def to_binary(self) -> str:
        binary = ""
        binary += bin(self.key)[2:].zfill(CommunicationSettings.key_bits)
        binary += self.data
        return CommunicationSettings.encode_message(binary)

    def to_packet(self, message: str) -> None:
        original_message = message
        if CommunicationSettings.check_sum == CheckSum.Hamming_code:
            message = Hamming.extractKey(message)

        self.key = int(message[0:CommunicationSettings.key_bits], 2)
        self.data = message[CommunicationSettings.key_bits: CommunicationSettings.key_bits + 1] 
        self.is_valid = CommunicationSettings.is_message_valid(message)

        if self.data == "1":
            self.retransmit = True
        elif self.data == "0":
            self.retransmit = False
        else:
            self.is_valid = False

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
        self.data = "1" #One in data mean that the packet should be retransmited
        self.retransmit = True

    #Should this packet say that retransmition is NOT needed
    def mark_as_not_retransmit(self) -> None:
        self.data_bits = "0" #Zero in data mean that the packet shouldn't be retrasmited
        self.retransmit = False

    #Checks if the packet calls for retransmition
    def should_retransmit(self) -> bool:
        return self.retransmit
