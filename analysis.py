import csv
from pandas import *
from statistics import mean 

"""
Process log files --> Statistics (mean logical clock jump, mean message queue length)
"""

#read 5 system trials
for t in range(1, 6):
    #read 3 machine logs / trial
    for l in range (1, 4):
        file_name = f't{t}-log{l}.csv'
        data = read_csv(file_name) #read log file
        logical_clock_time = data['Logical Clock Time'].tolist() #convert "logical clock time" column to list
        message_queue_length = [i for i in data['Message Queue Length'].tolist() if i != -1] #convert "message queue length" column to list

        logical_clock_jump = []
        #construct logical_clock_jump statistic
        for i in range(1, len(logical_clock_time)):
            logical_clock_jump.append(logical_clock_time[i]-logical_clock_time[i-1])

        with open(file_name, newline='') as f:
            reader = csv.reader(f)
            row1 = next(reader)
            #write row: mean logical clock jump, mean message queue length, drift
            print(f'{file_name}@{row1[6]}hz mLCP = {mean(logical_clock_jump)} mMQL = {mean(message_queue_length)}')