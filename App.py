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
packet = Packet1(0, reader.read_whole())
terminal1.send_message(packet)