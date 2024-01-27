import csv

csv_file_path = 'CAV_data.csv'
output_csv_path = 'processed_CAV_data.csv'

plotInterval = 0.5 # time between plots, in seconds

rawData = []
with open(csv_file_path, 'r') as rawFile:
    csv_reader = csv.reader(rawFile)
    for row in csv_reader:
        rawData.append(row)

# Display the list
#print(rawData)
        
stepsPerSecond = int(1/(float(rawData[2][0]) - float(rawData[1][0])))
num = int(plotInterval * stepsPerSecond)

newData = []
counter = 0

for row in rawData:
    if (counter == 0):
        newData.append(row)
    if ((counter-1) % num) == 0:
        newData.append(row)
    counter += 1

with open(output_csv_path, 'w', newline='') as processedFile:
    csv_writer = csv.writer(processedFile)
    csv_writer.writerows(newData)