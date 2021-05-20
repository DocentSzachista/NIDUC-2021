import textwrap
from typing import List

from DataPacket import DataPacket
from CommunicationSettings import CommunicationSettings

# refactor file wrtiting
class FileReader:
    #Method that reads the binary file and translates it to a list of string with only 0 and 1. Each string i word_size in bytes long 
    @staticmethod
    def read_file(file_name: str, word_size: int) -> list:
        with open(file_name, "rb") as file:
            #File reading as a bytearray
            ba = bytearray(file.read())
            bytes_list = []
            for b in ba:
                #Convertion of bytes to binary 
                bytes_list.append(bin(b)[2:].zfill(8))

            return_list = []
            for i in range(len(bytes_list)):
                if i % word_size == 0:
                    return_list.append(''.join(bytes_list[i:(i + word_size)]))

            return return_list

    #Method that recreates the file based on the provided byte list
    @staticmethod
    def create_file(file_content_list: list, file_name: str):
        with open(file_name, "wb") as file:
            bytes_list = []
            for word in file_content_list:
                parts = textwrap.wrap(word, 8)  #Words to bytes
                bytes_list.extend(parts)

            values = []
            for b in bytes_list:
                #Binary to numeric values
                values.append(int(b, 2))

            #Convertion of the numeric values to a bytearray
            ba = bytearray(values)
            file.write(ba)