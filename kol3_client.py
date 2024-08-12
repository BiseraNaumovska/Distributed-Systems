""" 3. Да се направи социјална мрежа за потребите на една државна институција во која работат 
помлади соработници, соработници и раководители. Програмата да биде дистрибуирана P2P 
клиент сервер апликација со употреба на TCP и RPC. Клиентот треба да се регистрира на 
сервер со единствено корисничко име, лозинка, позиција и сектор под кој работи во 
институцијата. По успешна регистрација клиентот треба да се најави на серверот. Најавените
клиенти можат да праќаат пораки до било кој од другите најавени клиенти. Институцијата 
функционира така што секој раководител може да креира група со името на својот сектор, а 
потоа тука може да се приклучат помладите соработници и соработниците и да испраќаат 
пораки. Исто така има и група во која членуваат сите раководители (неа може да ја креира 
било кој раководител, но само еднаш, а притоа групата ќе има име rakovoditeli) и тука исто 
така секој од раководителите кој се приклучил може да испраќа пораки. Секој вработен има 
можност и да се одјави од серверот.
Доколку помлад соработник или соработник се обиде да се приклучи во групата на 
раководителите или некој вработен се обиде да се приклучи во група од друг сектор да му се 
даде информација дека не може и поради која причина.
Притоа, регистрацијата, најавата, одјавата, креирањето на група се контролна комуникација
со северот, додека праќањето на порака од клиент до друг клиент или група е податочна
комуникација. (35п """

import socket,sys,struct,threading
import xmlrpc.client as client

def recv_all(socket, lenght):
    data = ''
    while len(data) < lenght:
        more = socket.recv(lenght - len(data)).decode()
        if not more:
            raise EOFError("...")
        data+=more
    return data.encode()

def chekaj(s):
    s.listen(5)
    while True:
        cs,address = s.accept()
        data = recv_all(cs , struct.unpack("!i" , recv_all(cs,4))[0]).decode().split('.')
        print(data[0] + " veli: " + data[1] + "\n")
        cs.close()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

proxy = client.ServerProxy('http://127.0.0.1:7001', allow_none=True)

while True:
    what = int(input("Vnesi broj: \n \t 1-registracija \n \t 2-najava \n \t 3-odjava \n \t 4-kreiraj grupa \n \t 5-kreiraj grupa za lideri \n \t 6-prikluchi se na grupa \n \t 7-izlezi od grupa \n \t 8-isprati poraka na korisnik \n \t 9-isprati poraka vo grupa \n"))

    if what == 1:
        korime = input("Vnesi username: ")
        lozinka = input("Vnesi lozinka: ")
        pozicija = int(input("Vnesi pozicija: 0-Junior, 1-Senior, 2-Lead"))
        sektor = input("Vnesi sektor: ")
        print(proxy.registracija(korime,lozinka,pozicija,sektor))
    if what == 2:
        korime = input("Vnesi username: ")
        lozinka = input("Vnesi lozinka: ")
        s.bind(('0.0.0.0', 0))
        print("Client is listening at: ", s.getsockname())
        threading.Thread(target=chekaj , args=(s,)).start()
        print(proxy.najava(korime,lozinka, s.getsockname()[0] , str(s.getsockname()[1])))
    if what == 3 and korime:
        print(proxy.odjava(korime))
    if what == 4 and korime:
        print(proxy.kreiraj_grupa(korime))
    if what == 5 and korime:
        print(proxy.kreiraj_grupa_rakovoditeli(korime))
    if what == 6 and korime:
        sektor = input("Vnesi go imeto na grupata vo koja sakash da chlenuvash \n")
        print(proxy.prikluchi_grupa(korime,sektor))
    if what == 7 and korime:
        sektor = input("Vnesi go imeto na grupata od koja sakash da izlezesh \n")
        print(proxy.napushti_grupa(korime,sektor))
    if what == 8 and korime:
        recepient = input("Vnesi go imeto na recepient \n")
        poraka = input("Vnesi poraka za recepient: \n")
        if proxy.isprati_do_korisnik(korime, recepient) != 'The recepient is not logged in, please try again!' and proxy.isprati_do_korisnik(korime,recepient) != "You are not logged in, please try again!":
            adresa,porta = proxy.isprati_do_korisnik(korime,recepient)
            sv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sv.connect((adresa, int(porta)))
            poraka_full = korime + "." + poraka
            sv.sendall(struct.pack("!i", len(poraka_full)) + poraka_full.encode())
            sv.close()
        else:
            print(proxy.isprati_do_korisnik(korime,recepient))
            

    if what == 9 and korime:
        sektor = input("Vnesi ime na grupa do koja sakash da ispratish poraka \n")
        poraka = input("Vnesi poraka: \n")
        if proxy.isprati_do_grupa(korime,sektor) != 'You are not a part of this group, please try again!' and proxy.isprati_do_grupa(korime, sektor) != "Group doesn't exist, please try again!":
            korisnici = dict(proxy.isprati_do_grupa(korime,sektor))
            for k in korisnici:
                sv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket_info = korisnici[k].split(".")
                poraka_full = str(korime) + "." + poraka 
                sv.connect((socket_info[0] , int(socket_info[1])))
                sv.sendall(struct.pack("!i" , len(poraka_full)) + poraka_full.encode())
                sv.close()
        else:
            print(proxy.isprati_do_grupa(korime,sektor))
            



 