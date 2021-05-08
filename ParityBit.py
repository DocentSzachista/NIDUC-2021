class ParityBit:

    """Metoda, która dołącza bit parzystości"""
    @staticmethod
    def add_parity_bit(value):
        number_of_1 = 0
        for i in range(len(value)):
            if value[i] == '1':
                number_of_1 += 1
        if number_of_1 % 2 == 0:
            value += '0'
        else:
            value += '1'

        return value

    @staticmethod
    def check_parity(value):
        if type(value) != str:
            return False
        """Zwraca True jeśli prawidłowo"""
        len_val = len(value)
        parity_bit = value[-1]
        numb_1 = 0
        for i in range(len_val-1):
            if value[i] == '1':
                numb_1 += 1

        residue = numb_1 % 2

        if parity_bit == '1' and residue == 1:
            return True
        elif parity_bit == '1' and residue == 0:
            return False
        elif parity_bit == '0' and residue == 1:
            return False
        elif parity_bit == '0' and residue == 0:
            return True
        else:
            return False
