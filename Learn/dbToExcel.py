import openpyxl
import pyodbc
import win32com
import datetime
import pandas

# serverString = 'Driver={SQL Server};Server=SJL-3H1J9H2\\DAVSMI_LOCAL;Database=MaryKay;Trusted_Connection=yes'
serverString = 'Driver={SQL Server};Server=SJL-5PPPDC2\\TAPE_LOCAL;Database=WATTapplication;Trusted_Connection=yes'
conn = pyodbc.connect(serverString)
cursor = conn.cursor()
getDate = datetime.datetime.now()

# sqlFile = 'C:\\dev\\SQL Files\\CustomerPull.sql'
sqlFile = r'C:\git\repo\Python\simpleQuery.sql'
with open(sqlFile) as sq:
    queryRead = sq.read()
    # print(queryRead)

cursor.execute(queryRead)
results = []

try:
    for row in cursor:
        results.append(row)
        # print(row)
except: 
    results = None

data = results
df = pandas.DataFrame(data)
print('df: ',df)

df.to_excel("sample.xlsx")

wb = openpyxl.Workbook()
sheet = wb.active
sheet.title = 'CustomerPull' 

# print (results)



try:
    for row in results:
        sheet.append(row)
        print(row)
except: 
    print('ecountered error')



wb.save('sample_' + getDate.strftime("%Y-%m-%d_%H-%M-%S") + '.xlsx')


conn.commit()
conn.close()

# print('DB Results',results)