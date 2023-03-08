from multiprocessing import Process
import queue
import csv
import random
import time
import sys

import socket
import threading
from _thread import *
from threading import Thread

"""
Run a simulated distributed system with three "machines" (1 Machine object/process). 
    Update local clock time on each Machine event
    Log local clock times, for analysis and testing
"""

class Machine:
    def __init__(self, id_code, host, port, debug=False, c=-1):
        self.id = id_code
        self.cycle = 1/random.randint(1,6)
        if debug: 
            self.cycle = c
        self.q = queue.Queue() #thread safe in python
        self.HOST = host
        self.PORT = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.connections = {} #thread safe in python
        self.clock = 0

def producer(m, portVal, port_id):
    #code from TF example
    host= "127.0.0.1"
    port = int(portVal)
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    try:
        #connect socket to localHost, portVal
        s.connect((host,port)) #blocking
        #store socket (we'll send messages to this socket in the future)
        m.connections[port_id] = s #no concurrency issues, as port_id is unique for both producer threads in a process
        print(f"Client-side({m.id})connection success to port val: {portVal} \n")
    except:
        pass
    return

def consumer(conn, m, debug=False):
    #listens for messages
    while True:
        msg = conn.recv(1024).decode("utf-8") #blocking
        if msg:
            m.q.put(msg)
            if debug: 
                print("(Debug) received: ", msg)

def handle_connections(m, host, debug=False):
    #listens for connections
    while True:
        conn, addr = m.s.accept() #blocking
        start_new_thread(consumer, (conn, m, debug))

def exec_instruction(m, writer, debug=False, n=2, counter=-1, hardcoded=-1):
    exc = random.randint(1,10) #generate instruction for this cycle
    if debug:
        exc = (counter % 10) + 1
    m.clock+=1
    if (exc > 3) or (debug and n == 0) or (debug and n == 1 and exc == 2) or hardcoded==0:
        #internal event
        writer.writerow([exc, time.time(), m.clock, -1, -1, -1])
        return
    if (n > 0 or (not debug)) and (exc==1 or exc==3):
        #send message to neighbor 1
        m.connections[0].send(f'{m.clock}, {m.id}'.encode('utf-8')) 
    if (n > 1 or (not debug)) and (exc==2 or exc==3):
        #send message to neighbor 2
        m.connections[1].send(f'{m.clock}, {m.id}'.encode('utf-8'))
    writer.writerow([exc, time.time(), m.clock, f'{m.clock}, {m.id}', -1, -1]) #addition to spec: m.id
    

def run_machine(id_code, host, port, port1, port2, fname, debug=False, c=-1, neighbors=2, hardcoded=-1):
    if debug: 
        m = Machine(id_code, host, port, debug, c) #init machine data structure, w preset cycle
    else: 
        m = Machine(id_code, host, port) #init machine data structure

    m.s.bind((m.HOST, m.PORT))
    m.s.listen()
    connections_thread = Thread(target=handle_connections, args=(m, host)) #accept connections to this machine, and listen for messages
    connections_thread.start()
    print(f"Starting up Machine {id_code}, with instruction cycle {1/m.cycle}")
    time.sleep(3) #buffer for startup completion on all machines

    #producer threads initialize connections to the machines at port1, port2
    if neighbors > 0 or (not debug):
        producer_thread1 = Thread(target=producer, args=(m, port1, 0))
        producer_thread1.start()
    if neighbors > 1 or (not debug):
        producer_thread2 = Thread(target=producer, args=(m, port2, 1))
        producer_thread2.start()
    time.sleep(3) #buffer for network connection on all machines

    log_file = open(fname, 'w')
    writer = csv.writer(log_file) #open log file for machine m
    writer.writerow(["Write Type", "Global Time", "Logical Clock Time", "Message", "Message Queue Length", "Sender", f'{1/m.cycle}']) #all fields = -1 when not logical or not relevant

    debug_counter = 0
    while True:
        log_file.flush() #flushes internal buffer
        time.sleep(m.cycle) #sleep for one machine cycle
        debug_counter += 1
        if not m.q.empty(): 
            msg = m.q.get() #queues are machine/process specific, prevents concurrency issues
            m.clock = max(m.clock, int(msg.split(",")[0]))+1 #update logical clock time via lamport's formula
            print('local time, sent by: ', msg)
            writer.writerow([0, time.time(), m.clock, msg, m.q.qsize(), int(msg.split(",")[1])]) #addition to spec: msg
            continue
        if not debug:
            exec_instruction(m, writer)
        else:
            exec_instruction(m, writer, debug, neighbors, debug_counter, hardcoded)


if __name__ == '__main__':
    localHost= "127.0.0.1"

    port1 = 2060
    port2 = 2061
    port3 = 2062

    #run 5 system trials
    for x in range(1, 6):

        #each system trial runs on a different set of ports
        port1 += 3*x
        port2 += 3*x
        port3 += 3*x

        #initialize processes (1st port argument = machine port. 2nd & 3rd = neighbor ports)
        p1 = Process(target=run_machine, args=(1,localHost, port1, port2, port3, f't{x}-log1.csv'))
        p2 = Process(target=run_machine, args=(2,localHost, port2, port3, port1, f't{x}-log2.csv'))
        p3 = Process(target=run_machine, args=(3,localHost, port3, port1, port2, f't{x}-log3.csv'))

        #run processes (1 simulated machine/process)
        p1.start()
        p2.start()
        p3.start()
