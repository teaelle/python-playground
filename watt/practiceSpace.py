import time
import os
import math
import pyodbc
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
    # getColorsStuff()
    dataSetCollection = ['Hello','Hi','There']
    error = 'Tamilyn'
    if error in dataSetCollection:
        print("found")
    else:
        print("not found")
        dataSetCollection.insert(len(dataSetCollection), error)
        print(dataSetCollection)



if __name__ == "__main__":
    main()