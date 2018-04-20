# !/usr/bin/python
# Autor: Alexandre Mariano, Murilo Marques, Guilherme Campos

import socket
import ConfigParser
from threading import Thread
import time
from Queue import Queue

config = ConfigParser.ConfigParser()
config.read("connection.ini")  # reading the config file

host = ''  # I AM THE HOST
port = config.getint('Section one', 'port')  # using the config file values

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # creating a socket object
orig = (host, port)
s.bind(orig)  # bind the host and the port

# num_threads = 20

f = Queue()
d = Queue()
p = Queue()

dty = {}  # empty dictionary


def consumer(stg, clt):
    flg, content = stg.split('.')  # extract the flag and content from string received
    key, value = content.split(',')  # extract the key and the string from content

    if flg == '1':
        if key not in dty:  # add key and value if key don't exist
            dty[key] = value
            s.sendto("Created!!!", clt)
        else:
            s.sendto("Key already exists!!!", clt)  # return case key already exists
    elif flg == '2':
        if key not in dty:  # return case key doesn't exists
            s.sendto("Key don't exist!!!", clt)
        else:
            s.sendto(dty.get(key), clt)  # retrieve and send string case key exist
    elif flg == '3':
        if key not in dty:  # if key doesn't exists, create the key and string
            dty[key] = value
            s.sendto("Not found... New register created!!!", clt)
        else:
            dty[key] = value
            s.sendto("Updated!!!", clt)
    elif flg == '4':
        if key not in dty:  # if key doesn't exists
            s.sendto("Key not found to delete!!!")
        else:
            s.sendto("Deleted: ", clt)
            s.sendto(dty.pop(key), clt)


def receiver(rec, client):
    print ("Received data from: ", client)
    print('Message received: ', rec)
    f.put(rec)  # insert received command in a list
    f.task_done()
    print('Command inserted in Queue')


def worker(cnt):  # client informations (host, port)
    if not f:  # if queue f is empty, sleep thread
        # print('Worker...Waiting...')
        time.sleep(1)
    else:
        print ('Saving in disk')
        temp = f.get()  # Retrieve the command and remove from older queue
        d.put(temp)  # Insert the command in disk log queue
        p.put(temp)  # Insert the command in consumer queue
        # process
        cons = p.get()  # remove from consume queue
        p.task_done()
        consumer(cons, cnt)

        disk_file = open("server.txt", 'a')  # open file for write a command
        value = d.get()
        d.task_done()
        disk_file.writelines(value)  # Write the value in disk
        disk_file.write("\n")
        disk_file.close()  # Close the file
        print('Successful...')


def charge(stg):  # execute the dictionary operations in stg
    flg, content = stg.split('.')  # extract the flag and content from string received
    key, value = content.split(',')  # extract the key and the string from content

    if flg == '1':
        dty[key] = value
    elif flg == '2':
        pass
    elif flg == '3':
        dty[key] = value
    elif flg == '4':
        dty.pop(key)


def retrieveServer():
    try:
        with open('server.txt', 'r') as fil:
            fwn = fil.read().splitlines()
            print 'Retrieve Map from server.txt ...'  # fwn = file without newlines
            for line in fwn:
                charge(line)
            print 'Done!!!'
    except IOError:
        print 'Nothing to retrieve! All looks good!'


# for i in range(num_threads):
retrieveServer()
while True:
    data, cln = s.recvfrom(1400)  # cat rec = map <flag.key, string> client (host, port)
    treceiver = Thread(target=receiver, args=(data, cln))  # thread receiver
    tworker = Thread(target=worker, args=(cln,))  # thread worker
    treceiver.start()
    tworker.start()
    f.join()
    d.join()
    p.join()
