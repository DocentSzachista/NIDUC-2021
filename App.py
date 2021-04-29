#Punkt wejścia do programu
from Packet1 import Packet1
from Terminals import Terminal
from FileReading import FileReader

#Testowa komunikacja
terminal1 = Terminal("Terminal1")
terminal2 = Terminal("Terminal2")

#Komentarz do próbnego commita
terminal1.bind(terminal2)
terminal2.bind(terminal1)

reader = FileReader()
reader.open_file("bee.png", "rb")

naive_key = 0
for file_chunk in reader.read_chunk():
    packet = Packet1(naive_key, file_chunk)
    naive_key += 1
    terminal1.send_message(packet, False)
terminal1.send_message(None, True)