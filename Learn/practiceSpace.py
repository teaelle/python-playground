import time
import os
import csv
import math
import pyodbc
import fnmatch
from datetime import date, datetime, timedelta
# import datetime
# os.getenv('COMPUTERNAME')


def queryDatabase(sqlStatement):
    serverString =  'Driver={SQL Server};Server=' + os.getenv('COMPUTERNAME') + '\\SQLEXPRESS;Database=WATTapplication;Trusted_Connection=yes;'
    print('executing',sqlStatement)
    global conn
    conn = pyodbc.connect(serverString)
    cursor = conn.cursor()
    cursor.execute(sqlStatement)
    results = []
    try: 
        for row in cursor:
            print('funcDB',len(row))
            results.append(row)
        print('funcDB',row)
    except:
        results = None
    print('funcDB.',results)
    conn.commit()
    conn.close()
    return results

def getTaskTypeList():
    # get list of task types for combo box
    global taskTypes
    taskTypes = queryDatabase("SELECT taskTypeId, taskTypeName FROM watt.taskType")
    print(taskTypes)
    taskTypesDict = dict(taskTypes)
    taskTypes = []
    for value in taskTypesDict.values():
        taskTypes.append(value)
    print(taskTypesDict)
    print(taskTypes)
    # taskListCombo['values']= taskTypes
    # taskListCombo.current(0)

def getColorsStuff():
    sqlStatement = 'SELECT workedItemId,taskTypeHexColor AS lastEntry FROM watt.worked INNER JOIN watt.tasktype ON worked.taskTypeId = taskType.taskTypeId WHERE workedItemId = (SELECT MAX(workedItemId) AS lastEntry FROM watt.worked)'
    results = queryDatabase(sqlStatement)
    print(results)
    try: 
        print('test2a',results[0][0])
        print('test3a',results[0][1])
    except:
        print('old query do not work')

def main():
    # getTaskTypeList()
    PASSWORDS = {
        "email" : "hello@gmail.com",
        "thing" : "valuething"
    }

    valuegetting = PASSWORDS['email']

    print(valuegetting)
    # getColorsStuff()
    dataSetCollection = ['Hello','Hi','There']
    errorTest = ['ZipCode "27004" was not found in the database.']
    error = 'Tamilyn'
    if error in dataSetCollection:
        print("found")
    else:
        print("not found")
        dataSetCollection.insert(len(dataSetCollection), error)
        print(dataSetCollection)
    filtered = fnmatch.filter(dataSetCollection, 'He*o')
    print(filtered)
    checking = fnmatch.filter(errorTest, 'ZipCode "?????" was not found in the database.')[0]
    print(checking)

    if fnmatch.filter(errorTest, 'ZipCode "?????" was not found in the database.')[0] in errorTest:
        print('continue on')

    if errorTest == checking:
        print('matching')


def testMyIf():
    filenamevalue = 'help'

    if "kk" not in filenamevalue:
        print('Ingore Name Of:') # DEBUG
        
    timestemp = str(datetime.datetime.today())[11:19]
    # str(datetime.today())[11:19]
    print(timestemp)

def learnStrings():
    myString = 'Hello Tamilyn How Are You Today'
    left = -5 # trims this many from the left
    right = None # goes this from from the left
    print(left,right)
    print(myString[left:right])

def inputToList():
    inputString = input('Enter 9 Digit SSN to Search: ')
    mySearchList = inputString.split(",")
    print(mySearchList)
    for x in mySearchList:
        print(x)

def printingLoop():
    results = [['336245609 DOD FOUND: 20130227 on 20130411.txt'],['529409871 DOD FOUND: 20190316 on 20190411.txt'],['531366868 DOD FOUND: 20180206 on 20180321.txt'],['421623250 DOD FOUND: 20190606 on 20190625.txt']]

    # print to CSV
    username = os.getlogin()
    reportOutputLocation = '\\\\secureshare\\Encrypted Share\\Delivery Management\\ETL Load Checklists\\In Progress\\Tamilyn Peck\\Tools and Testing\\ReportOutput' # TESTING LOCATION
    reportName = "CENTSsnSearch_" + str(datetime.today())[:19].replace(':','') + username + ".csv"
    reportOutputFilePathName = os.path.join(reportOutputLocation, reportName)
    # Open File to Write
    with open(reportOutputFilePathName, 'w', newline='') as reportFile:
        thewriter = csv.writer(reportFile)

        # Loop Through Results List and Write to CSV
        for dateSet in range(0,len(results)):
            thewriter.writerow(results[dateSet])
            # print(dataSetByDate[dateSet]) # DEBUG
    print('results in ReportOutput')

def findStringList():
    sflCodeList = ['LABC','FARM','MDLZ','LIBM','KRFT','WTW0','CHEV','COKE','BAKK']
    fileName = 'lkjdfLABCel2019'
    for x in sflCodeList:
        if x in fileName:
            print("Match Found")
            break # just breaks the for loop
        else:
            print("No Match")
    print("which level")

if __name__ == "__main__":
    # printingLoop()
    today = str(date.today() - timedelta(days=1))
    print(today)
    findStringList()