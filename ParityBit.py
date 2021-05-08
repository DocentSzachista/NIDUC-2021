class ParityBit:

    """Metoda, która dołącza bit parzystości"""
    @staticmethod
    def add_parity_bit(value):
        number_of_1 = 0
        for i in range(len(value)):
            if value[i] == 1:
                number_of_1 += 1
        if number_of_1 % 2 == 0:
            value.append(0)
        else:
            value.append(1)

        return value
