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
We perform integration tests and unit tests.

### Integration Tests
```bash
python3 integration_tests.py <f>
```

 f = 0 triggers test_robustness()
 f = 1 triggers test_robustness_hardcoded()

### Unit Tests
```bash
python3 unit_tests.py <f>
```

f = 0 triggers test_robustness()
f = 1 triggers test_connections()
f = 2 triggers test_producer()

**Robustness Test**

**Connections Test**

**Producer Test**

