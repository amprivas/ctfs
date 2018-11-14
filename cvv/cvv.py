#!/usr/bin/env python
import socket
import re
import time
import os
from random import Random
import copy

host = socket.gethostbyname("misc.chal.csaw.io")
port = 8308
s = socket.socket()
loop = True
contador = 0
creditcard2send = ""
#from pwn import *

#Connecting to the socket
def connection():
    try:
        return s.connect((host, port))
    except:
        print "Unexpected error:", sys.exc_info()[0]
        raise

def pwnconnection():
	connection = None
	connection = remote(host,port)
	return connection

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#Credit card prefixs

visaPrefixList = [
        ['4', '5', '3', '9'],
        ['4', '5', '5', '6'],
        ['4', '9', '1', '6'],
        ['4', '5', '3', '2'],
        ['4', '9', '2', '9'],
        ['4', '0', '2', '4', '0', '0', '7', '1'],
        ['4', '4', '8', '6'],
        ['4', '7', '1', '6'],
        ['4']]

mastercardPrefixList = [
        ['5', '1'], ['5', '2'], ['5', '3'], ['5', '4'], ['5', '5']]

amexPrefixList = [['3', '4'], ['3', '7']]

discoverPrefixList = [['6', '0', '1', '1']]

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#Generating the medium numbers of creditcard
def completed_number(prefix, length):
    ccnumber = prefix

    # generate digits

    while len(ccnumber) < (length - 1):
	generator = Random()
        digit = str(generator.choice(range(0, 10)))
        ccnumber.append(digit)

    # Calculate sum

    sum = 0
    pos = 0

    reversedCCnumber = []
    reversedCCnumber.extend(ccnumber)
    reversedCCnumber.reverse()

    while pos < length - 1:
        odd = int(reversedCCnumber[pos]) * 2
        if odd > 9:
            odd -= 9

        sum += odd

        if pos != (length - 2):
            sum += int(reversedCCnumber[pos + 1])
        pos += 2

    # Calculate check digit
    checkdigit = ((sum / 10 + 1) * 10 - sum) % 10
    ccnumber.append(str(checkdigit))

    return ''.join(ccnumber)

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#Generatig a creditcard number
def credit_card_number(rnd, prefixList, length):
    result = ""
    ccnumber = copy.copy(rnd.choice(prefixList))
    result = completed_number(ccnumber, length)

    return result

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#Generating the string of the creditcard
def output(title, numbers):
    result = []
    result.append(title)
    result.append('\n'.join(numbers))

    return '\n'.join(result)

#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#Understanding the requested information
def getCreditCardType(cadena):

    matched = re.search( r'(.*)\s(?P<creditcard>Discover|Visa|American\sExpress|MasterCard|\d+)!', cadena )
    if matched != None:
    	return matched.group(2)
    else:
    	matched = "nada"
    	return 

#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#Identifying the creditcard type
def getcreditcardnumber(st):
	generator = Random()
	ccgenerated = ""
	if st == "MasterCard":
		ccgenerated = credit_card_number(generator, mastercardPrefixList, 16)
		return ccgenerated
	elif st == "Visa":
		ccgenerated = credit_card_number(generator, visaPrefixList, 16)
		return ccgenerated
	elif st == "American Express":
		ccgenerated = credit_card_number(generator, amexPrefixList, 15)
		return ccgenerated
	elif st == "Discover":
		ccgenerated = credit_card_number(generator, discoverPrefixList, 16)
		return ccgenerated
	else:
		ccgenerated = st
		return ccgenerated
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#Validating the request
def requestvalidation(reqval):
	request = ""
	if reqval.find("I need a new card that starts with") != -1:
		request = "4d"
		return request
	elif reqval.find("I need a new") != -1:
		request = "ccardt"
		return request
		
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#Concatenating the shortcreditcard with the numbersrequested
def getcreditcardshortnumber(strdig):
	generator = Random()
	concatcc = ""
	concatcc = strdig+credit_card_number(generator, mastercardPrefixList, 11)
	return concatcc
	
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#Validating null data in a variable
def varnullvalidation(v2v):
	if v2v == None:
		return False
	else:
		return True

#
# Main
#

connection()

while loop:
	ccdata = s.recv(1024)
	print ccdata
	cctype = getCreditCardType(ccdata)
	
	if cctype != "nada":
		gencc = ""
		if ccdata.find("I need a new card that starts with") != -1:
			gencc = getcreditcardshortnumber(cctype)
		elif ccdata.find("I need a new") != -1:
			gencc = getcreditcardnumber(cctype)
		else:
			loop = False

		#contador = contador + 1
		#os.system('cls' if os.name == 'nt' else 'clear')
		#print "++++++++++++++++++ intento: "+str(contador)+"+++++++++++++++++++++++++"
		print "Nos pide: " + cctype
		print "Enviando: " + str(gencc)
		if varnullvalidation(gencc):
			s.send(gencc+"\n")
			print "Tarjeta enviada"
		else:
			print "La variable que contiene los datos a enviar esta vacia,\nTerminando el script.........."
			loop = False
	elif cctype == "nada":
		print "No reconozco esta peticion\nTerminando el script...."
		loop = False
	


#mastercard = credit_card_number(generator, mastercardPrefixList, 16)
#print "Mastercard: ", str(mastercard)

#visa = credit_card_number(generator, visaPrefixList, 16)
#print "Visa: ", str(visa)

#american_express = credit_card_number(generator, amexPrefixList, 15)
#print "American Express: ", str(american_express)

#discover = credit_card_number(generator, discoverPrefixList, 16)
#print "Discover: ", str(discover)



