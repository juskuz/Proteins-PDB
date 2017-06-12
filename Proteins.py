#! /usr/bin/env python3.5

# 21.02.2016

class Atom:

    def __init__(self, line):
        self.ATOM   = line[0:6]
        self.serial = line[6:11]
        self.name   = line[11:16]
        self.altLoc = line[16:17]
        self.resName= line[17:20]
        self.chainID= line[20:22]
        self.resSeq = int(line[22:26])
        #self.iCode  = line[26:27]
        self.x      = line[28:38]
        self.y      = line[38:46]
        self.z      = line[46:]

    def show_atom(self):
        print(self.ATOM+self.serial+self.name+self.altLoc+
              self.resName+self.chainID+" "+str(self.resSeq)+#self.iCode+
              self.x+self.y+" "+self.z)
    
class Protein:

    def __init__(self, plik):
        self.data = []
        self.file_name = plik
        self.lista_atomow=[]

    def open_file(self):
        self.counter = 0
        with open(self.file_name, 'r') as _file:
            self.data = _file.readlines()
            for line in self.data:
                if 'ENDMDL' in line:
                    self.counter += 1

        print("wczytano do programu")
        print("Liczba bialek w pliku:", self.counter)

    def file(self):
        for i in self.data:
            print(i)

    def renum_records(self):
        msg = ("Podaj numer bialka, ktore chcesz"
               " sprawdzic: (od 1 do {}):").format(str(self.counter))
        print(msg)
        self.numer = int(input())
        counter = 0
        sprawdz = 0
        c=0
        #import pdb; pdb.set_trace() # do debugowania
        last_name = '' #poprzedni aminokwas
        last_ID = '' #poprzedni numer
        for line in self.data:           
            c=c+1
            if line[0:5]=='MODEL':
                counter = counter + 1
                if counter == self.numer:
                    sprawdz = 1
                elif counter > self.numer:
                    break
            elif sprawdz == 1:
                if line[0:4] == 'ATOM':
                    if line[17:20] == last_name:
                        new_line=line[0:22]+last_ID+line[26:] #zmien numer na last_ID
                        self.data[c-1]=new_line
                        #print(new_line) #można odkomentować w celu wyświetlenia modyfikacji
                        
                    last_ID = line[22:26]
                    last_name = line[17:20]
                    n=Atom(self.data[c-1]);
                    self.lista_atomow.append(n)
        print("\nPrzenumerowano plik.\n")
        
    def show (self):
        for i in self.lista_atomow:
            i.show_atom()

    def find_residuum(self):
        value=int(input("Podaj szukana wartosc: "))
        found=0
        for i in self.lista_atomow:
            if value == i.resSeq:
                found=1
                print("\nZnaleziono nastepujący wiersz:")
                i.show_atom()
        if found==0:
            print("\nNie znaleziono residuum o takim numerze.\n")

    def show_discontinuous(self):
        nieciaglosci=[]
        for nr, i in enumerate(self.lista_atomow[:-1]):
            num=i.resSeq # wczytanie numeru sekwencji dla każdego atomu z listy
            next_num = self.lista_atomow[nr+1].resSeq
            if next_num-num>1:
                while num+1<next_num:
                    nieciaglosci.append(num+1)
                    num=num+1
        print("Brakujace numery residuów: ")
        for x in nieciaglosci:
            print(x)
            
def menu():
    while True:
        print("\nMENU:\nWybierz, co chcesz zrobić:"
              "\n- 'file' - wyswietlenie wczytanego pliku"
              "\n- 'renum' - przenumerowanie wierszy"
              "\n- 'show' - wyświetlenie atomow białka (dostępne po przenumerowaniu)"
              "\n- 'find' - szukanie konkretnego residuum (dostępne po przenumerowaniu)"
              "\n- 'write' - wypisanie miejsc nieciaglosci residuów (dostępne po przenumerowaniu)"
              "\n- 'end' - zakończenie programu\n")
        wybor=input("Wpisz wybrana opcje: ")

        if wybor == 'renum':
              p.renum_records()
        elif wybor == 'file':
            p.file()
        elif wybor == 'show':
              p.show()
        elif wybor == 'find':
              p.find_residuum()
        elif wybor == 'write':
              p.show_discontinuous()
        elif wybor == 'end':
            break
        else:
            print ("Nie ma takiej opcji. Spróbuj ponownie.\n")


if __name__ == '__main__':
    p = Protein("3GAU.pdb")  # utworzenie obiektu Protein z nazwa pliku
    p.open_file()
    menu()
   
