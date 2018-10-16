import json
import pandas as pd

with open('reviews_Health_and_Personal_Care_5.json') as f:
   ## print(json.loads())
    df = pd.DataFrame(json.loads(line) for line in f)
    ## print(df)
    df.to_csv('Output.csv', sep='\t', encoding='utf-8')