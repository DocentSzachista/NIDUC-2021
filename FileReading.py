import textwrap

# refactor file wrtiting


class FileReader:
    #Metoda odczytująca plik i zamieniająca go na listę słów o długości word_size w bajtach
    def read_file(file_name, word_size):
        with open(file_name, "rb") as file:
            # Wczytanie pliku i zamiana go na tablice bajtów
            ba = bytearray(file.read())
            bytes_list = []
            for b in ba:
                # Zamiana przeczytanych wartości na binarne ośmio cyfrowe wartości
                bytes_list.append(bin(b)[2:].zfill(8))

            return_list = []
            for i in range(len(bytes_list)):
                if i % word_size == 0:
                    # Łączenie bajtów w słowa o zadanej długości
                    return_list.append(''.join(bytes_list[i:(i + word_size)]))

            return return_list

    #Metoda odtwarzająca plik na podstawie listy słów
    #W liście długość jednego ciągu znaków MUSI być wielokrotnością liczby 8
    def create_file(file_content_list, file_name):
        with open(file_name, "wb") as file:
            bytes_list = []
            for word in file_content_list:
                parts = textwrap.wrap(word, 8)  # Przetworzenie słów na bajty
                bytes_list.extend(parts)

            values = []
            for b in bytes_list:
                # Zamiana binarnie zapisanych bajtów na liczby
                values.append(int(b, 2))

            ba = bytearray(values)
            file.write(ba)  # Zapisanie tych liczb do pliku