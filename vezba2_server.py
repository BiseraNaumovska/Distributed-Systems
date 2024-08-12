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
комуникација. (60п) """

import sys, socket, struct, threading
from xmlrpc.server import SimpleXMLRPCServer

class Korisnik():
    def __init__ (self, korime, lozinka, pozicija, grupa, adresa=0, porta=0 , najaven=0):
        self.korime, self.lozinka, self.pozicija, self.grupa, self.adresa, self.porta, self.najaven = korime,lozinka,pozicija,grupa,adresa,porta,najaven

class Grupa():
    def __init__(self, ime):
        self.ime = ime
        self.korisnici = {}

korisnici = {}
grupi = {}

def registracija(korime, lozinka, pozicija, grupa):
    if korime not in korisnici:
        korisnici[korime] = Korisnik(korime,lozinka,pozicija,grupa)
        return "Successful registration \n"
    else:
        return "Username already exists \n"
def najava(korime,lozinka,adresa,porta):
    if korime in korisnici and korisnici[korime].lozinka == lozinka:
        korisnici[korime].adresa = adresa
        korisnici[korime].porta = porta
        korisnici[korime].najaven = '1'
        return "Successful log in \n"
    else:
        return "Wrong credentials \n"
def odjava(korime):
    if korime in korisnici:
        del korisnici[korime]
        for g in grupi:
            if korime in grupi[g].korisnici:
                del grupi[g].korisnici[korime]
        return "Logged out from the group \n"
    else:
        return "Wrong username \n"
def kreiraj_grupa(korime, ime):
    if korime in korisnici:
        if korisnici[korime].pozicija == 'administrativec':
            if ime not in grupi:
                grupi[ime] = Grupa(ime)
                return "Group created \n"
            else:
                return "Group already existed \n"
        else:
            return "You have no permission \n"
    else:
        return "Wrong username \n"
def kreiraj_grupa_administracija(korime):
    if korime in korisnici:
        if korisnici[korime].pozicija == 'administrativec':
            g_name = 'administracija'
            if g_name not in grupi:
                grupi[g_name] = Grupa(g_name)
                return "Group 'administracija' created \n"
            else:
                return "Group 'administracija' already exists \n"
        else:
            return "You have no permission to create the group 'administracija' \n"
    else:
        return "Wrong username \n"
def prikluchi_grupa(korime, ime):
    if korime in korisnici:
        if ime == korisnici[korime].grupa:
            if ime in grupi:
                if korime not in grupi[ime].korisnici:
                    grupi[ime].korisnici[korime] = str(korisnici[korime].adresa + "." + korisnici[korime].porta)
                    return "You joined the group \n"
                else:
                    return "You are already a member of the group \n"
            else:
                # kreiraj_grupa(korime,ime)
                return "The group does not exist \n"
        else:
            return "You have no permission to join the group \n"
    else:
        return "Wrong username \n"
def napushti_grupa(korime, ime):
    if korime in korisnici:
        if ime in grupi:
            if korime in grupi[ime].korisnici:
                del grupi[ime].korisnici[korime]
                return "You left the group \n"
            else:
                return "You are not a member of the group \n"
        else:
            return "The group does not exist \n"
    else:
        return "Wrong username \n"

def isprati_do_korisnik(sender, recepient):
    if sender in korisnici and korisnici[sender].najaven == '1':
        if recepient in korisnici and korisnici[recepient].najaven == '1':
            return korisnici[recepient].adresa , korisnici[recepient].porta
        else:
            return "Recepient not logged in \n"
    else:
        return "First log in \n"

def isprati_do_grupa(sender , ime_g):
    if sender in korisnici and korisnici[sender].grupa == ime_g and korisnici[sender].najaven == '1':
        if ime_g in grupi:
            if sender in grupi[ime_g].korisnici:
                return grupi[ime_g].korisnici
            else:
                # prikluchi_grupa(sender, ime_g)
                return "You are not member of the group \n"
        else:
            return "The group does not exist \n"
    else:
        return "You have no permision or you are not logged in \n"
    

server = SimpleXMLRPCServer(('127.0.0.1' , 7000))
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

print("Server is ready \n")
server.serve_forever()


