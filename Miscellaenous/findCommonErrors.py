import csv
import os
import os.path, time
from datetime import date
from datetime import datetime


def main():

    folderLocation = r'\\TPECK\Shared Drive\Python Data Testing\Generated Sample Data'
    

    # Set Date Range for Review
    earliestFileCreationDateToReview = '2019-01-01' # TESTING DATE RANGE
    latestFileCreateDateToReview = str(datetime.today())

    # Initialize Variables
    dateOfFileCreation = ''
    sizeOfFile = 0
    dataSetCollection = [['ErrorMessage']]

    
    # Loop Through Directory & Folders in Directory
    for path, subdir, files in os.walk(folderLocation):

        print('Reviewing Files...')

        for file in files:
            loaderFile = os.path.join(path,file)
            if len(dataSetCollection) > 5:
                    print(dataSetCollection)
                    return dataSetCollection
            #Only Review if '.csv' (ignore folders, any random files)
            if not '.csv' in loaderFile:
                # print('Ingore Type Of:', file) # DEBUG
                continue

            try:
                dateOfFileCreation = str(datetime.fromtimestamp(os.path.getctime(loaderFile)))[:10]
                sizeOfFile = os.path.getsize(loaderFile)
            except:
                print('error getting properties of (',os.path.basename(loaderFile)[:50],')')
                print('Review previous manually. Continuing review..')
                # continue

            # Don't Review Certain Date Ranges 
            if dateOfFileCreation < earliestFileCreationDateToReview:
                # print('Ingore Date Of:', file) # DEBUG
                continue
            if dateOfFileCreation > latestFileCreateDateToReview:
                # print('Ingore Date Of:', file) # DEBUG
                continue

            # Don't Review Empty Files
            if sizeOfFile == 0:
                # print('Ingore empty file: (',os.path.basename(loaderFile)[:50],')')
                continue

            # Open and Read File
            with open(loaderFile, 'r', newline='') as csv_file:
                csv_reader= csv.reader(csv_file)

                # Loop Through Each Row on the File
                for line in csv_reader:
                    error = line[2]
                    # if err not like SSN in use
                    if "SSN " in error: 
                        continue
                    # if error not like.. 
                    # format error 

                    if [error] in dataSetCollection:
                        continue
                    else:
                        dataSetCollection.insert(len(dataSetCollection), [error])

    


def printResults(dataSetCollection):
    reportOutputLocation = r'\\TPECK\Shared Drive\Python Data Testing'
    # print("Results:") # DEBUG
    print('Review Complete: Outputing Results File')
    # Output CSV File with Results 
    # Determine File Name
    username = os.getlogin()
    reportName = "ErrorCollection_" + str(datetime.today())[:19].replace(':','') + username + ".csv"
    reportOutputFilePathName = os.path.join(reportOutputLocation, reportName)

    # Open File to Write
    with open(reportOutputFilePathName, 'w', newline='') as reportFile:
        thewriter = csv.writer(reportFile)

        # Loop Through Results List and Write to CSV
        for dateSet in dataSetCollection:
            # print(dataSetCollection[dateSet])
            # thewriter.writerow(dataSetCollection[dateSet])
             thewriter.writerow(dateSet)
            # print(dataSetByDate[dateSet]) # DEBUG


    print('File Output Complete')

if __name__ == "__main__":
    data = main()
    printResults(data)