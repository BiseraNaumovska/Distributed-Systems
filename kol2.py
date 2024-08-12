""" 1. Да се напише програма која симулира UDP комуникација во која клиентите праќаат порака
до серверот со која се регистрираат со корисничко име, лозинка и дали е вработен или 
корисник. Откако ќе се регистрираат, клиентите можат да праќаат пораки до друг клиент.
Пораката да не може да се прати помеѓу никој клиенти ако е поголема од 48B и тогаш
серверот да одговори дека порака е преголема. Доколку испраќа корисник на вработен може 
да биде до 24B, доколку пак испраќа корисник до корисник може да биде максимум 16B, а 
доколку испраќа вработен до вработен може да биде и до 26B. Доколку пораката не е во 
големина од дозволените граници за конкретната меѓуклиентска комуникација, а е помала од 
48B, серверот да врати за колку бити е надмината границата, а тоа клиентот да го испечати.
Истовремено при праќање на порака, клиентите може да примаат пораки од страна на други
клиенти. Препраќањето на пораките го врши серверот. (40п) """

import sys, socket, threading

class Korisnik():
    def __init__(self, korime,lozinka, vrabotenilikorisnik, adresa):
        self.korime, self.lozinka, self.vrabotenilikorisnik, self.adresa = korime, lozinka, vrabotenilikorisnik, adresa
    
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

MAX = 65535
PORT = 1060
MAX_CLIENT = 48
MAX_KORISNIK_VRABOTEN = 24
MAX_KORISNIK_KORISNIK = 26

#ova mi e za megjusebnata komunikacija na klientite
def primiPoraka(s):
    while True:
        data,address = s.recvfrom(MAX)
        print(data.decode())

if sys.argv[1:] == ['server']:
    korisnici = {}  #prazna lista na korisnici
    #prvo mora da se otvori
    s.bind(('127.0.0.1', PORT))
    print("Serverot slusha na: " , s.getsockname())

    while True:
        #e sega primame podatoci od klienti
        data,address = s.recvfrom(MAX)
        poraka = data.decode().split('.')
        tip = poraka[0]
        if tip == 'Connect':
            korime = poraka[1]
            lozinka = poraka[2]
            vrabotenilikorisnik = poraka[3]
            korisnici[korime] = Korisnik(korime,lozinka,vrabotenilikorisnik,address)
            print('Korisnikot ' + korime + ' uspeshno se najavi na serverot \n')
        elif tip == 'Send':
            isprakjach = poraka[1]
            dokogo = poraka[2]
            text = poraka[3]
            if dokogo in korisnici: #ako korisnikot komu sakame da pratime postoi 
                #mora da proverime dali e korisnik ili vraboten i porakata pomegju bilo kogo mora da e do 48 B
                if len(text) <= MAX_CLIENT:
                    #ako e pomala od 48 se izvrshuva se
                    #proverka za korisnik -> vraboten 24
                    if korisnici[isprakjach].vrabotenilikorisnik == 'Korisnik':
                        if korisnici[dokogo].vrabotenilikorisnik == 'Vraboten':
                            if len(text) <= MAX_KORISNIK_VRABOTEN:
                                #ako e pomala okej e
                                msg = isprakjach + ": " + text + " \n"
                                s.sendto(msg.encode(), korisnici[dokogo].adresa)
                            else:
                                golemina = len(text) - MAX_KORISNIK_VRABOTEN
                                golemina = int(golemina)
                                golemina = bin(golemina)[2:]
                                msg = 'Dolzinata na porakata e pogolema od 26 Bytes. Razlikata vo bits e: ' + golemina + "\n"
                                s.sendto(msg.encode() , korisnici[isprakjach].adresa)
                        #proverka za korisnik -> korisnik 26
                        elif korisnici[isprakjach].vrabotenilikorisnik == 'Korisnik':
                            if len(text) <= MAX_KORISNIK_KORISNIK:
                                #ako e pomala e okej
                                msg = isprakjach + ": " + text + " \n"
                                s.sendto(msg.encode() , korisnici[dokogo].adresa)
                            else: 
                                golemina = len(text) - MAX_KORISNIK_KORISNIK
                                golemina = int(golemina)
                                golemina = bin(golemina)[2:]
                                msg = 'Dolzinata na porakata e pogolema od 24 Bytes. Nadminuvanjeto vo bits e: ' + golemina + "\n"
                                s.sendto(msg.encode(), korisnici[isprakjach].adresa)
                    else:
                        msg = isprakjach + ": " + text + "\n"
                        s.sendto(msg.encode() , korisnici[dokogo].adresa)
                else:
                    #ako porakata e pogolema od 48 error
                    golemina = len(text) - MAX_CLIENT
                    golemina = int(golemina)
                    golemina = bin(golemina)[2:]
                    msg = 'Dolzinata na porakata nadminuva 48 Bytes. Razlikata vo bits e: ' + golemina + " \n"
                    s.sendto(msg.encode() , korisnici[isprakjach].adresa)               
            
            else:   #korisnikot ne postoi
                msg = 'Korisnikot ne postoi ! \n'
                s.sendto(msg.encode(), korisnici[isprakjach].adresa)

elif sys.argv[1:] == ['client']:
    korime = input("Vnesi korisnichko ime: \n")
    lozinka = input("Vnesi lozinka: \n")
    vrabotenilikorisnik = input("Vnesi dali si 'Vraboten' ili pak si 'Korisnik': \n")

    s.sendto(("Connect." + korime + "." + lozinka + "." + vrabotenilikorisnik).encode(), ('127.0.0.1', PORT))

    threading.Thread(target = primiPoraka , args = (s,)).start()

    while True:
        dokogo = input("Do kogo sakate da ispratite poraka: \n")
        poraka = input("Vnesi a porakata za isprakajnje: \n")

        s.sendto(("Send." + korime + "." + dokogo + "." + poraka).encode(), ('127.0.0.1', PORT))


else:
    print(sys.stderr, 'Usage: python kol2.py client|server \n')