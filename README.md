# cs262-dproj2

# Getting Started
*Tested on Python 3.10.10 using MacOS Ventura 13.2.1*
```bash
python3 lamport.py
```
For the time-limited version of the program, first install coreutils.
```bash
brew install coreutils
```
Then run with the timeout utility passing in a parameter.
```bash
gtimeout 2m python3 lamport.py
```
To run our analysis tool, do as follows.
```bash
python3 analysis.py
```

# Analysis
We start by examining the logs of a two-minute run, and discussing the size of the jumps in the values for the logical clocks. We measure these jumps by calculating the mean jump value on a given machine's logical clock. A table of results across five trials is contained below.
Trial | Machine 1 | Machine 2 | Machine 3
------------ | ------------ | ------------ | ------------ 
1 | 2.459 `@2hz` | 3.901 `@1hz` | 1.000 `@5hz`
2 | 1.000 `@2hz` | 1.901 `@1hz` | 1.964 `@1hz`
3 | 3.267 `@1hz` | 1.065 `@4hz` | 1.067 `@4hz`
4 | 1.007 `@6hz` | 2.959 `@2hz` | 1.489 `@4hz`
5 | 1.000 `@4hz` | 3.901 `@1hz` | 1.964 `@2hz`

An interesting observation to be made here is that the mean jump values for a given trial always follow a reverse ordering of that trial's clock speeds. In other words, a faster clock speed means a lower mean jump value. This intuitively makes sense as the machines that update more often are going to dominate most of the message space, meaning that they are effectively getting to set the rules for everybody else.

Next we examine the mean message queue lengths. A table of results is included below.
Trial | Machine 1 | Machine 2 | Machine 3
------------ | ------------ | ------------ | ------------ 
1 | 0.233 `@2hz` | 15.265 `@1hz` | 0 `@5hz`
2 | 0.058 `@2hz` | 0.339 `@1hz` | 0.275 `@1hz`
3 | 15.194 `@1hz` | 0.000 `@4hz` | 0.013 `@4hz`
4 | 0.000 `@6hz` | 1.510 `@2hz` | 0.082 `@4hz`
5 | 0.000 `@4hz` | 4.018 `@1hz` | 0.180 `@2hz`

An similar result is found here: a faster clock speed generally implies a lower mean message queue length. This again makes intuitive sense as faster machines will effectively have more processing resources to get through their messages, while slower machines will be stuck processing old messages from the more powerful machines.

# Testing
We perform unit tests and integration tests, as specified in the problem statement.

### Unit Tests
```bash
python3 unit_tests.py <f>
```

f = 0 triggers test_robustness()
f = 1 triggers test_connections()
f = 2 triggers test_producer()

**Robustness Test**
We replace 1-10 dice roll executions with 1-10 cyclical executions.

No terminal output.

Spot check log output for cyclical execution instructions, lamport clock jumps=1. 

There are no messages sent or received. This test evaluates the boilerplate of run_machine(). 

**Connections Test**
We replace 1-10 dice roll executions with 1-10 cyclical executions.

Terminal output should match the following pattern exactly:

(Debug) received:  msg: 0
(Debug) received:  msg: 1
(Debug) received:  msg: 2
(Debug) received:  msg: 3

No log output.

Allows us to test handle_connections() functionality in isolation. We set up a testing server/client and call handle_connections(). Tests 1) server handling of client connection and 2) server handling of messages. 

**Producer Test**
We replace 1-10 dice roll executions with 1-10 cyclical executions.

Terminal output should match the following pattern exactly:

Client-side(1)connection success to port val: 1050 
msg: 0
msg: 1
msg: 2
msg: 3

No log output.

Allows us to test producer() functionality. We set up a testing server/client and call handle_connections() and producer() (recall handle_connections() was already tested in isolation). Tests 1) client connection and 2) client-side message queue functionality.

### Integration Tests
```bash
python3 integration_tests.py <f>
```

 f = 0 triggers test_robustness()
 f = 1 triggers test_robustness_hardcoded()

**Robustness Test**
We replace 1-10 dice roll executions with 1-10 cyclical executions.

Spot check terminal output for either alternating messages, sent by process 1 and process 2, or messages sent only by process 1 or process 2. Command execution is cyclical, so the system should get stuck in one of these two patterns, depending on arbitrary order of executions in thread initialization.

local time, sent by:  2, 1
local time, sent by:  2, 2
local time, sent by:  10, 1
local time, sent by:  10, 2
local time, sent by:  12, 2
local time, sent by:  12, 1

OR 

local time, sent by:  2, 1
local time, sent by:  10, 1
local time, sent by:  12, 1
local time, sent by:  20, 1

Spot check log for cyclical execution instructions, lamport clock jumps = 1.

Note: Pattern 2 will reset to Pattern 1, given enough time. 

Simplifies distributed system interaction, allows human verification and step through of message send/receive interaction.

**Robustness Test Hardcoded**
We replace 1-10 dice roll executions with 1-10 cyclical executions.
We limit process 1 to executing internal instructions and receiving messages
$\implies$ only process 2 can send messages

Terminal output should match integration_hardcoded.txt exactly, up till end of file.

Spot check log for cyclical execution instructions, lamport clock jumps = 1.

Allows us to rigorously determine that our Lamport Clock equations are implemented as specified.

# Discussion
#drawback of our design: n machines --> 3n^2 sockets

#tf design had producer and consumer threads (good modular design), and a global variable (we scrap this)

#seems uncouth to model a distributed system w a global variable?