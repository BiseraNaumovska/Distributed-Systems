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
#sys -> za rabota so vlez
#socket -> za mrezna komunikacija, rabota so soketi
#random -> za sluchajno generiran broj

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) #kreiranje na udp soket
max_bytes = 65535
port = 1060

if len(sys.argv) == 2:  #dali ima dva argumenta koga ja startuvame programava
    interface = sys.argv[1] #prviot argument od terminal = ip adresata na koja serverot ke slusha klienti
    s.bind((interface, port)) #povrzuvanje na soketot so ip adresa i porta za slushanje
    print('Socket is listening at %s' % repr(s.getsockname()))

    while True: #dodeka serverot slusha
        data, address = s.recvfrom(max_bytes) #cheka da primi podatok od klientot=data i adresa=address

        if random.randint(0, 1): #serverot random ke odluchi dali da ja primi porakata od klientot ili ke ja otfrli
            message = data.decode().split('|') #dekodiranje na podatokot od bajti vo tekst i razdeluvanje na porakata

            if message[0] == 'ToBits': #vo shto sakame da pretvorime dali bajti ili biti
                number = message[1]
                number = int(number)
                binary = bin(number)[2:]
                print("Brojot binarno e: %s" % binary)
                s.sendto(('The number converted to binary is equal to %s' % binary).encode(), address)
            elif message[0] == "ToBytes":
                number = message[1]
                number = int(number)
                number_of_bytes = int((number / 256) + 1)
                byte_value = number.to_bytes(number_of_bytes, 'big')
                print("Brojot vo bajti e: %s" % byte_value)
                s.sendto(('The number converted to bytes is equal to %s' % byte_value).encode(), address)
            elif message[0] == "Length":
                sentence = message[1]
                print("The client's sentence has a length of %d bytes" % len(sentence))
                s.sendto(('The sent message has a length of %d bytes' % len(sentence)).encode(), address)
        else:
            print('Random datagram drop from address: %s' % repr(address)) # ako so random se odluchi da ne se primi porakata, taa se otfrla
else:
    print('Invalid use of Python script! A valid server IP address must be specified') #ako ima pomalku od 2 argumenta vo terminal