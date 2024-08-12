import sys, socket, threading, struct

def recv_all(sock,length):
    data=''
    while len(data) < length:
        more = sock.recv(length-len(data)).decode()
        if not more:
            raise EOFError('sock closed at %d bytes into %d-byte message' %(len(data),length))
        data += more
    return data.encode()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

def citaj(s):
    while True:
        length = struct.unpack("!i", recv_all(s,4))[0]
        data = recv_all(s,length)
        data = data.decode().split(".")
        print(data[0] + "veli:  " + data[1] + "\n")

if len(sys.argv) > 2:
    adresa = sys.argv[2]
    s.connect((adresa,1061))
    uname = sys.argv[1]
    msg = "korime." + uname
    length = len(msg)
    fullmsg = struct.pack("!i",length) + msg.encode()
    s.sendall(fullmsg)
    length = struct.unpack("!i", recv_all(s,4))[0]
    reply = recv_all(s,length).decode()
    if reply == 'nedozvoleno':
        print("Korisnichkoto ime  evekje zafateno \n")
        sys.exit(-1)
    elif reply == "registriran":
        print("Korisnikot " + uname + " uspeshno se registrirashe \n")
    try:    #tuka ima moznost za greshka pa zatoa so try i except
        threading.Thread(target = citaj, args=(s,)).start()
        while True:
            dokogo = sys.stdin.readline()[:-1]
            poraka = sys.stdin.readline()[:-1]
            msg = "poraka." +dokogo+"."+poraka
            length = len(msg)
            fullmsg = struct.pack("!i",length) + msg.encode()
            s.sendall(fullmsg)
    except:
        print("GRESHKA!!! \n")

else:
    print("Usage: python aud3_client.py bibi 127.0.0.1")
