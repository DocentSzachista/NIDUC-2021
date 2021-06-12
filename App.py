#Punkt wejścia do programu
from Statistics import Statistics
from SenderSAW import SenderSAW
from RecieverSAW import RecieverSAW
from SenderGBN import SenderGBN
from RecieverGBN import RecieverGBN
from SenderSR import SenderSR
from RecieverSR import RecieverSR
from CommunicationSettings import CheckSum, CommunicationSettings, NoiseType

#Halts the main thread until the simulation is finished
def wait_for_simulation_end() -> None:
    while(CommunicationSettings.get_simulation_state() == False):
        continue

def stop_and_wait_test(file_name: str, repetitions: int) -> None:
    for i in range(repetitions):
        #Print proggress
        print(f"Run {i + 1}/{repetitions}")
        stats = Statistics()

        #Setup test specific statistics
        CommunicationSettings.check_sum = CheckSum.CRC

        #Create sender and reciever
        sender = SenderSAW("Sender", stats)
        reciever = RecieverSAW("Reciever", stats)

        #Setup resoult image name
        reciever.set_recreated_image_name(f"Img/res_saw{i + 1}.png")

        #Bind them
        sender.bind(reciever)
        reciever.bind(sender)

        #Start them
        sender.start()
        reciever.start()

        #Start transmition
        sender.send_image(file_name)

        wait_for_simulation_end()
        print(stats.get_statistics())
        CommunicationSettings.reset_sumulation_state()

def go_back_n_test(file_name: str, repetitions: int) -> None:
    for i in range(repetitions):
        #Print proggress
        print(f"Run {i + 1}/{repetitions}")
        stats = Statistics()

        #Setup test specific statistics
        CommunicationSettings.check_sum = CheckSum.CRC
        CommunicationSettings.window_size = 4

        #Create sender and reciever
        sender = SenderSAW("Sender", stats)
        reciever = RecieverSAW("Reciever", stats)

        #Setup resoult image name
        reciever.set_recreated_image_name(f"Img/res_gbn{i + 1}.png")

        #Bind them
        sender.bind(reciever)
        reciever.bind(sender)

        #Start them
        sender.start()
        reciever.start()

        #Start transmition
        sender.send_image(file_name)

        wait_for_simulation_end()
        print(stats.get_statistics())
        CommunicationSettings.reset_sumulation_state()

def selective_repeat_test(file_name: str, repetitions: int) -> None:
    for i in range(repetitions):
        #Print proggress
        print(f"Run {i + 1}/{repetitions}")
        stats = Statistics()

        #Setup test specific statistics
        CommunicationSettings.check_sum = CheckSum.CRC
        CommunicationSettings.window_size = 4

        #Create sender and reciever
        sender = SenderSAW("Sender", stats)
        reciever = RecieverSAW("Reciever", stats)

        #Setup resoult image name
        reciever.set_recreated_image_name(f"Img/res_sr{i + 1}.png")

        #Bind them
        sender.bind(reciever)
        reciever.bind(sender)

        #Start them
        sender.start()
        reciever.start()

        #Start transmition
        sender.send_image(file_name)

        wait_for_simulation_end()
        print(stats.get_statistics())
        CommunicationSettings.reset_sumulation_state()

#Global settings (the same for all tests)
CommunicationSettings.noise = NoiseType.Simple
CommunicationSettings.data_bytes = 128 #W bajtach 128 * 8 = 1024 bity 
CommunicationSettings.key_bits = 16
CommunicationSettings.switch_probability = 0.0001
CommunicationSettings.logging = False  # Logging will clutter the console, so keep it disabled

#------------
#INSTRUCTIONS
#------------
#There are some specific settings in the methods (CheckSum and window size)
#To run the test, uncomment the type you want to test and run the application. Resoults will be printed on the console
#Genereated images will be in the "Img" folder

#The string is the name of the image to send
#The number is the amount of tests

#stop_and_wait_test("bee.png", 20)
#go_back_n_test("bee.png", 20)
#selective_repeat_test("bee.png", 20)
