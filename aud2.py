""" Да се напише програма во која клиентите праќаат порака до серверот со која се
регистрираат. Откако ќе се регистрираат, клиентите можат да праќаат пораки до друг
клиент. Истовремено при праќање на порака, клиентите може да примаат пораки од страна
на други клиенти. Препраќањето на пораките го врши серверот. """


import sys, socket, threading
# threading za da moze megju klienti

class Korisnik():
    def __init__(self, ime,prezime,korime,lozinka,adresa):
        self.ime, self.prezime, self.korime, self.lozinka, self.adresa = ime, prezime, korime, lozinka, adresa
        self.razgovori = {}

    def dodajPoraka(self, poraka, korisnik):    #korisnikot e do kogo ili od kogo ??
        if korisnik in self.razgovori:
            self.razgovori[korisnik] += [poraka]
        else:
            self.razgovori[korisnik] = []
            self.razgovori[korisnik] += [poraka]

s = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)
MAX = 65535
PORT = 1060

def klientPrimaj(s):
    while(True):
        data, address = s.recvfrom(MAX)
        print(data.decode())

if sys.argv[1:] == ['server']:
    korisnici = {}  #prazna lista na korisnici
    #sega treba da se povika serverot
    s.bind(('127.0.0.1' , PORT))
    print("Listening at: ", s.getsockname())

    while True:
        data, address = s.recvfrom(MAX)
        poraka = data.decode().split(".")
        tip = poraka[0]
        if tip == 'zdravo':
            ime = poraka[1]
            prezime = poraka[2]
            korime = poraka[3]
            lozinka = poraka[4]
            korisnici[korime] = Korisnik(ime,prezime,korime,lozinka,address)
            print("Se najavi korisnikot " + korime)
        elif tip == 'porakado':
            korime = poraka[1]
            if korime in korisnici:
                pratenaporaka = poraka[2]
                print("Poraka: " + pratenaporaka)
                s.sendto(pratenaporaka.encode() , korisnici[korime].adresa)
            else:
                s.sendto((korime + " ne e najaven").encode(), address)
elif sys.argv[1:] == ['client']:
    ime = input ('Vnesi ime: ')
    prezime = input('Vnesi prezime: ')
    korime = input('Vnesi korisnichko ime: ')
    lozinka = input('Vnesi lozinka: ')

    s.sendto(("zdravo." + ime + "." + prezime + "." + korime + "." + lozinka).encode() , ('127.0.0.1', PORT))

    threading.Thread(target = klientPrimaj, args = (s,)).start()
    while True:
        dokogo = input('Do kogo sakate da ispratite poraka? ')
        poraka = input('Poraka: ')
        s.sendto(("porakado." + dokogo + "." + poraka).encode(), ('127.0.0.1', PORT))

else: 
    print(sys.stderr, 'Usage: python zad.py client|server')
