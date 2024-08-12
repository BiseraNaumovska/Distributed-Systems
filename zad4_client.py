""" Да се напише програма во која клиенти можат да комуницираат меѓу себе со помош на
серверот. Клиентите се регистрираат на серверот. Откако ќе бидат регистрирани можат да
праќаат порака до други клиенти. Притоа, истовремено треба да можат да примаат и
пораки од други клиенти. """

import sys, socket, threading, struct

def recv_all(sock, length):
    data = ''
    while len(data) < length:
        more = sock.recv(length - len(data)).decode()
        if not more:
             raise EOFError('socket closed %d bytes into %d-byte message' %(len(data), length))
        data+= more
    return data.encode()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

def citaj(s):
    while True: #ako podatokot e pogolem od 64 bajti, slednite 3 linii kod se standardni za otpakuvanje na kod
        length = struct.unpack("!i" , recv_all(s, 4))[0]
        data = recv_all(s,length)
        data = data.decode().split('|')
        print(data[0] + "kazuva" + data[1] + "\n")

if len(sys.argv) > 2:
    adresa = sys.argv[2]
    s.connect((adresa, 1060))
    uname = sys.argv[1]
    msg = "korime|" + uname
    length = len(msg)
    fullmsg = struct.pack("!i", length) + msg.encode()
    s.sendall(fullmsg)
    length = struct.unpack("!i" , recv_all(s,4))[0]
    reply = recv_all(s,length).decode()
    if reply == 'nedozvoleno':
        print("Korisnichkoto ime vekje e zafateno")
        sys.exit(-1)
    elif reply == 'registriran':
        print("Korisnikot" + uname + "uspeshno se registrirashe")
    try:
        threading.Thread(target = citaj , args=(s,)).start()
        while True:
            dokogo = sys.stdin.readline()[:-1] #se osven posledniot karakter  \n
            poraka = sys.stdin.readline()[:-1]
            msg = "poraka|" + dokogo + "|" + poraka
            length = len(msg)
            fullmsg = struct.pack("!i",length) + msg.encode()
            s.send_all(fullmsg)
    except:
        print("Greshka")
else:
    print("Upotreba: " + sys.argv[0] + "username address")