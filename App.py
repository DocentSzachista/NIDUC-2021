#Punkt wejścia do programu
from Terminals import Terminal
from CommunicationSettings import ARQType, CheckSum, CommunicationSettings, NoiseType

#Initialize the test settings
CommunicationSettings.setup_communication(ARQType.Stop_and_wait, CheckSum.Parit_bit, NoiseType.Simple,  1024, 8, 0.001)

#Create two terminals
terminal1 = Terminal("Sender", True)
terminal2 = Terminal("Reciever", False)

#Bind them to eachother
terminal1.bind(terminal2)
terminal2.bind(terminal1)

#Start their threads
terminal1.start_terminal()
terminal2.start_terminal()

#Send the file form terminal1 to terminal2
terminal1.send_file("bee.png")
