from Packet1         import Packet1
from TerminalOptions import TerminalOptions
from EncodingOptions import EncodingOptions
from NoiseOptions    import NoiseOptions
class Container1:
     def __init__(self):
         """Lista przechowująca obiekty - pakiety"""
         self.container = []

     def push(self, Packet1, encoding_option):
      
        self.container.append(Packet1)

     def insert(self, Packet1, index):
         if index < len(self.container):
             self.container.insert(Packet1, index)
         else:
             return None

     def pop(self):
         if len(self.container) > 0:
             return self.container.pop()
         else:
             return None

     def get(self, index):
         if index < len(self.container):
            return self.container[index]
         else:
            return  None

     def length(self):
         return len(self.container)

     def get_beginning(self):
         if len(self.container) > 0:
            return self.container.pop(0)
         else:
            return None

