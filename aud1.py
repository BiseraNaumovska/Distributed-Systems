import sys, socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

MAX=65535
PORT=1060

if sys.argv[1:] == ['server']:
    #ako e server, mora da se otvori serverot za da pochne da prima poraki
    s.bind(('127.0.0.1', PORT))
    print('server listening at', s.getsockname()) #samo da se ispoishe na ekranot na koja adresa i porta slusha serverot
    while True: #celo vreme moze da prima poraki odnovo i odnovo od klienti
        data, address = s.recvfrom(MAX) #za primanje na podatoci od klientot
        #vo adrsa ke se vpishe adresata na podatokot-data
        #MAX = goleminata na najgolemata poraka shto moze da se primi od klientot
        print("Klientot na adresa", address, "veli" , repr(data))  #repr(data) go pokazuva podatokot kako string
        s.sendto(('Vashata poraka e golema %d bytes'%len(data)).encode(), address)
elif sys.argv[1:] == ['client']:
   # print('Adresata 1 e: ', s.getsockname())
    s.sendto('Ova e mojata poraka koja shto ja isprakjam do serverot: '.encode(), ('127.0.0.1', PORT))
    print('Adresata 2 e: ', s.getsockname())
    data,address = s.recvfrom(MAX)
    print('Serverot veli: ', repr(data))
else:
    print(sys.stderr, 'Upotreba: python aud1.py server|client')
