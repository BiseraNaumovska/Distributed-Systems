""" 1. Да се напише програма која симулира UDP комуникација во која клиентите праќаат порака
до серверот со која се регистрираат со корисничко име, лозинка и дали е студент или 
професор. Откако ќе се регистрираат, клиентите можат да праќаат пораки до друг клиент. 
Доколку се испраќа порака до професор може да биде до 16B, доколку пак се испраќа до 
студент може да биде и до 26B, без разлика кој ја испраќа пораката. Пораката да не може да 
се прати до клиентот ако е поголема од соодветната дозволена граница и тогаш серверот да 
одговори дека порака е преголема и да врати за колку бајти е надмината границата, а тоа 
клиентот да го испечати. Истовремено при праќање на порака, клиентите може да примаат 
пораки од страна на други клиенти. Препраќањето на пораките го врши серверот. (30п)
 """

import sys, socket, threading

class Korisnik():
    def __init__(self, korime,lozinka, studentiliprofesor, adresa):
        self.korime, self.lozinka, self.studentiliprofesor, self.adresa = korime,lozinka, studentiliprofesor,adresa

s = socket.socket(socket.AF_INET , socket.SOCK_DGRAM)

MAX = 65535
PORT = 1060
MAX_PROFFESORS = 16
MAX_STUDENTS = 26

def primiPoraka(s):
    while True:
        data,address = s.recvfrom(MAX)
        print(data.decode())

if sys.argv[1:] == ['server']:
    korisnici = {} #prazna lista na korisnici
    #koga sme kaj serverot toj mora prvo da se otvori za da slusha
    s.bind(('127.0.0.1' , PORT))
    print('Server listening at...' , s.getsockname())

    while True:
        data, address = s.recvfrom(MAX)
        poraka = data.decode().split(".")
        tip = poraka[0]
        if tip == 'Connect':
            korime = poraka[1]
            lozinka = poraka[2]
            studentiliprofesor = poraka[3]

            korisnici[korime] = Korisnik(korime, lozinka, studentiliprofesor, address)
            print("Korisnikot " + korime + " uspeshno se registrirashe \n")
        elif tip == 'Send':
            korime = poraka[1]
            dokogo = poraka[2]
            text = poraka[3]

            if dokogo in korisnici:
                if korisnici[dokogo].studentiliprofesor == 'Student':
                    if len(text) <= MAX_STUDENTS:
                        #ako imame soodvetna dolzina, da moze da se isprati
                        msg = korime + ': ' + text
                        s.sendto(msg.encode(), korisnici[dokogo].adresa)
                    else: #ako nemame soodvetna dolzina
                        msg = 'Dolzinata na porakata e pregolema. Nadminuvate golemina za: ' + str(len(text) - MAX_STUDENTS) + ' bajti \n'
                        s.sendto(msg.encode(), korisnici[korime].adresa)
                elif korisnici[dokogo].studentiliprofesor == 'Profesor':
                    if len(text) <= MAX_PROFFESORS:
                        #ako ima soodvetna dolzina
                        msg = korime + ": " + text
                        s.sendto(msg.encode(), korisnici[dokogo].adresa)
                    else:   #ako nema soodvetna dolzina
                        msg = 'Dolzinata na porakata e pregolema. Nadminuvate golemina za: ' + str(len(text) - MAX_PROFFESORS) + ' bajti \n'
                        s.sendto(msg.encode(), korisnici[korime].adresa)
                else:
                    print(sys.stderr, 'Treba da vnesesh Student ili Profesor')
            else:
                msg = 'Korisnikot ne se ushte ne se najavil na serverot \n'
                s.sendto(msg.encode(), korisnici[korime].adresa)
                
elif sys.argv[1:] == ['client']:
    korime = input("Vnesi korisnichko ime: \n")
    lozinka = input("Vnesi lozinka: \n")
    studentiliprofesor = input("Vnesi 'Student' ili 'Profesor' \n")

    s.sendto(("Connect." + korime + "." + lozinka + "." + studentiliprofesor).encode(), ('127.0.0.1', PORT))

    threading.Thread(target = primiPoraka, args = (s,)).start()
    
    while True:
        dokogo = input('Do kogo sakate da ispratite poraka: \n')
        poraka = input('Vnesete ja porakata za isprakjanje: \n')

        s.sendto(('Send.'+ korime + "." + dokogo + "." + poraka).encode(), ('127.0.0.1', PORT))
else:
    print(sys.stderr , "Usage: python zad.py client|server")

