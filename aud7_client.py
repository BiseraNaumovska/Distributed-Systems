""" Да се напише дистрибуирана P2P клиент сервер апликација со употреба на TCP и RPC.
Клиентот треба да се регистрира на серверот со единствено корисничко име и лозинка. По
успешна регистрација клиентот треба да се најави на серверот. Најавените клиенти можат
да праќаат пораки до други најавени клиенти. Секој најавен клиент може да креира група
со одредено име ако таа група не постои, да се приклучи на одредена група ако веќе не е
член и да испраќа пораки до групата во која што е член. Клиентот треба да има можност и
да се одјави од серверот. Притоа, регистрацијата, најавата, одјавата, креирањето на група се
контролна комуникација со северот, додека праќањето на порака од клиент до друг клиент
или група е податочна комуникација.
 """

#!/usr/bin/env python
import sys, socket,struct, threading
import xmlrpc.client as client

def recv_all(sock,length):
    data=''
    while len(data) < length:
        more = sock.recv(length - len(data)).decode()
        if not more:
            raise EOFError('...error...')
        data+=more
    return data.encode()

def chekaj(s):
    s.listen(2)
    while True:
        cs,address = s.accept()
        length = struct.unpack("!i" , recv_all(cs,4))[0]
        data = data.decode().split(".")
        print("\n" + data[0] + " veli: " + data[1] + "\n")
        cs.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

proxy = client.ServerProxy('http://127.0.0.1:7001' , allow_none=True)

try:
    while True:
        what = input(" \t r-registracija  \n\t n-najava \n\t o-odjava \n\t k-kreiraj grupa \n\t pp-prikluchi grupa \n\t nn-napushti grupa \n\tik-isprati do korisnik \n\t ig-isprati do grupa \n Your choice is:")

        if what == 'r':
            korime = input("Input username: ")
            lozinka = input("Input password: ")
            print(proxy.registracija(korime,lozinka))
        if what == 'n':
            korime = input("Input username: ")
            lozinka = input("Input password: ")
            s.bind(('0.0.0.0' , 0))
            print(s.getsockname())
            threading.Thread(target = chekaj , args=(s,)).start()
            print(proxy.najava(korime,lozinka.s.getsockname()[0] , str(s.getsockname()[1])))
        if what == 'o' and korime:
            print(proxy.odjava(korime))
        if what == 'k':
            ime = input("Insert group name: ")
            print(proxy.kreiraj_grupa(ime))
        if what == 'pp':
            ime = input("Insert group name: ")
            print(proxy.priklushi_gruoa(ime, korime, s.getsockname()[0] , str(s.getsockname()[1])))
        if what == 'nn':
            ime = input("Insert group name: ")
            print(proxy.napushti_grupa(ime, korime))



            #sledniot del e P2P komunikacija
        if what == 'ik':
            #isprati do korisnik
            korime_p = input("Which user? ")
            poraka = input("What message? ")
            if proxy.isprati_do_korisnik(korime_p,korime) != 'You are not logged in' and proxy.isprati_do_korisnik(korime_p,korime) != 'Not logged in':
                adresa, porta = proxy.isprati_do_korisnik(korime_p, korime)
                sv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sv.connect(('adresa', int(porta)))
                poraka_full = korime + "." + poraka
                sv.sendall(struct.pack("!i" , len(poraka_full)) + poraka_full.encode())
                sv.close()
            else:
                print(proxy.isprati_do_korisnik(korime_p,korime))


        if what == 'ig':
            #isprati do grupa
            ime = input("Which group? ")
            poraka = input("What message? ")
            if proxy.isprati_do_grupa(ime,korime) != "Group does not exist" and proxy.isprati_do_grupa(ime,korime) != "Join group first":
                korisnici = proxy.isprati_do_grupa(ime, korime)
                poraka_full = korime + "." + poraka
                for k in korisnici:
                    sv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    socket_info = korisnici[k].split(".")
                    sv.connect((socket_info[0] , int(socket_info[1])))
                    sv.sendall(struct.pack("!i" , len(poraka_full)) + poraka_full.encode())
                    sv.close()
            else:
                print(proxy.isprati_do_grupa(ime,korime))
except:
    print("Greshka \n")