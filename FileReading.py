# refactor file wrtiting 
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
    def read_chunk(self, chunksize=1024 ):
        
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
    def write_to_file(self, message):
        if self.reading_mode == "wb":
            self.file.write(message)
        else:
            print("ZLy modyfikator do odczytu")
    
    def read_whole(self)->str:
        dane = self.file.read()
        return dane
        
    def write_whole(self, message):
        self.file.write(message)
