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

#ARQ mode that the terminals will use in the simulation
class ARQType(Enum):
    Stop_and_wait = 0
    Go_back_n = 1
    Selective_repeat = 2

#Type of noise to use when scrambling the data
class NoiseType(Enum):
    Simple = 0
    Efficient = 1

#Class that holds all of the settings for the current communication simulation
class CommunicationSettings:
    #Default settings
    arg_mode = ARQType.Stop_and_wait
    check_sum = CheckSum.Parit_bit
    noise = NoiseType.Simple
    data_size = 1024
    key_size = 8
    simulate = True
    switch_probability = 0

    #Method that allows you to change the simulation settings. This should only be called before the simulation starts
    @staticmethod
    def setup_communication(arq: ARQType, check_sum: CheckSum, noise: NoiseType, data_size: int, key_size: int, bit_switch_probability: float) -> None:
        CommunicationSettings.arg_mode = arq
        CommunicationSettings.check_sum = check_sum
        CommunicationSettings.noise = noise

        CommunicationSettings.data_size = data_size
        CommunicationSettings.key_size = key_size

        if bit_switch_probability < 0.0 or bit_switch_probability > 1.0:
            print("Bit switch probability has to be between 0 an 1")
        else:
            CommunicationSettings.switch_probability = bit_switch_probability

    #Method that will encode the send data using the selected method
    @staticmethod
    def encode_message(message: str) -> str:
        encodedMessage = ""
        if CommunicationSettings.check_sum is CheckSum.Parit_bit:
            encodedMessage = ParityBit.add_parity_bit(message)
        elif CommunicationSettings.check_sum is CheckSum.CRC:
            print("CRC")
            encodedMessage = CRC.encode_data(message)
        elif CommunicationSettings.check_sum is CheckSum.Hamming_code:
            print("hamming")
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
