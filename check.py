import pandas as pd

df = pd.read_csv('uuid_url.csv')

df.set_index('uuid',inplace=True)

print(df.loc['1488bfc2-8812-4da4-8b88-345f2401546c'])