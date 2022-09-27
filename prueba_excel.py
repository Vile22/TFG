#!/usr/bin/python3

import pandas as pd
import openpyxl
#Hola
df = pd.DataFrame(columns=['Tiempo'])
for i in range(1,16):
    df = df.append({'Tiempo': 4}, ignore_index=True)

df.to_excel('pandas_to_excel.xlsx', sheet_name = 'Nueva hoja')
