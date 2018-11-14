#!/usr/bin/env python
import sys
import socket
import re
import time
import os

host = socket.gethostbyname("misc.chal.csaw.io")
port = 4239
s = socket.socket()
loop = True
parity = 0
contador = 0
flag = ""

#Funcion para abrir comunicacion con el socket
def obconnection():
    try:
        return s.connect((host, port))
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

#Funcion para obtener unicamente el string con los bits
def getbytestring(st):
    matched = re.search( r'.*(?P<dbytes>\d{11})', st )
    return matched.group()

#Funcion que calcula el bit de paridad
def parity_brute_force(x):
        bit = 0
        num_bits = 0
        while x:
            bitmask = 1 << bit
            bit += 1
            if x & bitmask:
                num_bits += 1
                x &= ~bitmask
        return num_bits % 2

#Main
#Conectandome....
obconnection()

while loop:
    contador = contador + 1
    strbytes = getbytestring(s.recv(1024))
    f = parity_brute_force(int(strbytes,2))

    if f>0:
        os.system('cls' if os.name == 'nt' else 'clear')
        s.send("1")
        print "+++++++++++++++++++++++++++++++++++"+str(contador)+" lineas+++++++++++++++++++++++++++++++++++++++"
        flag = flag + chr(int(strbytes[1:9:],2))
        print flag
        if chr(int(strbytes[1:9:],2)) == "}":
            print "Se ha obtenido el flag completamente!!!"
            loop = False

    else:
        s.send("0")
