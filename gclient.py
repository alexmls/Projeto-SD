import ConfigParser
from Queue import Queue
import threading
import time

import grpc
import observer_pb2
import observer_pb2_grpc

config = ConfigParser.ConfigParser()
config.read("connection.ini")  # reading the config file

host = config.get('Section one', 'host')  # using the config file values
gport = config.getint('Section one', 'grpcport')

q = Queue()

channel = grpc.insecure_channel('%s:%s' % (host, gport))  # grpc channel

stub = observer_pb2_grpc.ObserverStub(channel)  # stub for client


def comkeys():
    while True:
        keey = raw_input('Enter with key to monitoring: ')
        q.put(keey)  # put the value in queue
        q.task_done()


def resmon():
    while True:
        if not q:
            time.sleep(1)
        else:
            keyy = q.get()
            response = stub.monitor(observer_pb2.KeyReq(key=keyy))
            temp = response.info

            flg, content = temp.split('.')

            if flg == '1':
                print 'Created Map: ', content
            elif flg == '2':
                print 'Retrieved value for Key', content
            elif flg == '3':
                print 'Updated value for key', content
            elif flg == '4':
                print 'Deleted Map:', content


t1 = threading.Thread(target=comkeys)  # instance new thread
t2 = threading.Thread(target=resmon)

t1.start()  # start thread
t2.start()
