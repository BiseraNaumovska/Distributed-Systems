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


import sys, socket, threading

class user():
    def __init__(self, ime, prezime, username, password):
        self.ime, self.prezime, self.username, self.password = ime, prezime, username, password
        self.chats = {} #razgovorite se kao rechnik 

    def dodajRazgovor(self, user):
        if user not in self.chats:
            self.chats[user] = []   #ako korisnikot ne postoi vo listata razgovori, togash se kreira prazna lista za negovite razgovori

    def dodajPoraka(self, message, user): #za da se napishe poraka vo razgovorot so drugiot korisnik
        if user in self.chats:
            self.chats[user] += [message]
        else:
            self.chats[user] = []
            self.chats[user] += [message]

    def zemiPoraki(self, user):
        if user in self.chats:
            return self.chats[user]
        
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
max_bytes = 65535
port = 1060

def displayMessage(s): #za da se prikaze tekstot shto e primen na ekran
    while True:
        data = s.recvfrom(max_bytes)
        print(data.decode())

if sys.argv[1:] == ['server']:  #povikuvanje kako server UDP
    users = {}  #rechnik za chuvanje na korisnicite
    s.bind(('127.0.0.1', port))
    print('Server is listening at %s' % repr(s.getsockname()))

    while True:
        data, address = s.recvfrom(max_bytes)
        message = data.decode().split('|')
        message_type = message[0] #prviot zbor se zima

        if message_type == 'Zdravo': #ako prviot zbor e zdravo znachi deka klientot saka da se najavi
            ime = message[1]
            prezime = message[2]
            username = message[3]
            password = message[4]

            if username not in users:   #ako korisnikot ne postoi od prethodno kreira nov user
                users[username] = user(ime, prezime, username, password) #se kreira nov objekt od klasata user
                print('Korisnikot %s se logirashe' % username)
                s.sendto('Uspeshno'.encode(), address)
            else:   #ako vekje postoi korisnichkoto ime -> neuspeshno
                print('Neuspeshno logiranje, username-ot vekje postoi!')
                s.sendto('Invalid'.encode(), address)

        elif message_type == 'Destinacija':
            username = message[1]
            sender = message[3]

            if username in users:
                message_to_send = sender + ": " + message[2]
                users[sender].dodajPoraka(message[2], username)

                print('Poraka za isprakjanje: %s' % message_to_send)
                s.sendto(message_to_send.encode(), users[username].address)
            else:
                s.sendto(('Korisnikot %s ne e registriran' % username).encode(), address)
elif sys.argv[1:] == ['client']:    #povikuvanje kako klient
    ime = input('Vnesi ime: ')
    prezime = input('Vnesi prezime: ')
    username = input('Vnesi username: ')
    password = input('Vnesi password: ')

    s.sendto(('Zdravo|' + ime + '|' + prezime + '|' + username + '|' + password).encode(), ('127.0.0.1', port))
    data, address = s.recvfrom(max_bytes) #primanje na odgovor od serverot
    reply = data.decode()

    if reply == 'Uspeshno':
        print('Uspeshno se logiravte!')
        threading.Thread(target = displayMessage, args = (s, )).start()

        while True:
            destination = input('Vnesi go primachot:\n')
            message = input('Vnesi poraka:\n')

            s.sendto(('Destination|' + destination + '|' + message + '|' + username).encode(), ('127.0.0.1', port))
    elif reply == 'Neuspeshno':
        print('Username-ot postoi, obidi se povtorno!')
else:
    print('Invalid use of Python script')