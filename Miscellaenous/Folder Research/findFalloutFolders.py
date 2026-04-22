import csv
import os
import os.path, time
import fnmatch
from datetime import date
from datetime import datetime


def main():

    folderLocation = r'\\secureshare\Encrypted Share\Data Incidents\Fallout Records'

    # Set Date Range for Review
    ignoreYears = ['2013','2014','2015','2016','2017']
    # latestFileCreateDateToReview = str(datetime.today())

    # Initialize Variables
    # clientCodeList = ['LABC','FARM','MDLZ','LIBM','KRFT','WTW0','CHEV','COKE','BAKK']
    dataSetCollection = [['ClientFolder','FolderYear','FolderMonth','CompletedFound','SentFound','FilePath']]
    completed_found = 0
    sent_found = 0
    ignorePath = 0
    
    # Loop Through Directory & Folders in Directory
    print("Starting Review...",str(datetime.today())[11:19])
    for path, subdir, files in os.walk(folderLocation):
        
        ignorePath = 0
        for x in ignoreYears:
            if x in path:
                ignorePath = 1
                # print("ingore path",path)
                break
        if ignorePath == 1:
            continue
        
        # print('Reviewing Folders in...',path)
        try:
            if path.split("\\")[-1].upper() == 'COMPLETED' or  path.split("\\")[-1].upper() == 'COMPLETE':
                completed_found = 1
                # upperFolder = UPPER(subdir[0][:4])
                if subdir[0][:4].upper() == 'SENT' or subdir[0][:4].upper() == 'SEND':    
                    # print('found sent in',path)
                    sent_found = 1
                    # print(subdir)
                    # pathSections = [path[61:].split("\\")
                dataSetCollection.append([path[61:].split("\\")[0] , path[61:].split("\\")[1] , path[61:].split("\\")[2] , completed_found,sent_found,path])
        except:
            pass

        completed_found = 0
        sent_found = 0
        # if len(dataSetCollection) > 2000:
        #       # print(dataSetCollection)
                # return dataSetCollection
    
    return dataSetCollection


def printResults(dataSetCollection):
    reportOutputLocation = r'X:\Learning Files\Python'
    # print("Results:") # DEBUG
    print('Review Complete: Outputing Results File',str(datetime.today())[11:19])
    # Output CSV File with Results 
    # Determine File Name
    username = os.getlogin()
    reportName = "FindFolders_" + str(datetime.today())[:19].replace(':','') + username + ".csv"
    reportOutputFilePathName = os.path.join(reportOutputLocation, reportName)

    if dataSetCollection is None:
        print('No Results')
        return
    else:

        # Open File to Write
        with open(reportOutputFilePathName, 'w', newline='') as reportFile:
            thewriter = csv.writer(reportFile)

            # Loop Through Results List and Write to CSV
            for dateSet in range(0,len(dataSetCollection)):
                # print(dataSetCollection[dateSet])
                thewriter.writerow(dataSetCollection[dateSet])
                # print(dataSetByDate[dateSet]) # DEBUG


        print('File Output Complete',str(datetime.today())[11:19])

if __name__ == "__main__":
    data = main()
    print(len(data))
    # print(data)
    if len(data) > 1:
        printResults(data)