
from EncodingOptions import EncodingOptions
from ParityBit import ParityBit
from CRC import CRC
from Hamming import Hamming
class Packet1:

    def __init__(self, key = 0, value = '', encoding_option='' ):
        """Pole przechowujące klucz pakietu"""
        self.key = key
        """Pole przechowujące wartość do wysłania"""
        self.value = value
        """dlugosc pakietu"""
        self.length = len(value)
        """opcja kodowania"""
        self.encoding_option = encoding_option

    def convert_to_bin(self):
        string = ''
        string += bin(self.key)[2:].zfill(8)
        string += self.value

    # Warunki do kodowania pakietu
        if self.encoding_option is EncodingOptions.parity_bit:
            print("parity")
            string = ParityBit.add_parity_bit(string)
        elif self.encoding_option is EncodingOptions.CRC:
            print("CRC")
            string = CRC.encode_data(string)
        elif self.encoding_option is EncodingOptions.hamming:
            print("hamming")
            num_of_r_bits = Hamming.numOfRedundantBits(len(string))
            arr = Hamming.posRedundantBits(string, num_of_r_bits)
            string = Hamming.calcParityBits(arr, num_of_r_bits)
        return string

    def convert_to_packet(self, binary):
        str1 = binary[0:8]
        self.key = int(str1, 2)
        str2 = binary[8:-1]
        self.value = str2


    def to_string(self):
        return f"Key: {self.key}, value: {self.value}"

    def add_bit(self, bit):
        if bit == '1' or bit == '0':
            self.value += bit

    def clear_value(self):
        self.value = ''

    # Settery i gettery do enkapsulacji danych
    def get_key(self):
        return self.key

    def get_value(self):
        return self.value

    def set_key(self, key):
        self.key = key

    def set_value(self, value):
        self.value = value

    
