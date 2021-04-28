import pandas as pd 

xls = pd.ExcelFile('large.xlsx')
df1 = pd.read_excel(xls, 'w')
df2 = pd.read_excel(xls, 'c')
df3 = pd.read_excel(xls, 'f')


print(df1)
print(df2)
print(df3)