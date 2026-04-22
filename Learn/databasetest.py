import pyodbc

serverString = 'Driver={SQL Server};Server=SJL-5PPPDC2\\TAPE_LOCAL;Database=WATTapplication;Trusted_Connection=yes'

longSqlStatement = '''
SELECT *
FROM tablename
WHERE blah

'''
sqlStatement = "SELECT * FROM WATT.worked"

conn = pyodbc.connect(serverString)
cursor = conn.cursor()
cursor.execute(sqlStatement)

results = []
try: 
    for row in cursor:
        # print('funcDB',len(row))
        results.append(row)
except:
    results = None

print('DB Results',results)

conn.commit()
conn.close()
