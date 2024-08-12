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

#!/usr/bin/env python

from xmlrpc.server import SimpleXMLRPCServer
import sys, threading, struct, socket

class Korisnik():
    def __init__(self, korime, lozinka, pozicija, sektor, adresa=0, porta=0, najaven=0):
        self.korime, self.lozinka,self.pozicija,self.sektor,self.adresa,self.porta,self.najaven = korime,lozinka,pozicija,sektor,adresa,porta,najaven

class Grupa():
    def __init__(self, ime):
        self.ime = ime
        self.korisnici = {}

korisnici = {}
grupi = {}

def registracija(korime, lozinka,pozicija, sektor):
    if korime not in korisnici:
        korisnici[korime] = Korisnik(korime,lozinka,pozicija,sektor)
        return "You have successfully registered on the server"
    else:
        return "This user already exist, please try again!"
    
def najava(korime, lozinka,adresa,porta):
    if korime in korisnici and korisnici[korime].lozinka == lozinka:
        korisnici[korime].adresa = adresa
        korisnici[korime].porta = porta
        korisnici[korime].najaven = 1
        return "You have successfully logged in on the server"
    else:
        return "Invalid user credentials, please try again!"
    
def odjava(korime):
    if korime in korisnici:
        del korisnici[korime]
        for group in grupi:
            if korime in grupi[group].korisnici:
                del grupi[group].korisnici[korime]
        return "You have successfully logged out"
    else:
        return "Username doesn't exist, please try again!"
    
def kreiraj_grupa(korime):
    #samo rakovoditelot smee da kreira grupa so imeto kako na svojot sektor
    if korime in korisnici:
        if korisnici[korime].pozicija == '2':
            if korisnici[korime].sektor not in grupi:
                grupi[korisnici[korime].sektor] = Grupa(korisnici[korime].sektor)
                return "The group has successfully been created"
            else:
                return "This group already exists, please try again!"
        else:
            return "You must have a lead position in the company to create groups"
    else:
        return "Username doesn't exist, please try again!"
    
def kreiraj_grupa_rakovoditeli(korime):
    if korime in korisnici:
        if korisnici[korime].pozicija == '2':
            if 'rakovoditeli' not in grupi:
                grupi['rakovoditeli'] = Grupa('rakovoditeli')
                return "Leaders group successfully created"
            else:
                return "This group already exists, feel free to join in"
        else:
            return "You must have a lead position in the company to create this group"
    else:
        return "Username doesn't exist, please try again!"
    
def prikluchi_grupa(korime, ime):
    if korime not in korisnici:
        return "Username doesn't exist, please try again!"
    elif korisnici[korime].pozicija < 2 and korisnici[korime].sektor != ime:
        return "You are only allowed to join the group of your sector, please try again!"
    elif korisnici[korime].pozicija == 2 and korisnici[korime].sektor != ime and ime != "rakovoditeli":
        return "You are only allowed to join the group of your sector, or the leaders group, please try again!"
    
    if ime in grupi:
        if korime not in grupi[ime].korisnici:
            grupi[ime].korisnici[korime] = str(korisnici[korime].adresa + "." + korisnici[korime].porta)
            return "You have successfully joined this group"
        else:
            return "You are already a part of this group, please try again!"
    else:
        return "Group doesn't exist, please try again!"
    
def napushti_grupa(korime, ime):
    if korime not in korisnici:
        return "Username doesn't exist, please try again!"
    if ime in grupi:
        if korime in grupi[ime].korisnici:
            del grupi[ime].korisnici[korime]
            return "You have successfully left the group"
        else:
            return "You are not a part of this group, please try again!"
    else:
        return "Group doesn't exist, please try again!"
    
def isprati_do_korisnik(sender, recepient):
    if sender in korisnici and korisnici[sender].najaven == 1:
        if recepient in korisnici and korisnici[recepient] == 1:
            return korisnici[recepient].adresa, korisnici[recepient].porta
        else:
            return "The recepient is not logged in, please try again!"
    else:
        return "You are not logged in, please try again!"

def isprati_do_grupa(korime, ime):
    if ime in grupi:
        if korime in grupi[ime].korisnici and korisnici[korime].najaven == 1:
            return grupi[ime].korisnici
        else:
            return "You are not a part of this group, please try again!"
    else:
        return "Group doesn't exist, please try again!"
    

server = SimpleXMLRPCServer(('127.0.0.1', 7001))
server.register_introspection_functions()
server.register_multicall_functions()

server.register_function(registracija)
server.register_function(najava)
server.register_function(odjava)
server.register_function(kreiraj_grupa)
server.register_function(kreiraj_grupa_rakovoditeli)
server.register_function(prikluchi_grupa)
server.register_function(napushti_grupa)
server.register_function(isprati_do_korisnik)
server.register_function(isprati_do_grupa)

print("Server ready \n")
server.serve_forever()


