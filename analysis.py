import csv
from pandas import *
from statistics import mean 

"""
Process log files --> statistics
"""

#load 5 trials
for t in range(1, 6):
    #load 3 log files ("machines")/trial
    for l in range (1, 4):
        file_name = f't{t}-log{l}.csv' #read log file
        data = read_csv(file_name)
        logical_clock_time = data['Logical Clock Time'].tolist() #csv column --> list
        global_time = data['Global Time'].tolist() #csv column --> list
        message_queue_length = [i for i in data['Message Queue Length'].tolist() if i != -1] #csv column --> list

        logical_clock_jump = []
        #calculate logical_clock_jump statistic
        for i in range(1, len(logical_clock_time)):
            logical_clock_jump.append(logical_clock_time[i]-logical_clock_time[i-1])

        #output statistics to file_name
        with open(file_name, newline='') as f:
            reader = csv.reader(f)
            row1 = next(reader)
            adjusted_max_global_time = global_time[-1] - global_time[0]
            drift = adjusted_max_global_time - logical_clock_time[-1]/float(row1[6]) + logical_clock_time[0]/float(row1[6])
            #write row: mean logical clock jump, mean message queue length, drift
            print(f'{file_name}@{row1[6]}hz mLCP = {mean(logical_clock_jump)} mMQL = {mean(message_queue_length)} drift = {-drift}')