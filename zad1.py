"""
Да се напише едноставна UDP клиент-сервер апликација во која серверот ќе чека 
пораки од клиенти, а клиентот ќе испраќа порака и ќе чека потврден одговор 
за прием од серверот
"""

import sys, socket

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

MAX = 65535
PORT = 1060

if sys.argv[1:] == ["server"]: 
    s.bind(('127.0.0.1' , PORT))
    print("Listening at", s.getsockname())

    while True:
        data,address = s.recvfrom(MAX)
        print('The client at', address, 'says', repr(data))
        s.sendto(('Your message was %d bytes' %len(data)).encode(),address)
       
        
elif sys.argv[1:] == ["client"]:
      # print('Address before sending: ', s.getsockname())
       s.sendto('This is my message'.encode(), ('127.0.0.1', PORT))
       print('Address after sending: ', s.getsockname())
       data,address = s.recvfrom(MAX)
       print('The server says', repr(data))

else:
     print(sys.stderr, 'usage:zad1.py server|client')