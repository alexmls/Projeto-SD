#!/usr/bin/python
# Autor: Alexandre Mariano, Murilo Marques, Guilherme Campos

import socket
import ConfigParser
import threading
import time
from serconcproxy import Serconc

#config = ConfigParser.ConfigParser()
#config.read("connection.ini")  # reading the config file

#host = config.get('Section one', 'host')  # using the config file values
#port = config.getint('Section one', 'port')

#des = (host, port)
#s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # creating a socket object

#lst = []  # Result list


def menu(opt):
    i = 0
    while i != 1:  # check if the key is less than 20 bytes
        key = raw_input('Enter with key:')
        if len(key) > 40:
            print 'Enter a key less than 40 digits!!!'

        elif ',' in key or '.' in key or '*' in key or ' ' in key or '=' in key:
            print 'Just words or numbers'
        else:
            i = 1

    if opt == "1" or opt == "3":
        j = 0
        while j != 1:
            sti = raw_input('Enter with String:')
            if ',' in sti or '.' in sti or '*' in sti or ' ' in sti or '=' in sti:
                print 'Just words or numbers'
            else:
                j = 1


    elif opt == "2" or opt == "4":
        dtg = key + ','
        w = opt + '.' + dtg

    print ('Sending command...')
    s = Serconc('127.0.0.1:14000,127.0.0.1:14001,127.0.0.1:14002')
    print ('OK...')
    if opt == '1':
        x = s.create(key, sti)
        print('Server say: ', x)
    elif opt == '2':
        x = s.retrieve(key)
        print('Server say: ', x)
    elif opt == '3':
        x = s.update(key, sti)
        print('Server say: ', x)
    elif opt == '4':
        x = s.delete(key)
        print('Server say: ', x)



def command():
    while True:
        print ('### Select a option: ###')
        print ('### 1-Create data ###')
        print ('### 2-Retrieve data ###')
        print ('### 3-Update data ###')
        print ('### 4-Delete data ###')
        print ('')
        x = raw_input()
        a = ['1', '2', '3', '4']
        if x in a:
            menu(x)
        else:
            print 'INVALID OPTION'


#def results():
#    while True:
#        print ('Tread 2 - Waiting for results...')
#        msg = s.recv(1400)  # receive response from server
#        lst.append(msg)
#        if not lst:  # sleep thread while any result exist in list lst
#            time.sleep(1)
#        else:
#            print ("Server Result: ", lst.pop())

while True:
    command()

#t1 = threading.Thread(target=command)  # instance new thread
#t2 = threading.Thread(target=results)

#t1.start()  # start thread
#t2.start()
