class CRC:
    
    static_divisor = '101'
    # Metoda pełniąca rolę logicznego XOR
    @staticmethod
    def xor(arg1, arg2):
        # tablica na rezultat
        result = []
        for i in range(1, len(arg2)):
            if arg1[i] == arg2[i]:
                result.append('0')
            else:
                result.append('1')
        # Zwraca nic dołączając tablice result
        return ''.join(result)

    @staticmethod
    def mod2division(divident, divisor):
        # Liczba bitów, które podlegają XOR (długość dzielnika)
        pick = len(divisor)

        tmp = divident[0:pick]

        while pick < len(divident):
            if tmp[0] == '1':
                tmp = CRC.xor(divisor, tmp) + divident[pick]
            else:
                tmp = CRC.xor('0'*pick, tmp) + divident[pick]
            pick += 1

        if tmp[0] == '1':
            tmp = CRC.xor(divisor, tmp)
        else:
            tmp = CRC.xor('0'*pick, tmp)

        checkword = tmp
        return checkword

    @staticmethod
    def encode_data(data):
        l_key = len(CRC.static_divisor )

        appended_data = data + '0'*(l_key-1)
        remainder = CRC.mod2division(appended_data, CRC.static_divisor )

        coded_word = data + remainder
        return coded_word

    @staticmethod
    def decode_data(data):
        l_key = len(CRC.static_divisor )
        appended_data = data + '0'*(l_key-1)
        remainder = CRC.mod2division(appended_data, CRC.static_divisor )

        return remainder

    @staticmethod
    def check_CRC(binary):
        result = CRC.decode_data(binary)
        for i in range(len(result)):
            if result[i] == '1':
                return False
        return True
