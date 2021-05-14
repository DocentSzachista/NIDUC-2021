import random

class Noise:
    #Switches 0 to 1 an 1 to 0 in a string
    def swap_bit(bit: str) -> str:
        if bit == '1':
            return '0'
        else:
            return '1'

    #Simple noise. Tests the probability for each bit
    @staticmethod
    def simple_noise(data, switch_probability):
        data_list = list(data)
        for i, c in enumerate(data_list):
            if switch_probability >= random.random():
                data_list[i] = Noise.swap_bit(c)
        return ''.join(data_list)

    #Different noise algorithm
    @staticmethod
    def efficient_noise(data, switch_probability):
        data_list = list(data)
        length = len(data_list)
        prob = random.triangular(0, length, length * switch_probability) #Calculate the amount of bits to switch
        bits_to_switch = int(round(prob)) #Round it to an integer

        for i in range(bits_to_switch):
            index = random.randint(0, length - 1) #Switch bit on a random position
            data_list[index] = Noise.swap_bit(data_list[index])
        return ''.join(data_list)