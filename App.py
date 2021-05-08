#Punkt wejścia do programu
from Packet1 import Packet1
from Terminals import Terminal
from FileReading import FileReader
import time

# definicja ARQ stop_and wait w przesylaniu (naiwna implementacja bo dzialamy w obrebie aplikacji)
def stop_and_wait(terminal, packet ):
    while(True):
        if terminal.send_message(packet, False) is True:
            return
        else:
            time.sleep(3)


#Testowa komunikacja
terminal1 = Terminal("Terminal1")
terminal2 = Terminal("Terminal2")

#Komentarz do próbnego commita
terminal1.bind(terminal2)
terminal2.bind(terminal1)

reader = FileReader()
reader.open_file("bee.png", "rb")

naive_key = 0
for file_chunk in reader.read_chunk(1024):
    packet = Packet1(naive_key, file_chunk)
    naive_key += 1
    stop_and_wait(terminal1, packet)

terminal1.send_message(None, True)
