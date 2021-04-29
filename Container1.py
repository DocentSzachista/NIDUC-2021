from Packet1 import Packet1

class Container1:
     def __init__(self):
         """Lista przechowująca obiekty - pakiety"""
         self.container = []

     def container_push(self, Packet1):
         self.container.append(Packet1)

     def container_insert(self, Packet1, index):
         self.container.insert(Packet1, index)

     def container_pop(self):
         return self.container.pop()

     def container_get(self, index):
         return self.container[index]

     def container_length(self):
         return len(self.container)

