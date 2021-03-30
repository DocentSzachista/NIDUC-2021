
class FileReader:
    #Konstruktor
    def __init__(self, filename):
        self.filename=filename
        self.binaries=[]

    #Otwieranie pliku do odczytu
    def open_file(self):
        self.file=open(self.filename, "rb")

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
     
        for piece in files.read_chunk(chunk):
            self.binaries.append(piece)

    #wpisywanie do pliku 
    def write_to_file(self, filename):
        self.file=open(filename, "wb")
        for chunk in self.binaries:
            self.file.write(chunk)

#Wykonywanie programu By zobaczyc ze dziala :D 

files=FileReader("bee.png")
files.open_file()
files.read_and_safe_to_list(2048)
files.close_file()
files.write_to_file("bee2.jpg")



