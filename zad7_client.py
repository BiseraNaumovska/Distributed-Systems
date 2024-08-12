""" Да се напише дистрибуирана P2P клиент сервер апликација со употреба на TCP и RPC.
Клиентот треба да се регистрира на серверот со единствено корисничко име и лозинка. По
успешна регистрација клиентот треба да се најави на серверот. Најавените клиенти можат
да праќаат пораки до други најавени клиенти. Секој најавен клиент може да креира група
со одредено име ако таа група не постои, да се приклучи на одредена група ако веќе не е
член и да испраќа пораки до групата во која што е член. Клиентот треба да има можност и
да се одјави од серверот. Притоа, регистрацијата, најавата, одјавата, креирањето на група се
контролна комуникација со северот, додека праќањето на порака од клиент до друг клиент
или група е податочна комуникација. """

#!/usr/bin/env python

import xmlrpc.client as client
import sys, struct, socket, threading

def recv_all(sock, length):
    data=''
    while len(data) < length:
        more = sock.recv(length - len(data)).decode()
        if not more:
            raise EOFError("...")
        data += more
    return data.encode()

s = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET , socket.SO_REUSEADDR , 1)

proxy = client.ServerProxy('http://127.0.0.1:7001', allow_none=True)

def chekaj(s):
    s.listen(2)
    while True:
        cs, address = s.accept()
        length = struct.unpack("!i", recv_all(cs,4))[0]
        data = recv_all(cs, length)
        data = data.decode().split(".")
        print("\n" + data[0] + " veli: " + data[1] + " \n")
        cs.close()  #za da moze drug klient da se opsluzi
try:
    while True:
        what = input('What is next? \n \t r-registracija \n \t n-najava \n \t o-odjava \n \t k-kreiraj grupa \n \t pp-prikluchi grupa \n \t nn-napushti grupa \n \t ik-isprati do korisnik \n \t ig-ispratidogrupa \n Your choice:')
        if what == 'r':
            korime = input("Vnesi ime: ")
            lozinka = input("Vnesi lozinka: ")
            print(proxy.Registracija(korime,lozinka))
             
        if what == 'n':
            korime = input("Vnesi username: ")
            lozinka = input("Vnesi lozinka: ")
            s.bind(('0.0.0.0', 0))
            print(s.getsockname())
            threading.Thread(target = chekaj , args = (s,)).start()
            print(proxy.Najava(korime,lozinka,s.getsockname()[0],str(s.getsockname()[1])))

        if what == 'k':
            ime = input("Vnesi ime: ")
            print(proxy.KreirajGrupa(ime))

        if what == 'pp':
            ime = input("Vnesi ime na grupata: ")
            print(proxy.PrikluchiGrupa(ime,korime,s.getsockname()[0] , str(s.getsockname()[0])))

        if what == 'nn':
            ime = input("Vnesi ime na grupa: ")
            print(proxy.NapushtiGrupa(ime,korime))

        if what == 'ik':
            korime_p=input("Koj korisnik: ")
            poraka = input("What message? ")
            if proxy.IspratiDoKorisnik(korime_p,korime) != "Not logged in" and proxy.IspratiDoKorisnik(korime_p,korime) != "You are not logged in":
                adresa,porta = proxy.IspratiDoKorisnik(korime_p, korime)
                sv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sv.connect((adresa, int(porta)))
                poraka_full = korime + "." + poraka
                sv.sendall(struct.pack("!i", len(poraka_full)) + poraka_full.encode())
                sv.close()
            else:
                print(proxy.IspratiDoKorisnik(korime_p, korime))

        if what == 'ig':
            ime = input("Koja grupa? ")
            poraka = input("What message? ")
            if proxy.IspratiDoGrupa(ime,korime) != "Group does not exist" and proxy.IspratiDoGrupa(ime,korime) != "Join group first: ":
                korisnici = proxy.ispratiDoGrupa(ime,korime)
                poraka_full = korime + "." + poraka
                for k in korisnici:
                    sv = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
                    socket_info = korisnici[k].split(".")
                    sv.connect((socket_info[0], int(socket_info[1])))
                    sv.sendall(struct.pack("!i",len(poraka_full)) + poraka_full.encode())
                    sv.close()
            else:
                print(proxy.IspratiDoGrupa(ime,korime))
                
        if what == 'o' and korime:
            print(proxy.odjava(korime))

except:
    print("Greshka \n")






