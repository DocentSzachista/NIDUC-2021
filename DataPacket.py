from CommunicationSettings import CommunicationSettings

#Packet that is only used for sending data
class DataPacket:

    def __init__(self, key: int = 0, data: str = "0") -> None:
        self.key = key
        self.data = data
        self.valid = True
        self.eot = False

    #Method that converts the packet data to it's binary representation 
    #and encodes it with the method selected in CommunicationSettings
    def to_binary(self) -> str:
        binary = ""
        binary += bin(self.key)[2:].zfill(CommunicationSettings.key_size)
        binary += self.data
        return CommunicationSettings.encode_message(binary)

    def to_packet(self, message: str) -> None:
        #TODO: Change this convertion to include the ability to decode hamming code
        key_str = message[0:CommunicationSettings.key_size]
        self.key = int(key_str, 2)
        self.data = message[CommunicationSettings.key_size: CommunicationSettings.data_size * 8 + CommunicationSettings.key_size]
        self.is_valid = CommunicationSettings.is_message_valid(message)
        if key_str == "".rjust(CommunicationSettings.key_size, "1"):
            self.eot = True

    #Returns true if the packet contains valid data
    def get_valid(self) -> bool:
        return self.valid

    #Returns the key of the packet
    def get_key(self) -> int:
        return self.key

    #Returns the data that the packet contains
    def get_data(self) -> str:
        return self.data

    #Marks the packet as end of transmiton
    def mark_as_eot(self) -> None:
        #All 1 means end of transmition
        self.key = int("".rjust(CommunicationSettings.key_size, "1"), 2)
        self.data = "".rjust(CommunicationSettings.data_size * 8, "1")

    #Checks if the packet signals the end of transmition
    def is_eot(self) -> bool:
        return self.eot
