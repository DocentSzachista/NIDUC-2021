class Packet1:
    def __init__(self, key, value):
        """Pole przechowujące klucz pakietu"""
        self.key = key
        """Pole przechowujące wartość do wysłania"""
        self.value = value
        """Informacja o potrzebie retransmisji"""
        self.retransmission = False

    def convert_to_bin(self):
        string = ''
        string += bin(self.key)[2:].zfill(8)
        string += self.value
        return string

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

    def get_retransmission(self):
        return self.retransmission

    def set_retransmission(self, ret):
        if ret is True or ret is False:
            self.retransmission = ret
