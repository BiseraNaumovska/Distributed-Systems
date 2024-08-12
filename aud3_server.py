import sys, socket, threading, struct

l = threading.RLock()
users = dict() #dictionary
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

def recv_all(sock,length):
    data=''
    while len(data) < length:   #ako goleminata na soketot e pomala od dolzinata na podatokot
        more = sock.recv(length-len(data)).decode()
        if not more:
            raise EOFError('socket closed %d bytes into a %d-byte message'%(len(data), length))
        data +=more
    return data.encode()

def opsluziKlient(s):
    while True:
        length = struct.unpack("!i", recv_all(s,4))[0]
        data = recv_all(s,length)
        data = data.decode().split(".")
        if data[0] == 'korime':
            korime = data[1]
            l.acquire()
            if korime in users:
                msg = "nedozvoleno"
                length = len(msg)
                msg = struct.pack("!i",length) + msg.encode()
                s.sendall(msg)
            else:
                users[korime] = s
                msg = 'registriran'
                length = len(msg)
                msg = struct.pack("!i",length) + msg.encode()
                s.sendall(msg)
            l.release()
        elif data[0] == 'poraka' and data[1] in users:
            dokogo = data[1] 
            msg = korime + "." + data[2]
            length = len(msg)
            fullmsg = struct.pack("!i" , length) + msg.encode()
            users[dokogo].sendall(fullmsg)

s.bind(('localhost' , 1061))
s.listen(1)
while True:
    sc,sockname = s.accept()
    threading.Thread(target = opsluziKlient , args=(sc,)).start()

