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
### Mean Jump Times
We start by examining the logs of a two-minute run, and discussing the size of the jumps in the values for the logical clocks. We measure these jumps by calculating the mean jump value on a given machine's logical clock. A table of results across five trials is contained below.
Trial | Machine 1 | Machine 2 | Machine 3
------------ | ------------ | ------------ | ------------ 
1 | 2.459 `@2hz` | 3.901 `@1hz` | 1.000 `@5hz`
2 | 1.000 `@2hz` | 1.901 `@1hz` | 1.964 `@1hz`
3 | 3.267 `@1hz` | 1.065 `@4hz` | 1.067 `@4hz`
4 | 1.007 `@6hz` | 2.959 `@2hz` | 1.489 `@4hz`
5 | 1.000 `@4hz` | 3.901 `@1hz` | 1.964 `@2hz`

An interesting observation to be made here is that the mean jump values for a given trial always follow a reverse ordering of that trial's clock speeds. In other words, a faster clock speed means a lower mean jump value. This intuitively makes sense as the machines that update more often are going to dominate most of the message space, meaning that they are effectively getting to set the rules for everybody else.

### Mean Message Queue Lengths
Next we examine the mean message queue lengths. A table of results is included below.
Trial | Machine 1 | Machine 2 | Machine 3
------------ | ------------ | ------------ | ------------ 
1 | 0.233 `@2hz` | 15.265 `@1hz` | 0 `@5hz`
2 | 0.058 `@2hz` | 0.339 `@1hz` | 0.275 `@1hz`
3 | 15.194 `@1hz` | 0.000 `@4hz` | 0.013 `@4hz`
4 | 0.000 `@6hz` | 1.510 `@2hz` | 0.082 `@4hz`
5 | 0.000 `@4hz` | 4.018 `@1hz` | 0.180 `@2hz`

An similar result is found here: a faster clock speed generally implies a lower mean message queue length. This again makes intuitive sense as faster machines will effectively have more processing resources to get through their messages, while slower machines will be stuck processing old messages from the more powerful machines.

### Terminating Drifts
Next we examine the max drift values. This value is calculated by looking at the wall clock and then deriving the wall clock based off the logical clock, and seeing how far off they are at the point of process termination.
Trial | Machine 1 | Machine 2 | Machine 3
------------ | ------------ | ------------ | ------------ 
1 | 162.42 `@2hz` | 324.44 `@1hz` | -2.75 `@5hz`
2 | -1.08 `@2hz` | 100.44 `@1hz` | 107.46 `@1hz`
3 | 253.46 `@1hz` | 5.10 `@4hz` | 5.35 `@4hz`
4 | -2.47 `@6hz` | 218.31 `@2hz` | 52.30 `@4hz`
5 | -2.13 `@4hz` | 324.46 `@1hz` | 106.88 `@2hz`

An similar result is found here: a faster clock speed generally implies a lower terminating drift value. This makes sense, as it again follows the paradigm of the faster clock speed machines "setting the rules" and everyone else playing catch-up. Since the faster clock speed machines are basically the ones always setting the clock, it is intuitive for them to have lower drifts. 

## Analysis with Alterations
Next, we altered our program by decreasing the variation in clock cycles from (1,6) to (1,2) and decreasing the probability that a given event is internal from 7/10 to 1/4. 

### Mean Jump Times
Trial | Machine 1 | Machine 2 | Machine 3
------------ | ------------ | ------------ | ------------ 
1 | 1.125 `@2hz` | 1.125 `@2hz` | 1.120 `@2hz`
2 | 1.901 `@1hz` | 1.000 `@2hz` | 1.910 `@1hz`
3 | 1.125 `@2hz` | 1.125 `@2hz` | 1.125 `@2hz`
4 | 1.107 `@2hz` | 1.111 `@2hz` | 1.589 `@1hz`
5 | 1.107 `@2hz` | 1.107 `@2hz` | 1.625 `@1hz`

### Mean Message Queue Lengths
Trial | Machine 1 | Machine 2 | Machine 3
------------ | ------------ | ------------ | ------------ 
1 | 0.196 `@2hz` | 0.303 `@2hz` | 0.226 `@2hz`
2 | 1.539 `@1hz` | 0 `@2hz` | 4.321 `@1hz`
3 | 0.229 `@2hz` | 0.205 `@2hz` | 0.357 `@2hz`
4 | 0 `@2hz` | 0 `@2hz` | 23.610 `@1hz`
5 | 0.055 `@2hz` | 0.04 `@2hz` | 18.339 `@1hz`

### Terminating Drifts
Trial | Machine 1 | Machine 2 | Machine 3
------------ | ------------ | ------------ | ------------ 
1 | 12.931 `@2hz` | 12.991 `@2hz` | 12.457 `@2hz`
2 | 100.480 `@1hz` | -1.019 `@2hz` | 101.456 `@1hz`
3 | 12.899 `@2hz` | 12.902 `@2hz` | 12.908 `@2hz`
4 | 10.959 `@2hz` | 11.408 `@2hz` | 65.452 `@1hz`
5 | 10.968 `@2hz` | 10.977 `@2hz` | 69.472 `@1hz`

We notice overall, across all three charts, that our numbers are less harsh and more similar within themselves. Mean jump times are all below two, mean message queue remain low, and the terminating drifts aren't nearly as significant.

# Testing
We perform integration tests and unit tests.
### Integration Tests
```bash
python3 integration_tests.py
```
### Unit Tests
```bash
python3 unit_tests.py 
```

# Engineering Notebook
We started by drawing out the theory behind the logical clock on an iPad and then brainstorming a networking stack. We originally considered using HTTP requests 