class Packet1:
    def __init__(self, key, value):
        """Pole przechowujące klucz pakietu"""
        self.key = key
        """Pole przechowujące wartość do wysłania"""
        self.value = value

    def to_string(self):
        return f"Key: {self.key}, value: {self.value}"

    # Settery i gettery do enkapsulacji danych
    def get_key(self):
        return self.key

    def get_value(self):
        return self.value

    def set_key(self, key):
        self.key = key

    def set_value(self, value):
        self.value = value
