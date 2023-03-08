from lamport import *

def test_robustness():
    localHost= "127.0.0.1"
    port1 = 1040
    #initialize processes (1st port argument = machine port. 2nd & 3rd = neighbor ports)
    p1 = Process(target=run_machine, args=(1,localHost, port1, -1, -1, f'unit-log1.csv', True, 0.5, 0))
    #run processes (1 simulated machine/process)
    p1.start()
    #joining processes --> proper shutdown on ctrl+c
    p1.join()

def test_connections():
    #create instance of Machine (initialize server socket)
    localHost= "127.0.0.1"
    port1 = 1050
    m = Machine(1, localHost, port1, True, 0.5)
    m.s.bind((m.HOST, m.PORT))
    m.s.listen()

    #start thread handle_connections
    start_new_thread(handle_connections,  (m, m.HOST, True))

    #initialize client socket
    s2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s2.connect((localHost, port1))

    #test server handle_connections() functionality #send messages from client to server
    counter = 0
    while True:
        time.sleep(m.cycle)
        s2.send(f'msg: {counter}'.encode('utf-8'))
        counter += 1

def test_producer():
    #create instance of Machine (initialize server socket)
    localHost= "127.0.0.1"
    port1 = 1050
    m = Machine(1, localHost, port1, True, 0.5)
    m.s.bind((m.HOST, m.PORT))
    m.s.listen()

    #start thread handle_connections (already tested this functionality in isolation via test_connections() unit test)
    start_new_thread(handle_connections,  (m, m.HOST, False))
    time.sleep(1) #initialization buffer

    #start thread producer (tests client connection successful?)
    producer_thread1 = Thread(target=producer, args=(m, port1, 0))
    producer_thread1.start()

    #send messages from client to server (tests client connection via message queue functionality)
    counter = 0
    while True:
        if not m.q.empty():
            print(m.q.get())
        time.sleep(m.cycle)
        m.connections[0].send(f'msg: {counter}'.encode('utf-8'))
        counter += 1


if __name__ == "__main__":
    try:
        if int(sys.argv[1]) == 0:
            test_robustness()
        if int(sys.argv[1]) == 1:
            test_connections()
        if int(sys.argv[1]) == 2:
            test_producer()
    except:
        print("Incorrect Usage")
