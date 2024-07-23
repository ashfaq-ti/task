import pandas as pd

df = pd.read_csv('result.csv')

print(len(df.iloc[21,0]))