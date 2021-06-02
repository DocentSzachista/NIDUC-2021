#Punkt wejścia do programu
from Statistics import Statistics
from SenderSAW import SenderSAW
from RecieverSAW import RecieverSAW
from SenderGBN import SenderGBN
from RecieverGBN import RecieverGBN
from CommunicationSettings import CheckSum, CommunicationSettings, NoiseType

def stop_and_wait_test(file_name: str, second_file_name: str) -> None:
    stats = Statistics()

    #Create sender and reciever
    sender = SenderSAW("Sender", stats)
    reciever = RecieverSAW("Reciever", stats)

    reciever.set_recreated_image_name(second_file_name)

    #Bind them
    sender.bind(reciever)
    reciever.bind(sender)

    #Start them
    sender.start()
    reciever.start()

    #Start transmition
    sender.send_image(file_name)

def go_back_n_test(file_name: str, second_file_name: str) -> None:
    stats = Statistics()

    #Create sender and reciever
    sender = SenderGBN("Sender", stats)
    reciever = RecieverGBN("Reciever", stats)

    reciever.set_recreated_image_name(second_file_name)

    #Bind them
    sender.bind(reciever)
    reciever.bind(sender)

    #Start them
    sender.start()
    reciever.start()

    #Start transmition
    sender.send_image(file_name)


#Initialize the test settings
CommunicationSettings.check_sum = CheckSum.CRC
CommunicationSettings.noise = NoiseType.Simple
CommunicationSettings.data_bytes = 4096
CommunicationSettings.key_bits = 16
CommunicationSettings.switch_probability = 0.00001
CommunicationSettings.window_size = 5
CommunicationSettings.logging = True  # Enable debug logging

#stop_and_wait_test("bee.png", "bee2.png")
go_back_n_test("bee.png", "bee2.png")
