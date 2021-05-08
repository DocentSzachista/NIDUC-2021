import random

class Noise:
    #Metoda zamieniająca w ciągu 0 na 1 i odwrtonie
    def swap_bit(bit):
        if bit == '1':
            return '0'
        else:
            return '1'

    #Proste zaszumianie sygnału za pomocą testowania prawdopodobieństwa dla każdej wielkości po kolei
    @staticmethod
    def simple_noise(data, switch_probability):
        data_list = list(data)
        for i, c in enumerate(data_list):
            if switch_probability >= random.random():
                data_list[i] = Noise.swap_bit(c)
        return ''.join(data_list)

    #Zaszumianie bez przechodzenia przez wszystkie bity
    @staticmethod
    def performant_noise(data, switch_probability):
        data_list = list(data)
        length = len(data_list)
        prob = random.triangular(0, length, length * switch_probability) #Wylosowanie ile bitów powinno być zmienionych
        bits_to_switch = int(round(prob))

        for i in range(bits_to_switch):
            index = random.randint(0, length - 1) #Wybranie losowego miejsca do zmiany znaku
            data_list[index] = Noise.swap_bit(data_list[index])

        return ''.join(data_list)