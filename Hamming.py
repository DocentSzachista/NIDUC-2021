class Hamming:
    # Determinate how many redundant bits is needed
    @staticmethod
    def numOfRedundantBits(data_length):
        # 2^i >= data_lenght + i + 1
        # 2^i - position of redundant bits
        # data_lenght + i + 1 - when we append redundant bits, data bits are moving one position forward
        for i in range(data_length):
            if(2**i >= data_length + i + 1):
                return i


    # Determinate position of redundant bits
    @staticmethod
    def posRedundantBits(data, num_of_r_bits):
        j = 0   # power
        k = 1   # position of data bit
        data_length = len(data)
        result = ''

        for i in range(1, data_length + num_of_r_bits + 1):
            if(i == 2**j):
                result = result + '0'
                j += 1
            else:
                result = result + data[-1 * k]  # appended backwards
                k += 1

        # In array result data is appended backwards, so it needs to be reversed
        return result[::-1]


    # Calculating parity bits
    @staticmethod
    def calcParityBits(array, num_of_r_bits):
        array_length = len(array)

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
        error_pos = 0

        # Find parity bits
        for i in range(num_of_r_bits):
            val = 0
            for j in range(1, array_length + 1):
                if(j & (2**i) == (2**i)):   #AND
                    val = val ^ int(array[-1 * j])    #XOR
            
            error_pos = error_pos + val * (10**i)

        if(error_pos == 0):
            return False
        else:
            return True


####  TEST  ##############
# hamming = Hamming()
# data = '101101'
# print("Data:        " + data)

# data_length = len(data)
# num_of_r_bits = Hamming.numOfRedundantBits(data_length)

# arr = Hamming.posRedundantBits(data, num_of_r_bits)
# arr = Hamming.calcParityBits(arr, num_of_r_bits)

# print("Coded data:  " + arr)  

# # Simulation of error data
# arr = '10111'
# print("Error data:  "+ arr)
# print("Error:       " + str(Hamming.detectError(arr, num_of_r_bits)))
##################################################