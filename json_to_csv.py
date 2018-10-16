import csv
import json
import pandas as pd

inputFile = open('Test.json', 'r')
outfile = open('sentimentAnalysis.csv', 'w')
print(inputFile)
data = json.load(inputFile)
inputFile.close()

output = csv.writer(outfile)

print(data[0]["reviewerID"])
for row in data:
        values = data[row]
        print(row)