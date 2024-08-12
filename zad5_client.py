""" Да се напише P2P апликација за размена на статии (текстови). 
Секој клиент има речник со статии дефинирана во кодот, со облик: 
statii = { "Naslov1" : "Tekst od statijata Naslov 1", "Naslov2" : "Tekst od statijata Naslov 2" } 
При поврзување со серверот, клиентите ја испраќаат само листата од свои наслови. 
Корисникот од тастатура внесува наслов, и доколку го нема кај себе, се испраќа барање до 
серверот. 
Серверот ја враќа IP адресата на првиот клиент кој го има тој наслов. 
Потоа клиентот се поврзува на другиот клиент и од него ја превзема статијата.
 """

import socket, threading, pickle, struct

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#potrebni ni se dva soketi, ako sakam da komuniciram i so server, a edniot za drugite klienti

s.bind(('0.0.0.0', 0))  #za so server ili za so drug klient koga jas komuniciram
sl.bind(('', 0))    #razlichni klienti ke imaat razlichni adresi = koga drugi sakaat da iskomuniciraat so mene
print(sl.getsockname())
print(s.getsockname())
srv = ('127.0.0.1' , 1060)

statii = {}

def recv_all(sock, length):
    data =''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError('... end of file')
        data += more.decode('latin1')
    return data.encode('latin1')

def hear(sl): #ova mi e za komunikacijata so razlichnite klienti
    sl.listen(10)  #kolku klienti vo eden moment mozam da opsluzam = 10
    while True:
        sc,socketname = sl.accept()
        data = recv_all(sc,struct.unpack("!i", recv_all(sc,4))[0]).decode('latin1')
        sc.sendall(struct.pack("!i",len(statii[data])) + statii[data].encode('latin1'))
        sc.close()  #pishuvame i go zatvorame soketot, ne se gasne


n = input("Enter number of entries \n")
for i in range(int(n)):
    ime = input("Enter name of text \n")
    text = input("Enter text \n")
    statii[ime] = text
s.connect(srv)
t = threading.Thread(target = hear, args = (sl,)).start()

while True:
    command = input("Connect to server or search for text \n")
    if command == "connect":
        msg = "connect." + sl.getsockname()[0] + "." + str(sl.getsockname()[1])
        s.sendall(struct.pack("!i", len(msg)) + msg.encode('latin1'))
        dat = recv_all(s, struct.unpack("!i", recv_all(s,4))[0])
        print(dat)
        statii_keys = []
        for key in statii.keys():
            statii_keys.append(key)
        msg = pickle.dumps(statii_keys)
        s.sendall(struct.pack("!i", len(msg)) + msg)
        dat = recv_all(s, struct.unpack("!i", recv_all(s,4))[0])
        print(dat)

    elif command == "serach":
        c = input("Enter title \n")
        msg = "search." + c
        s.sendall(struct.pack("!i", len(msg)) + msg.encode('latin1'))
        dat = recv_all(s, struct.unpack("!i", recv_all(s,4))[0])
        d = dat.decode('latin1').split(".")
        if d[0] == "OK":
            sv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(d[1], int(d[2]))
            #sega sakam da se konektiram kaj drugiot klient-drugarot
            sv.connect((d[1], int(d[2])))
            sv.send(struct.pack("!i", len(c)) + c.encode('latin1'))
            rez = recv_all(sv, struct.unpack("!i", recv_all(sv,4))[0]).decode('latin1')
            print(rez)
            sv.close()
        elif d[0] == 'Error':
            print(d[1])
