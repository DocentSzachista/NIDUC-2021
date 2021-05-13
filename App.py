#Punkt wejścia do programu
from Terminals       import Terminal
from Container1      import Container1
from TerminalOptions import TerminalOptions
from EncodingOptions import EncodingOptions
from NoiseOptions    import NoiseOptions

import time

# definicja ARQ stop_and wait w przesylaniu (naiwna implementacja bo dzialamy w obrebie aplikacji)
def stop_and_wait(terminal, packet ):
    while(True):
        if terminal.send_message(packet, False) is True:
            return
        else:
            time.sleep(3)
    
#Testowa komunikacja
terminal1 = Terminal("Terminal1", TerminalOptions.stop_and_wait, EncodingOptions.parity_bit, 0, 1024)
terminal2 = Terminal("Terminal2", TerminalOptions.stop_and_wait, EncodingOptions.parity_bit, 0, 1024)

#Komentarz do próbnego commita
terminal1.bind(terminal2)
terminal2.bind(terminal1)
terminal1.send_message("bee.png")
#reader.create_file(byte_list, "bee2.png")
