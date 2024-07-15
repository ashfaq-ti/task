# import pandas as pd
# dict = {
#     'a' : [1],
#     'b' : [4]
# }
# df = pd.DataFrame(dict)
# print(df)
# df.to_csv('file.csv')
import csv
with open('file.txt','w+') as file:
    file.write('hello\n')
    file.seek(0)
    line = file.read()
    s = 'world'
    file.write(f'{s}\n')
print(line)

with open('file1.txt','w+') as file:
    pass


