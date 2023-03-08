from multiprocessing import Process #Machine/process instead of machine/thread. There exist fundamental differences between processes and threads (ex shared memory). Under machine/process we eliminate the "this is kosher" reasoning we'd need under machine/thread.
import queue
import csv
import random
import time
import sys

import socket
import threading
from _thread import *
from threading import Thread

#drawback of this design choice (ie the choice to build on top of sockets): 3n^2 sockets for n machines (to construct a connected graph)

#an alteration from tf's design: having a producer and consumer thread is good, modular design, but the idea of a global variable isn't sitting right with me. seems like it defies the purpose of this exercise

class Machine:
    def __init__(self, id_code, host, port):
        self.id = id_code
        self.cycle = 1/random.randint(1,6)
        self.q = queue.Queue() #thread safe in python
        self.HOST = host
        self.PORT = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.connections = {} #dictionaries are thread safe in python
        self.clock = 0

def producer(m, portVal, port_id):
    #code from TF example
    host= "127.0.0.1"
    port = int(portVal)
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        s.connect((host,port))
        m.connections[port_id] = s #no lock needed, as each producer thread in a process gets passed a different port id
        print(f"Client-side({m.id})connection success to port val: {portVal} \n")
    except:
        #print exception?
        pass
    return

def consumer(conn, m):
    while True:
        msg = conn.recv(1024).decode("utf-8")
        if msg:
            m.q.put(msg)

def handle_connections(m, host):
    while True:
        conn, addr = m.s.accept()
        start_new_thread(consumer, (conn, m))


def run_machine(id_code, host, port, port1, port2, fname):
    m = Machine(id_code, host, port)
    m.s.bind((m.HOST, m.PORT))
    m.s.listen()
    connections_thread = Thread(target=handle_connections, args=(m, host)) #create the thread to handle connections to the client (blocking calls)
    connections_thread.start()
    print(f"Starting up Machine {id_code}, with instruction cycle {1/m.cycle}")
    time.sleep(3) #buffer for startup completion on all machines
    #producer threads
    producer_thread1 = Thread(target=producer, args=(m, port1, 0))
    producer_thread1.start()
    producer_thread2 = Thread(target=producer, args=(m, port2, 1))
    producer_thread2.start()
    time.sleep(3) #buffer for network connection on all machines

    log_file = open(fname, 'w')
    writer = csv.writer(log_file)
    writer.writerow(["Write Type", "Global Time", "Logical Clock Time", "Message", "Message Queue Length", "Sender", f'{1/m.cycle}']) #all fields = -1 when not logical or not relevant
    while True:
        log_file.flush()
        time.sleep(m.cycle)
        if not m.q.empty(): 
            msg = m.q.get() #kosher because only this process has access to this queue
            m.clock = max(m.clock, int(msg.split(",")[0]))+1
            print('local time, sent by: ', msg)
            writer.writerow([0, time.time(), m.clock, msg, m.q.qsize(), int(msg.split(",")[1])]) #included message received
            continue
        exc = random.randint(1,10)
        m.clock+=1
        if (exc > 3):
            writer.writerow([exc, time.time(), m.clock, -1, -1, -1])
            continue
        if exc==1 or exc==3:
            m.connections[0].send(f'{m.clock}, {m.id}'.encode('utf-8'))
        if exc==2 or exc==3:
            m.connections[1].send(f'{m.clock}, {m.id}'.encode('utf-8'))
        writer.writerow([exc, time.time(), m.clock, f'{m.clock}, {m.id}', -1, -1]) #added field m.id to spec


if __name__ == '__main__':
    localHost= "127.0.0.1"

    port1 = 2060
    port2 = 2061
    port3 = 2062

    for x in range(1, 6):

        port1 += 3*x
        port2 += 3*x
        port3 += 3*x

        p1 = Process(target=run_machine, args=(1,localHost, port1, port2, port3, f't{x}-log1.csv'))
        p2 = Process(target=run_machine, args=(2,localHost, port2, port3, port1, f't{x}-log2.csv'))
        p3 = Process(target=run_machine, args=(3,localHost, port3, port1, port2, f't{x}-log3.csv'))

        p1.start()
        p2.start()
        p3.start()
