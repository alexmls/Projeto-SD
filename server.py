# !/usr/bin/python
# Autor: Alexandre Mariano, Murilo Marques, Guilherme Campos

import socket
import ConfigParser
from threading import Thread
import time
from Queue import Queue
import grpc
from concurrent import futures
import observer_pb2
import observer_pb2_grpc

config = ConfigParser.ConfigParser()
config.read("connection.ini")  # reading the config file

host = ''  # I AM THE HOST
port = config.getint('Section one', 'port')  # using the config file values
gport = config.getint('Section one', 'grpcport')  # cat the gRPC Port
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # creating a socket object
orig = (host, port)
s.bind(orig)  # bind the host and the port

# num_threads = 20

f = Queue()  # Queue for receive commands
d = Queue()  # Queue for log in disk
p = Queue()  # Queue for consume commands
g = Queue()  # Queue for gRPC

dty = {}  # empty dictionary


def monit(kvalue):
    if not g:  # if queue f is empty, sleep thread
        # print('Worker...Waiting...')
        time.sleep(1)
    else:
        val = g.get()  # retrieve new Queue element to monitore
        f.put(val)  # put the elemente in Queue to process
        f.task_done()
        f.join()
        if kvalue in val:
            return val
        else:
            return 'Key doesent exist!!!'


class ObserverService(observer_pb2_grpc.ObserverServicer):

    def monitor(self, request, context):
        i = 0
        while i != 1:
            temp = request.key
            if ' ' in temp:
                stp, ky = temp.split(' ')
                if stp == 'stop':
                    i = 1
            else:
                response = observer_pb2.InfoRep()
                response.info = monit(request.key)
                return response




def grpcTh():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    observer_pb2_grpc.add_ObserverServicer_to_server(ObserverService(), server)

    print('Starting gRPC Thread. Listen on port ', gport)
    server.add_insecure_port('[::]:%s' % gport)
    server.start()

    try:  # loop to keep alive
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


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
            s.sendto("Key dont exist!!!", clt)
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
            s.sendto("Key not found to delete!!!", clt)
        else:
            s.sendto("Deleted: ", clt)
            s.sendto(dty.pop(key), clt)


def receiver(rec, client):
    print ("Received data from: ", client)
    print('Message received: ', rec)
    g.put(rec)  # insert received command in a list
    g.task_done()
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
    tgrpc = Thread(target=grpcTh)  # gRPC thread
    treceiver.start()
    tworker.start()
    tgrpc.start()
    g.join()
    d.join()
    p.join()
