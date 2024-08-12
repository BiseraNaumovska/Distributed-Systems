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

from xmlrpc.server import SimpleXMLRPCServer
import socket,struct,sys,threading

class Korisnik():
    def __init__(self,korime,lozinka,adresa=0,porta=0,najaven=0):
        self.korime,self.lozinka,self.adresa,self.porta,self.najaven = korime,lozinka,adresa,porta,najaven

class grupa():
    def __init__(self,ime):
        self.ime = ime
        self.korisnici = {}

korisnici = {}
grupi = {}

def Registracija(korime,lozinka):
    if korime in korisnici:
        return 'Username already taken'
    else:
        korisnici[korime] = Korisnik(korime,lozinka)
        return "Registration successful"

def Najava(korime,lozinka,interface,port):
    if korime in korisnici and korisnici[korime].lozinka == lozinka:
        korisnici[korime].najaven = 1
        korisnici[korime].adresa = interface
        korisnici[korime].port = port
        return "Login successful"
    else:
        return "Wrong username or password"

def Odjava(korime):
    if korime in korisnici:
        del korisnici[korime]
        for grupa in grupi:
            if korime in grupi[grupa].korisnici:
                del grupi[grupa].korisnici[korime]
        return "Successful logout"
    else:
        return "User not logged in"
    
def KreirajGrupa(ime):
    if ime in grupi:
        return "Group name already taken"
    else:
        grupi[ime] = grupa(ime)
        return "Empty group created"
    
def PrikluchiGrupa(ime,korime,interface,port):
    if ime in grupi:
        if korime in grupi[ime].korisnici:
            return "Already in group"
        else:
            grupi[ime].korisnici[korime] = str(interface + "." + port)
            return "You were added to the group"

def NapushtiGrupa(ime, korime):
    if ime in grupi:
        try:
            del grupi[ime].korisnici[korime]
            return "Seccussfully removed from the group"
        except KeyError:
            return "User not in the group"

def IspratiDoKorisnik(korimep, korime):
    print(korimep)
    if korime not in korisnici or korisnici[korime].najaven == 0:
        return "You are not logged in"
    if korimep in korisnici and korisnici[korimep].najaven:     #TCP komunikacija za koga e najaven
        return korisnici[korime].adresa, korisnici[korimep].porta
    else:
        return "Not logged in"
        
def IspratiDoGrupa(ime, korime):
    if ime not in grupi:
        return 'Group does not exist'
    if korime in grupi[ime].korisnici and korisnici[korime].najaven:
        return grupi[ime].korisnici
    else:
        return "Join group first"
    
server = SimpleXMLRPCServer(('127.0.0.1', 7001))
server.register_introspection_functions()
server.register_multicall_functions()

server.register_functions(Registracija)
server.register_functions(Najava)
server.register_functions(Odjava)
server.register_functions(KreirajGrupa)
server.register_functions(PrikluchiGrupa)
server.register_functions(NapushtiGrupa)
server.register_functions(IspratiDoKorisnik)
server.register_functions(IspratiDoGrupa)

print("Server ready")
server.serve_forever()