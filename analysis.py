import csv
from pandas import *
from statistics import mean 

for t in range(1, 6):
    for l in range (1, 4):
        file_name = f't{t}-log{l}.csv'
        data = read_csv(file_name)
        logical_clock_time = data['Logical Clock Time'].tolist()
        message_queue_length = [i for i in data['Message Queue Length'].tolist() if i != -1]
        logical_clock_jump = []
        for i in range(1, len(logical_clock_time)):
            logical_clock_jump.append(logical_clock_time[i]-logical_clock_time[i-1])
        with open(file_name, newline='') as f:
            reader = csv.reader(f)
            row1 = next(reader)
            print(f'{file_name}@{row1[6]}hz mLCP = {mean(logical_clock_jump)} mMQL = {mean(message_queue_length)}')