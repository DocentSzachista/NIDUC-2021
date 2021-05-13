
from EncodingOptions import EncodingOptions
from ParityBit import ParityBit
from CRC import CRC
from Hamming import Hamming
class Packet2:
    """opcja kodowania"""
    encoding_option = 0

    
    def __init__(self, key = 0, value = '', ):
        """Pole przechowujące klucz pakietu"""
        self.key = key
        """Pole przechowujące wartość do wysłania"""
        self.value = value
    
    
    def convert_to_bin(self):
        string = ''
        string += bin(self.key)[2:].zfill(8)
        string += self.value

    # Warunki do kodowania pakietu
        if Packet2.encoding_option is EncodingOptions.parity_bit:
            print("parity")
            string = ParityBit.add_parity_bit(string)
        elif Packet2.encoding_option is EncodingOptions.CRC:
            print("CRC")
            string = CRC.encode_data(string)
        elif Packet2.encoding_option is EncodingOptions.hamming:
            print("hamming")
            num_of_r_bits = Hamming.numOfRedundantBits(len(string))
            arr = Hamming.posRedundantBits(string, num_of_r_bits)
            string = Hamming.calcParityBits(arr, num_of_r_bits)
        return string

    def convert_to_packet(self, binary):
        str1 = binary[0:8]
        self.key = int(str1, 2)
        # *8 bo rozmiar to bajty +8 bo offset na klucz
        str2 = binary[8:16]
        self.value = str2

        if Packet2.encoding_option is EncodingOptions.parity_bit:
            return  ParityBit.check_parity(binary) 
        
        elif Packet2.encoding_option is EncodingOptions.CRC:   
            return  CRC.check_CRC(binary)
        
        elif Packet2.encoding_option is EncodingOptions.hamming:
            print("Hamming")
    def get_key(self):
        return self.key

    def get_value(self):
        return self.value
