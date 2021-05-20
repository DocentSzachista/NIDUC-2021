from enum import Enum

from ParityBit import ParityBit
from CRC import CRC
from Hamming import Hamming

from Noise import Noise

#Checks sum that will be used when evaluating if the packet is valid or not
class CheckSum(Enum):
    Parit_bit = 0
    CRC = 1
    Hamming_code = 2

#Type of noise to use when scrambling the data
class NoiseType(Enum):
    Simple = 0
    Efficient = 1

#Class that holds all of the settings for the current communication simulation
class CommunicationSettings:
    #Default settings
    check_sum = CheckSum.Parit_bit
    noise = NoiseType.Simple
    data_bytes = 1024
    key_bits = 8
    switch_probability = 0
    logging = True

    #Method that will encode the send data using the selected method
    @staticmethod
    def encode_message(message: str) -> str:
        encodedMessage = ""
        if CommunicationSettings.check_sum is CheckSum.Parit_bit:
            encodedMessage = ParityBit.add_parity_bit(message)
        elif CommunicationSettings.check_sum is CheckSum.CRC:
            encodedMessage = CRC.encode_data(message)
        elif CommunicationSettings.check_sum is CheckSum.Hamming_code:
            num_of_r_bits = Hamming.numOfRedundantBits(len(message))
            arr = Hamming.posRedundantBits(message, num_of_r_bits)
            encodedMessage = Hamming.calcParityBits(arr, num_of_r_bits)
        return encodedMessage
    
    #Checks if the provided message is valid using the selected check sum
    @staticmethod
    def is_message_valid(message: str) -> bool:
        if CommunicationSettings.check_sum is CheckSum.Parit_bit:
            return ParityBit.check_parity(message)
        elif CommunicationSettings.check_sum is CheckSum.CRC:
            return  CRC.check_CRC(message)
        elif CommunicationSettings.check_sum is CheckSum.Hamming_code:
            print("Hamming code detection not implemented")
            return False

    #Header method that scrambles the message using the selected algorithm
    @staticmethod
    def scramble_message(message: str) -> str:
        if CommunicationSettings.noise is NoiseType.Simple:
            return Noise.simple_noise(message, CommunicationSettings.switch_probability)
        elif CommunicationSettings.noise is NoiseType.Efficient:
            return Noise.efficient_noise(message, CommunicationSettings.switch_probability)
