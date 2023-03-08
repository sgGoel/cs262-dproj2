from lamport import *

def test_robustness():
    localHost= "127.0.0.1"
    port1 = 1090
    port2 = 1091

    #initialize processes (1st port argument = machine port. 2nd & 3rd = neighbor ports)
    p1 = Process(target=run_machine, args=(1,localHost, port1, port2, -1, f'integration-log1.csv', True, 0.5, 1))
    p2 = Process(target=run_machine, args=(2,localHost, port2, port1, -1, f'integration-log2.csv', True, 0.5, 1))

    #run processes (1 simulated machine/process)
    p1.start()
    p2.start()

    #joining processes --> proper shutdown on ctrl+c
    p1.join()
    p2.join()


#hardcoded behavior! compare terminal output to integration_hardcoded.txt
def test_robustness_hardcoded():
    localHost= "127.0.0.1"
    port1 = 1090
    port2 = 1091

    #initialize processes (1st port argument = machine port. 2nd & 3rd = neighbor ports)
    p1 = Process(target=run_machine, args=(1,localHost, port1, port2, -1, f'integration-log1.csv', True, 0.5, 1, 0))
    p2 = Process(target=run_machine, args=(2,localHost, port2, port1, -1, f'integration-log2.csv', True, 0.5, 1, 1))

    #run processes (1 simulated machine/process)
    p1.start()
    p2.start()

    #joining processes --> proper shutdown on ctrl+c
    p1.join()
    p2.join()


if __name__ == "__main__":
    try:
        if int(sys.argv[1]) == 0:
            test_robustness()
        if int(sys.argv[1]) == 1:
            test_robustness_hardcoded()
    except:
        print("Incorrect Usage")