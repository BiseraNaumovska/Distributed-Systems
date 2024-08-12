""" Да се напише P2P апликација за размена на статии (текстови). 
Секој клиент има речник со статии дефинирана во кодот, со облик: 
statii = { "Naslov1" : "Tekst od statijata Naslov 1", "Naslov2" : "Tekst od statijata Naslov 2" } 
При поврзување со серверот, клиентите ја испраќаат само листата од свои наслови. 
Корисникот од тастатура внесува наслов, и доколку го нема кај себе, се испраќа барање до 
серверот. 
Серверот ја враќа IP адресата на првиот клиент кој го има тој наслов. 
Потоа клиентот се поврзува на другиот клиент и од него ја превзема статијата.
 """

import socket, threading, struct, pickle
#so pickle se prenesuvaat pokompleksni stvari, nizi, rechnici, strukturni python slozeni objekti
#otkako ke gi pratime podatocite da pristignat kako shto treba

#Naslov1: "Tekst od naslov1"    ->   kluch:vrednost

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#preku soketi sakame da se reiskoristuvaat adresite, da ne sedat zafateni

srv = ('0.0.0.0', 1060)
s.bind(srv)
l = threading.Lock() #vkluchuvam lock -> zakluchuvame
library = {}

def recv_all(sock,length):
    data = ''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError('socket closed %d bytes into %d-byte message' %(len(data), length))
        data += more.decode('latin1')
    return data.encode('latin1') 
    # latin1  =  azbuki od zapadno-evropski jazici  = bukva po bukva od levo kon desno

def serve(sc, socketname):
    while True:
        data = recv_all(sc , struct.unpack("!i", recv_all(sc,4))[0])
        zb = data.decode('latin1').split(".")
        if zb[0] == "connect":
            print("Client" , socketname, " requesting to connect \n")
            sc.sendall(struct.pack("!i" , len("OK, send the list. ")) + "OK, send the list. ".encode('latin1'))
            length = struct.unpack("!i", recv_all(sc,4))
            print(length)
            data = recv_all(sc, length[0])
            datal = pickle.loads(data)
            with l:
                #ekvivalentno na zakluchuvanje
                for i in datal:
                    library[i] = (zb[1] , zb[2]) # ova e dataat shto ja primam
            sc.sendall(struct.pack("!i", len("list accepted")) + "list accepted".encode('latin1'))
            print("Connection with client " , socketname, "successfully completed")
        
        elif zb[0] == "search":
            with l:
                if zb[1] in library:
                    print(zb[1] , " is found at " , library[zb[1]])
                    msg = "OK." + library[zb[1]][0] + "." + library[zb[1]][1]   #ok adresa porta
                    sc.sendall(struct.pack("!i", len(msg)) + msg.encode('latin1'))
                else:
                    msg = "Error. No such file in library"
                    sc.sendall(struct.pack("!i", len(msg)) + msg.encode('latin1'))
s.listen(1) #slushame sega
while True:
    sc, socketname = s.accept() #nekoj shto se obidel da se svrze na serverot, go primame
    t = threading.Thread(target = serve, args = (sc, socketname,)).start()
    #sc,sockname se argumentite za serve funkcijata

 