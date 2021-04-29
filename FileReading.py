
class FileReader:
    #Konstruktor
    binaries=[]
    file=0
    reading_mode=0
    def __init__(self):
        pass
    #Otwieranie pliku do odczytu
    def open_file(self, filename, reading_mode):
        self.reading_mode=reading_mode
        self.file=open(filename, self.reading_mode)

    #zamykanie pliku
    def close_file(self):
        self.file.close()       
    #czytanie fragmentu pliku    
    def read_chunk(self, chunksize ):
        
        while True:
            file_part= self.file.read(chunksize) 
            #jezeli plik sie konczy  to wyjdz inaczej przekaz fragment pliku
            if not file_part:
                break
            yield file_part
    
    #Zapisywanie fragmentow do listy, wykorzystuje reach_chunk'a
    def read_and_safe_to_list(self, chunk=1024):
        if self.reading_mode == "rb":
            for piece in files.read_chunk(chunk):
                self.binaries.append(piece)
        else:
            print("ZLy modyfikator do odczytu")

    #wpisywanie do pliku 
    def write_to_file(self):
        if self.reading_mode == "wb":
            for chunk in self.binaries:
                self.file.write(chunk)
        else:
            print("ZLy modyfikator do odczytu")
    
    def read_whole(self)->str:
        dane = self.file.read()
        return dane
        
    def write_whole(self, message):
        self.file.write(message)
#Wykonywanie programu By zobaczyc ze dziala :D 

files=FileReader()
files.open_file("bee.png", "rb")
files.read_and_safe_to_list(2048)
files.close_file()
files.open_file("bee2.png", "wb")
files.write_to_file()