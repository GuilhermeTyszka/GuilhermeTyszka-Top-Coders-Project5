from sqlalchemy import create_engine, text
import csv

db_url = "mssql+pymssql://localhost:58787/db_lufalufa"
engine = create_engine(db_url, pool_size=5, pool_recycle=3600)

import csv
with open('nomes.csv') as file:
    planilha = list(csv.reader(file, delimiter=','))

string_final = ''
for elemento in planilha:
    string = '('
    for elementos in elemento:
        string = string + "'" + elementos + "'"
    string = (string + ')').replace(';','\',\'')
    string_final = string_final + ',' + string

string_final = string_final[1::]

conn = engine.connect()
sql_text = text(f'INSERT INTO dbo.Alunos VALUES {string_final}')
result = conn.execute(sql_text)
