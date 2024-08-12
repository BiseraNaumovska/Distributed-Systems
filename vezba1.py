""" . Да се напише програма која симулира UDP комуникација во која клиентите праќаат порака
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
import sys,socket,threading, struct

class Korisnik():
    def __init__(self ,korime,lozinka,vrabotenilikorisnik,adresa):
        self.korime, self.lozinka, self.vrabotenilikorisnik, self.adresa = korime,lozinka,vrabotenilikorisnik,adresa

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

MAX= 65535
PORT = 1060
MAX_KLIENT = 48
MAX_K_V = 24
MAX_K_K = 26

def chitaj(s):
    while True:
        data,address = s.recvfrom(MAX)
        print(data.decode())


if sys.argv[1:] == ['server']:
    korisnici = {}
    s.bind(('127.0.0.1' , PORT))
    print("SErverot slusha na " , s.getsockname())

    while True:
        data,address = s.recvfrom(MAX)
        poraka = data.decode().split(".")
        tip = poraka[0]
        if tip == 'Connect':
            korime = poraka[1]
            lozinka = poraka[2]
            vrabotenilikorisnik = poraka[3]
            korisnici[korime] = Korisnik(korime,lozinka,vrabotenilikorisnik,address)
        elif tip == 'Send':
            korime = poraka[1]
            dokogo = poraka[2]
            text = poraka[3]
            if dokogo in korisnici:
                if len(text) <= MAX_CLIENT:
                    if korisni....
        msg = korime + ": " + text + "\n"
        s.sendto(msg.encode() , korisnici[dokogo].adresa)


elif sys.argv[1:] == ['client']:
    korime = input("Korime:")
    lozinka = input("Lozinka")
    vrabotenilikorisnik = input("vraboten ili korisnik")
    s.sendto(('Connect.' + korime + "." + lozinka + "." + vrabotenilikorisnik).encode() , ('127.0.0.1' , PORT))

    threading.Thread(target = chitaj , args = (s,)).start()

    dokogo = input("Do kogo ")
    poraka = input ("Poraka")
    s.sendto(('Send.' + korime + "." + dokogo + "." + poraka).encode() , ('127.0.0.1', PORT))

else:
    print(sys.stderr, "Usage: python vezba.py client|server")