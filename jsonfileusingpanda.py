import json
import pandas as pd

with open('reviews_Health_and_Personal_Care.json') as f:
   # print(json.loads())
    df = pd.DataFrame(json.loads(line) for line in f)
    # print(df)
    df.to_csv('Output_large.csv', sep='\t', encoding='utf-8')