'''
1. Да се сними дадената скрипта и да се стартува серверот. Потоа неколку пати да се 
стартува клиентот.
import random, socket, sys
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
MAX = 65535
PORT = 1060
if 2 <= len(sys.argv) <= 3 and sys.argv[1] == 'server':
interface = sys.argv[2] if len(sys.argv) > 2 else ''
s.bind((interface, PORT))
print('Listening at', s.getsockname())
while True:
data, address = s.recvfrom(MAX)
if random.randint(0, 1):
print('The client at', address, 'says: ', repr(data))
s.sendto(('Your data was %d bytes' %len(data)).encode(), address)
else:
print('Pretending to drop packet from: ', address)
elif len(sys.argv) == 3 and sys.argv[1] == 'client':
hostname = sys.argv[2]
s.connect((hostname, PORT))
print('Client socket name is: ', s.getsockname())
delay = 0.1
while True:
s.send('This is another message'.encode())
print('Waiting up to ', delay, ' seconds for the server to reply.')
s.settimeout(delay)
try:
data = s.recv(MAX)
except socket.timeout:
delay *= 2
if delay > 2.0:
raise RuntimeError('I think the server is down...')
except:
raise
else:
break
print ('The server says', repr(data))
else:
print(sys.stderr, 'usage: aud_1_1_udp_klient_server_so_problemi.py server [ <interface> ]')
print(sys.stderr, ' or: aud_1_1_udp_klient_server_so_problemi.py client <host>')
sys.exit(2)


Да се анализира кодот.
2. Зошто се користи connect кај UDP конекција?
3. За што служи settimeout?

'''



import random, socket, sys
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
MAX = 65535
PORT = 1060

if 2 <= len(sys.argv) <= 3 and sys.argv[1] == 'server':
    interface = sys.argv[2] if len(sys.argv) > 2 else ''
    s.bind((interface, PORT))
    print('Listening at', s.getsockname())
    while True:
        data, address = s.recvfrom(MAX)
        if random.randint(0, 1):
            print('The client at', address, 'says: ', repr(data))
            s.sendto(('Your data was %d bytes' %len(data)).encode(), address)
        else:
            print('Pretending to drop packet from: ', address)
elif len(sys.argv) == 3 and sys.argv[1] == 'client':
    hostname = sys.argv[2]
    s.connect((hostname, PORT))
    print('Client socket name is: ', s.getsockname())
    delay = 0.1
    while True:
        s.send('This is another message'.encode())
        print('Waiting up to ', delay, ' seconds for the server to reply.')
        s.settimeout(delay)
        try:
            data = s.recv(MAX)
        except socket.timeout:
            delay *= 2
            if delay > 2.0:
                raise RuntimeError('I think the server is down...')
        except:
            raise
        else:
            break
    print ('The server says', repr(data))
else:
    print(sys.stderr, 'usage: server1.py server [ <interface> ]')
    print(sys.stderr, ' or: client1.py client <host>')
sys.exit(2)


# 2.
'''
Connect funkcijata vo Python Socket API se koristi za da se ovozmozi
povrzuvanje, odnosno konekcija so soodvetniot socket, koj shto pak socket e 
definiran so IP adresa i broj na porta.

Ako imame UDP, koj shto e nekonekciski orientiran protokol, funkcijata connect() 
ovozmozuva ednokratno otvaranje na socket za da moze da se vospostavi vrskata i da se
ovozmozi komunikacijata 

'''
# 3.
'''
settimeout() funkcijata ovozmozuva podesuvanje na vrednosta na timeout-ot
na soketot. Timeout e vremenski interval vo koj soodvetniot socket
mora da ja isprati ili pak primi potrebanta informacija.
Ako porakata ne e primena vo soodvetniot interval i timeout-ot isteche,
togash se javuva greshka za socket timeout.
'''
