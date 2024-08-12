'''
1. Да се напише скрипта за чување на податоци за корисници на една апликација (име, презиме, 
корисничко име, лозинка). 
За секој корисник се чува и листа од разговори кои ги направил со други корисници. 
Разговорите се чуваат во речник каде клуч е корисничкото име на корисникот со кој се прави 
разговорот. 
Да се додадат функции во класата за додавање нов разговор, и додавање порака во постоечки 
разговор. 
Да се напише класа за секој корисник:
class Korisnik():
 def __init__(self, ime, prezime ... ):
 self.ime, self.prezime... = ime, prezime ...
 self. Razgovori = {}
 def dodajRazgovor(self, korisnik):
 …
 def dodajPoraka(self, poraka, korisnik):
 …
 def zemiPoraki(self, korisnik):
 …
Забелешка: Првиот аргумент во секоја функција од питон класите е self.
Скриптата да се дополни со код за тестирање на класата и функциите.
'''


class user():   #Definiranje n aklasa Korisnik
    def __init__(self, ime, prezime, username, password ):  #inicijalizator na korisnik, negovo ime,prezime...
        self.ime, self.prezime, self.username, self.password = ime, prezime, username, password
        self.chats = {}

    def dodajRazgovor(self, user):
        if user not in self.chats:
            self.chats[user] = []

    def dodajPoraka(self, message, user):
        if user in self.chats:
            self.chats[user] += [message]
        else:
            self.chats[user] = []
            self.chats[user] += [message]

    def getChat(self, user):
        if user in self.chats:
            return self.chats[user]
        
first_user = user('Bisera', 'Naumovska', 'bibi', '2001')
second_user = user('Maksim', 'Mitevski', 'max', '2000')

first_user.dodajRazgovor(second_user.username)
second_user.dodajRazgovor(first_user.username)

first_user.dodajPoraka('Zdravo Max, dobar li si?\n', second_user.username)
second_user.dodajPoraka('Ejjj Bibi. Dobro sum, top.!\n', first_user.username)
second_user.dodajPoraka('Ti dobar li si, shto ima?\n', first_user.username)
first_user.dodajPoraka('Dobar be dobar, okej sum. Shto da ima..hahaha\n', second_user.username)

print("Porakite od razgovorot na prviot korisnik so vtoriot korisnik", first_user.getChat(second_user.username))
print("Porakite od razgovorot na vtoriot korisnik so prviot korisnik", second_user.getChat(first_user.username))