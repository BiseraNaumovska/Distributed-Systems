'''
4. Да се измени скриптата така што клиентот и серверот ќе се стартуваат од различни 
датотеки, а притоа во повикувањето на скриптата нема да се наведува како аргумент 
на позиција 1 за кого станува збор.
5. Да се измени кодот од UDP комуникацијата клиент-сервер, така што клиентот да 
може да побара од серверот три различни пресметки: 
• ако клиентот наведе ‘tobits’ и цел број, серверот да му врати пресметка 
на тој цел број во бити;
• ако клиентот наведе ‘tobytes’ и цел број, серверот да му врати пресметка 
на тој цел број во бајти;
• ако клиентот наведе ‘length’ и реченица, серверот да му ја врати 
пресметката на реченицата во бајти
'''

import sys, socket, random

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
max_bytes = 65535
port = 1060

if len(sys.argv) == 4: #proverka dali ima 4 argumenti koga ja startuvame skriptata
    hostname = sys.argv[1] #vtor argument za ime na server
    delay = 0.1 #chekanje na odgovor od serverot

    s.connect((hostname, port))
    print('Client socket name is: %s' % repr(s.getsockname()))

    while True: #klientot ke isprakja baranja do serverot dodeka ne dobie odgovor
        message = sys.argv[2] + '|' + sys.argv[3] #spojuvanje na  vtor i tret element
        s.send(message.encode()) #podatokot se prakja vo bajti preku metodata encode()
        print('Waiting for %f seconds for server to reply' % delay)
        s.settimeout(delay)

        try:
            data = s.recv(max_bytes) #primanje podatoci od server
        except socket.timeout: #ako ima iskluchok kodot sepak ke se izvrshi
            delay *= 2

            if delay > 2.0:
                raise RuntimeError('The server is down...')
        except:
            raise #vo sprotiv o se izvrshu a blokot kod
        else:
            break

    print('The server replied: %s' % repr(data.decode()))
else:
    print('Invalid use of Python script! A valid server IP address and message mode must be specified')