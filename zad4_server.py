""" Да се напише програма во која клиенти можат да комуницираат меѓу себе со помош на
серверот. Клиентите се регистрираат на серверот. Откако ќе бидат регистрирани можат да
праќаат порака до други клиенти. Притоа, истовремено треба да можат да примаат и
пораки од други клиенти. """

import sys, socket, threading, struct

l = threading.RLock() # za da se sprechi istovremeno da se pristapi do eden objekt
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
users = dict() #rechnik

s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR , 1)
#za da moze da gi koristime opciite na soketot , treba da se dozvoli povtorna upotreba na istite adresi , vrednost sekogash = 1

def recv_all(sock, length):
    data = ''
    while len(data) < length:
        more = sock.recv(length - len(data)).decode()
        if not more:
            raise EOFError('socket closed %d bytes into %d-byte message' %(len(data), length))
        data+= more
    return data.encode()

def opsluzhiKlient(s):
    while True:
        length = struct.unpack("!i", recv_all(s, 4))[0]
        data = recv_all(s,length)
        data = data.decode().split("|")
        if data[0] == 'korime':
            korime = data[1]
            l.acquire() #go zakluchuva, se izvrshuva pa se otkluchuva
            if korime in users:
                msg = "nedozvoleno"
                length = len(msg)
                msg = struct.pack("!i", length) + msg.encode()
                s.sendall(msg)
            else:
                users[korime] = s
                msg = "registriran"
                length = len(msg)
                msg = struct.pack("!i" , length) + msg.encode()
                s.sendall(msg)
        elif data[0] == 'poraka' and data[1] in users:
            korime_dest = data[1]
            msg = korime + "|" + data[2]
            length = len(msg)
            fullmsg = struct.pack("!i", length) + msg.encode()
            users[korime_dest].sendall(fullmsg)

s.bind(('localhost' , 1060))
s.listen(1)

while True:
    sc, sockname = s.accept()
    threading.Thread(target = opsluzhiKlient , args=(sc,)).start()
    print("Upotreba: " + sys.argv[0] + "username || dest + msg")


 
