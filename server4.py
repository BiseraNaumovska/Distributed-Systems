'''
2. Да се напише мрежна апликација за едноставна комуникација помеѓу повеќе клиенти и со 
користење на UDP сокети и со TCP сокети (две засебни комуникации – две задачи).
Да се искористи класата Korisnik за чување на информации за корисниците и разменетите 
пораки. 
Секој клиент се поврзува со серверот и му испраќа корисничко име. 
Потоа, кај клиентот од тастатура се внесува корисничко име и порака, по што клиентот ја 
испраќа пораката до серверот а тој ја препраќа до соодветниот корисник
'''


import sys, socket, threading, struct

class user():
    def __init__(self, ime, prezime, username, password, address, socket):
        self.ime, self.prezime, self.username, self.password, self.address, self.socket = ime, prezime, username, password, address, socket
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

    def zemiPoraki(self, user):
        if user in self.chats:
            return self.chats[user]
        
lock = threading.RLock()    #za osloboduvanje na nitki
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #kreiranje na TCP soket sega
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

max_bytes = 65535
port = 1060

#klient
def recv_all(socket, length):   #prima podatoci od soketot
    data = ''

    while len(data) < length:
        more = socket.recv(length - len(data)).decode()

        if not more:
            raise EOFError('Socket closed %d bytes into a %d-byte message' % (len(data), length))
        
        data += more
    
    return data.encode()

def read_all(socket):   #chita podatoci od soketot i gi dava na ekran
    while True:
        length = struct.unpack("!i", recv_all(socket, 4))[0]
        data = recv_all(socket, length)
        data = data.decode().split('|')

        print('%s: %s' % (data[0], data[1]))

def serveClient(socket, address, users): #obsluzuva klienti, prima poraki i prakja odgovori
    while True:
        length = struct.unpack("!i", recv_all(socket, 4))[0]
        data = recv_all(socket, length)
        data = data.decode().split('|')

        if data[0] == 'Zdravo':
            ime = data[1]
            prezime = data[2]
            username = data[3]
            password = data[4]

            lock.acquire()

            if username in users:
                message = 'Nevalidno'
                length = len(message)
                message = struct.pack("!i", length) + message.encode()
                socket.sendall(message)
            else:
                users[username] = (user(ime, prezime, username, password, address, socket))
                message = "Uspeshno"
                length = len(message)
                message = struct.pack("!i", length) + message.encode()
                socket.sendall(message)

            lock.release()
        elif data[0] == "Destination" and data[1] in users:
            destination = data[1]
            message = username + '|' + data[2]
            users[username].addMessage(data[2], destination)

            length = len(message)
            message = struct.pack("!i", length) + message.encode()
            users[destination].socket.sendall(message)

if sys.argv[1:] == ['server']:
    users = dict()
    s.bind(('127.0.0.1', 1060))
    s.listen(1)
    print('Server is listening at %s' % repr(s.getsockname()))

    while True:
        socket_temp, address = s.accept()
        threading.Thread(target = serveClient, args = (socket_temp, address, users)).start()
elif sys.argv[1:] == ['client']:
    s.connect(('127.0.0.1', 1060))

    ime = input('Vnesi ime: ')
    prezime = input('Vnesi prezime: ')
    username = input('Vnesi username: ')
    password = input('Vnesi password: ')

    message = 'Zdravo|' + ime + '|' + prezime + '|' + username + '|' + password

    length = len(message)
    message = struct.pack("!i", length) + message.encode()
    s.sendall(message)

    length = struct.unpack("!i", recv_all(s, 4))[0]
    reply = recv_all(s, length).decode()

    if reply == 'Nevalidno':
        print('Username vekje postoi, obidi se povtorno!')
        sys.exit(-1)
    elif reply == 'Uspeshno':
        print('Uspeshno se logiravte!')
        try:
            threading.Thread(target = read_all, args = (s, )).start()

            while True:
                destination = input('Vnesi go primachot:\n')
                message = input('Vnesi poraka:\n')

                message = 'Destination|' + destination + '|' + message
                length = len(message)
                message = struct.pack("!i", length) + message.encode()
                s.sendall(message)
        except:
            print('error')
else:
    print('Invalid use of Python script')