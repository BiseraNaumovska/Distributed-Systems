""" Да се напише едноставна RPC клиент сервер апликација во која серверот ќе му овозможи на 
клиентот да користи негови функционалности (две математички пресметки и една repr()).
*The repr() function returns a printable representation of the given object. """

#!/usr/bin/env python

import xmlrpc.client as client
proxy = client.ServerProxy('http://127.0.0.1:7001', allow_none = True)
print('Here are the functions supported by this server: ')

for method_name in proxy.system.listMethods():  #tuka spagjaat def (sistemski metodi) shto gi kreiravme kaj serverot rachno
    if method_name.startswith('system'):
        continue
    signatures = proxy.system.methodSignature(method_name)
    if isinstance(signatures, list) and signatures:
        for signature in signatures:
            print('%s (%s)' %(method_name, signature))
    else:
        print('%s (...)' %(method_name))
    method_help = proxy.system.methodHelp(method_name) #vrakja za sekoj metod kako se koristi
    if method_help:
        print(' ', method_help)

#do tuka bea funkcii sega rpc
print(proxy.addtogether('x', 'y' , 'z'))
print(proxy.addtogether(20, 30, 4, 1))
print(proxy.quadratic(2, -4 , 0))
print(proxy.quadratic(1,2,1))
print(proxy.remote_repr([1, 2.0, 'three']))
print(proxy.remote_repr((1, 2.0 , 'three')))
print(proxy.remote_repr({'name': 'Bisera' , 'data': {'age':26 , 'sex' : 'F'} }))

multicall = client.MultiCall(proxy)
multicall.addtogether('a' , 'b' , 'c')
multicall.quadratic(2 , -4, 0)
multicall.remote_repr([1 , 2.0 , 'three'])
for answer in multicall():
    print(answer)


