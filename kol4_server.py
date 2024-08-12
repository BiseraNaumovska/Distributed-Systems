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
со северот, додека праќањето на порака од клиент до друг клиент или група е податочна
комуникација. (60п) """

from xmlrpc.server import SimpleXMLRPCServer
import sys, socket, struct, threading

class Korisnik():
    def __init__(self, korime, lozinka, pozicija, grupa, adresa=0, porta=0,najaven=0):
        self.korime, self.lozinka, self.pozicija, self.grupa, self.adresa, self.porta, self.najaven = korime,lozinka,pozicija,grupa,adresa,porta,najaven

class Grupa():
    def __init__(self,ime):
        self.ime = ime
        self.korisnici = {}

korisnici = {}
grupi = {}

def registracija(korime, lozinka, pozicija, grupa):
    if korime not in korisnici:
        korisnici[korime] = Korisnik(korime,lozinka,pozicija,grupa)
        return "You have successfully registered on the server"
    else:
        return "Username already exists"
    
def najava(korime, lozinka, adresa, porta):
    if korime in korisnici and korisnici[korime].lozinka == lozinka:
        korisnici[korime].adresa = adresa
        korisnici[korime].porta = porta
        korisnici[korime].najaven = 1
        return "You have successfully logged into the server"
    else:
        return "Invalid user credentials"
    
def odjava(korime):
    if korime in korisnici:
        del korisnici[korime]
        for group in grupi:
            if korime in grupi[group].korisnici:
                del grupi[group].korisnici[korime]
        return "You have successfully logged out of the server"
    else:
        return "Username doesn't exist"

def kreiraj_grupa(korime, ime):
    if korime in korisnici:
        if korisnici[korime].pozicija == 2:
            if ime not in grupi:
                grupi[ime] = Grupa(ime)
                return "The group has been successfully created"
            else:
                return "This group already exists"
        else:
            return "You do not have permision to create a group chat"
    else:
        return "Username does not exist"
    
def kreiraj_grupa_administracija(korime):
    if korime in korisnici:
        if korisnici[korime].pozicija == 2:
            ime_na_grupa = 'administracija'
            if ime_na_grupa not in grupi:
                grupi[ime_na_grupa] = Grupa(ime_na_grupa)
                return "The group has been created"
            else:
                return "This group already exists"
        else:
            return "You do not have permision to create this group"
    else:
        return "Username does not exist"
    
def prikluchi_grupa(korime, ime):
    if korime in korisnici:
        if ime == korisnici[korime].grupa:
            if ime in grupi:
                if korime not in grupi[ime].korisnici:
                    grupi[ime].korisnici[korime] = str(korisnici[korime].adresa + "." + korisnici[korime].porta)
                    return "You have successfully joined the group"
                else:
                    return "You are already a member of the group"
            else:
                return "The group does not exist"
        else:
            return "You can only join a group with the same name as your group"
    else:
        return "Username does not exist"
    

def napushti_grupa(korime, ime):
    if korime in korisnici:
        if ime in grupi:
            if korime in grupi[ime].korisnici:
                del grupi[ime].korisnici[korime]
                return "You left the group"
            else:
                return "You are not member of the group"
        else:
            return "The group does not exist"
    else:
        return "Username does not exist"

def isprati_do_korisnik(sender, recepient):
    if sender in korisnici and korisnici[sender].najaven == 1:
        if recepient in korisnici and korisnici[recepient].najaven == 1:
            return korisnici[recepient].adresa, korisnici[recepient].porta
        else:
            return "The recepient has not registered or logged in yet"
    else:
        return "You have not registered or logged in yet"
    
def isprati_do_grupa(sender, ime):
    if sender in korisnici and korisnici[sender].najaven == 1:
        if ime in grupi:
            if sender in grupi[ime].korisnici:
                return grupi[ime].korisnici #sakam da gi vratam site korisnici
            else:
                return "You are not member of the group"
        else:
            return "The group does not exist"
    else:
        return "You are not registered or logged in"


server = SimpleXMLRPCServer(('127.0.0.1', 7000))
server.register_introspection_functions()
server.register_multicall_functions()

server.register_function(registracija)
server.register_function(najava)
server.register_function(odjava)
server.register_function(kreiraj_grupa)
server.register_function(kreiraj_grupa_administracija)
server.register_function(prikluchi_grupa)
server.register_function(napushti_grupa)
server.register_function(isprati_do_korisnik)
server.register_function(isprati_do_grupa)

print("Server ready")
server.serve_forever()

                




