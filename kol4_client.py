""" 2. Да се направи социјална мрежа за потребите на една детска градинка во која работат 
воспитувачи, готвачи и административци. Програмата да биде дистрибуирана P2P клиент 
сервер апликација со употреба на TCP и RPC. Клиентот треба да се регистрира на сервер со 
единствено корисничко име, лозинка и позиција. Доколку позицијата му е воспитувач, се 
чува и дополнителна информација за тоа на која група е воспитувач, а доколку е готвач се 
чува дополнителна информација за што е специјализиран. По успешна регистрација клиентот
треба да се најави на серверот. Најавените клиенти можат да праќаат пораки до било кој од 
другите најавени клиенти. Градинката функционира така што секој административец може да
креира група со името од “дополнителната информација”, а потоа тука може да се приклучат 
готвачите и воспитувачите и да испраќаат пораки, но доколку групата им е соодветна 
(дополнителната информација се совпаѓа со името на групата). Исто така има и група во која 
членуваат сите административци (неа може да ја креира било кој административец, но само 
еднаш, а притоа групата ќе има име administracija) и тука исто така секој од 
административците кој се приклучил може да испраќа пораки. Секој вработен има можност и
да се одјави од серверот.
Доколку готвач или воспитувач се обиде да се приклучи во групата на административците 
или некој вработен се обиде да се приклучи во несоодветна група да му се даде информација 
дека не може и поради која причина.
Притоа, регистрацијата, најавата, одјавата, креирањето на група се контролна комуникација
со северот, додека праќањето на порака од клие0нт до друг клиент или група е податочна
комуникација. (60п """

import xmlrpc.client as client
import sys, struct, threading, socket

def recv_all(socket, length):
    data=''
    while len(data) < length:
        more = socket.recv(length-len(data)).decode()
        if not more:
            raise EOFError("...")
        data+=more
    return data.encode()

def chekaj(s):
    s.listen(5)
    while True:
        sv,address = s.accept()
        data = recv_all(sv, struct.unpack("!i" , recv_all(s,4))[0]).decode().split(".")
        print('\n' + data[0] + " veli: " + data[1] + "\n")
        sv.close()

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
proxy = client.ServerProxy('http://127.0.0.1:7000' , allow_none = True)

while True:
    what = int(input("Vnesi broj: \n \t 1-registracija \n \t 2-najava \n \t 3-odjava \n \t 4-kreiraj grupa \n \t 5-kreiraj grupa za lideri \n \t 6-prikluchi se na grupa \n \t 7-izlezi od grupa \n \t 8-isprati poraka na korisnik \n \t 9-isprati poraka vo grupa \n"))

    if what == 1:
        korime =input("Vnesi korisnichko ime:")
        lozinka = input("Vnesi lozinka: ")
        pozicija = input("Vnesi pozicija: 0-Vospituvach, 1-Gotvach, 2-Administrativec :")
        if pozicija==0:
            grupa = input("Vnesi grupa: ")
        elif pozicija==1:
            grupa = input("Vnesi ekspertiza ")
        else:
            grupa = 'administracija'
        print(proxy.registracija(korime,lozinka,pozicija,grupa))
    if what == 2:
        korime = input("Vnesi korime")
        lozinka = input("Vnesi lozinka")
        s.bind(('0.0.0.0', 0))
        print("Client is listening at " , s.getsockname())
        print(proxy.najava(korime,lozinka, s.getsockname()[0] , str(s.getsockname()[1])))
        threading.Thread(target = chekaj, args=(s,)).start()
    if what == 3 and korime:
        print(proxy.odjava(korime))
    if what == 4 and korime:
        ime = input("Vnesi ime na grupa")
        print(proxy.kreiraj_grupa(korime,ime))
    if what == 5 and korime:
        print(proxy.kreiraj_grupa_administracija(korime))
    if what == 6 and korime:
        ime = input("Vnesi ime na grupa ")
        print(proxy.prikluchi_grupa(korime,ime))
    if what == 7 and korime:
        ime = input("Vnesi ime na grupa ")
        print(proxy.napushti_grupa(korime,ime))



    if what == 8 and korime:    #(sender,recepient)
        recepient = input("Vnesi recepient")
        poraka = input("Vnesi poraka ")
        if proxy.isprati_do_korisnik(korime,recepient) != "The recepient has not registered or logged in yet" and proxy.isprati_do_korisnik(korime,recepient) != "You have not registered or logged in yet":
            adresa, porta = proxy.isprati_do_korisnik(korime,recepient)
            sv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sv.connect((adresa, int(porta)))
            poraka_full = korime + "." + poraka
            sv.sendall(struct.pack("!i" , len(poraka_full)) + poraka_full.encode())
            sv.close()
        else:
            print(proxy.isprati_do_korisnik(korime,recepient))



    if what == 9 and korime:    #(sender,ime)
        ime = input("Vnesi ime na grupa")
        poraka = input("Vnesi poraka ")
        if proxy.isprati_do_grupa(korime,ime) != "You are not member of the group" and proxy.isprati_do_grupa(korime,ime) != "The group does not exist" and proxy.isprati_do_grupa(korime,ime) != "You are not registered or logged in" :
            korisnici = dict(proxy.isprati_do_grupa(korime,ime))

            for korisnik in korisnici:
                sv = socket.socket(socket.AF_INET , socket.SOCK_STREAM)
                socket_info = korisnici[korisnik].split(".")
                sv.connect((socket_info[0] , int(socket_info[1])))
                poraka_full = korime + "." + poraka
                sv.sendall(struct.pack("!i" , len(poraka_full)) + poraka_full.encode())
                sv.close()
        else:
            print(proxy.isprati_do_grupa(korime,ime))


