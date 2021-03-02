import csv

# init empty list
device_list=[]

# open csv file and reading it
with open('ipaddresses.csv', newline='') as csvfile:
    ipreader = csv.reader(csvfile, delimiter=',')
    # append read entries into list
    for row in ipreader:
        device_list.append(row)

# read list out
for device in device_list:
    print(device[2])