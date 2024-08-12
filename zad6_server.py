""" Да се напише едноставна RPC клиент сервер апликација во која серверот ќе му овозможи на 
клиентот да користи негови функционалности (две математички пресметки и една repr()).
*The repr() function returns a printable representation of the given object. """


#!/usr/bin/env python

import operator, math
from functools import reduce
from xmlrpc.server import SimpleXMLRPCServer

def addtogether(*things):
    #add together everythng in the list *things
    return reduce(operator.add, things)

def quadratic(a,b,c):
    #Determine x values satisfying : a *x*x + b *x +c =0
    b24ac = math.sqrt(b*b - 4.0*a*c )
    return list(set([(-b-b24ac) / 2.0*a,
                     (-b+b24ac) / 2.0*a]))

def remote_repr(arg):
    #return the repr() rendering of the supplied arg
    return arg
    #vrakja neshto shto e chitlivo za nas = reprezentacija shto moze da se ispechati i e jasna za nas

server = SimpleXMLRPCServer(('127.0.0.1' , 7001))
server.register_introspection_functions() #registrira funkcii signature, help, method... ni pomaga za da moze da gi povika i izlista 
server.register_multicall_functions()

server.register_function(addtogether)
server.register_function(quadratic)
server.register_function(remote_repr)

print("Server ready")
server.serve_forever()
