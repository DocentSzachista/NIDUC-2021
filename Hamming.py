class Hamming:
    # Ile bitów kontrolnych trzeba dodać
    @staticmethod
    def numOfRedundantBits(data_length):
        # 2^i >= data_lenght + i + 1
        # 2^i - bity kontrolne dodajemy na pozycje będące potegą 2
        # data_lenght + i + 1 - dodajemy 1 bo pozycje kolejnych bitów się przesuwają po dodaniu bitu kontrolnego

        for i in range(data_length):
            if(2**i >= data_length + i + 1):
                return i


    # Wyznaczenie pozycji bitów kontrolnych
    @staticmethod
    def posRedundantBits(data, num_of_r_bits):
        j = 0   # potega
        k = 1   # pozycja bitu danych
        data_length = len(data)
        result = ''

        for i in range(1, data_length + num_of_r_bits + 1):
            if(i == 2**j):
                result = result + '0'
                j += 1
            else:
                result = result + data[-1 * k]  # zapis od tyłu
                k += 1

        # W tablicy result dane są od tyłu, więc trzeba je odwrócić
        return result[::-1]


    # Wyznaczenie bitów parzystości
    @staticmethod
    def calcParityBits(array, num_of_r_bits):
        array_length = len(array)

        # For finding rth parity bit, iterate over
        # 0 to r - 1
        for i in range(num_of_r_bits):
            val = 0

            for j in range(1, array_length + 1):
                if(j & (2**i) == (2**i)):
                    val = val ^ int(array[-1 * j])

            # (0 to n - 2^r) + parity bit + (n - 2^r + 1 to n)
            array = array[:array_length-(2**i)] + str(val) + array[array_length-(2**i)+1:]
        return array

    @staticmethod
    def detectError(array, num_of_r_bits):
        array_length = len(array)
        result = 0

        # Obliczanie bitów parzystości
        for i in range(num_of_r_bits):
            val = 0
            for j in range(1, array_length + 1):
                if(j & (2**i) == (2**i)):
                    val = val ^ int(array[-1 * j])

            result = result + val*(10**i)

        return int(str(result), 2)


####   TEST PROGRAMU  ##############
# hamming = Hamming()
# data = '1011001'
# print("Dane:    " + data)

# data_length = len(data)
# num_of_r_bits = Hamming.numOfRedundantBits(data_length)

# arr = Hamming.posRedundantBits(data, num_of_r_bits)
# arr = Hamming.calcParityBits(arr, num_of_r_bits)

# print("Dane zakodowane: " + arr)  

# # Symulacja błędu na 10 pozycji
# arr = '11101001110'
# print("Błedne dane:     "+ arr)
# correction = Hamming.detectError(arr, num_of_r_bits)
# print("Pozycja błędu:   " + str(correction))
##################################################