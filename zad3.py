""" Да се напише програма во која клиентите праќаат порака до серверот со која се
регистрираат. Откако ќе се регистрираат, клиентите можат да праќаат пораки до друг
клиент. Истовремено при праќање на порака, клиентите може да примаат пораки од страна
на други клиенти. Препраќањето на пораките го врши серверот. """

import sys, socket, threading

class korisnik():
    def __init__(self, ime,prezime,korime,lozinka,adresa):
        self.ime, self.prezime, self.korime, self.lozinka, self.adresa = ime, prezime,korime,lozinka,adresa
        self.razgovori = {}     #na pochetokot e prazno, tuka ke se sodrzat site razgovori na eden korisnik

    def dodajPoraka(self, poraka,korisnik):
        if korisnik in self.razgovori:  #ako korisnikot e vekje najaven, togash
            self.razgovori[korisnik] += [poraka]    #porakite samo ke se dodavaat na vekje postoechkiot razgovor
        else:                               # ako korisnikot ne postoel do ovoj moment 
            self.razgovori[korisnik] = []   # se kreira razgovor za korisnikot i se dodavaat negovite poraki
            self.razgovori[korisnik] += [poraka]

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
MAX = 65535
PORT = 12345 #1060 

def klientPrimaj(s):    
    while(True):        #postojano moze da prima poraki 
        data,address = s.recvfrom(MAX)
        print(data.decode()) #dekodiranata ja vrakja od bajti vo obichnata kako shto e prvichnata   

if sys.argv[1:] == ['server']:
    korisnici = {}  #kreirame prazna lista na korisnici
    s.bind(('127.0.0.1', PORT))     # se povikuva serverot 
    print('Listening at:', s.getsockname()) # se povikuva na 127.0.0.1 i porta 12345

    while True:             #ovoj while ciklus e za da moze postojano da se odviva komunikacijata, postojano da se prakjat poraki 
        data,address = s.recvfrom(MAX)
        poraka = data.decode().split("|")
        tip = poraka[0]
        if tip == "zdravo":
            ime = poraka[1]
            prezime = poraka[2]
            korime = poraka[3]
            lozinka = poraka[4]
            korisnici[korime] = korisnik(ime,prezime,korime,lozinka,address)  #ovaa adresa e od recvfrom(MAX)
            print('Se najavi: ' + korime)
        elif tip == "porakado":
            korime = poraka[1]
            if korime in korisnici:
                datatosend = poraka[2]
                print(datatosend)
                s.sendto(datatosend.encode(), korisnici[korime].adresa)
            else:
                s.sendto((korime + " ne e najaven").encode(), address)
elif sys.argv[1:] == ['client']:
    ime = input('Vnesi ime:')
    prezime = input('Vnesi prezime: ')
    korime = input('Vnesi korisnichko ime: ')
    lozinka = input('Vnesi lozinka: ')

    s.sendto(("zdravo|" +ime+ "|" +prezime + "|" + korime+ "|" + lozinka).encode() , ('127.0.0.1' , PORT))

    threading.Thread(target = klientPrimaj, args=(s,)).start()  #ova e za da moze dva klienti da komuniciraat, dvonasochnost


    while True:
        dokogo = input("Do kogo: ")
        poraka = input("Poraka: ")
        s.sendto(("porakado|" +dokogo + "|" + poraka).encode(), ('127.0.0.1' , PORT))

else:
    print(sys.stderr, 'usage: zad3.py server|client')



