import csv
import os
import os.path, time
import fnmatch
from datetime import date
from datetime import datetime


def main():

    folderLocation = r'\\prodjobdata.extendhealth.com\EligibilityFileImportNotImported\2019\11'
    # folderLocation = r'\\secureshare\Encrypted Share\Delivery Management\Eligibility\ErrorOutputs\EtlErrors'

    # Set Date Range for Review
    earliestFileCreationDateToReview = '2019-01-01' # TESTING DATE RANGE
    latestFileCreateDateToReview = '2019-11-30'
    # latestFileCreateDateToReview = str(datetime.today())

    # Initialize Variables
    sflFileFound = 0
    sflCodeList = ['LABC','FARM','MDLZ','LIBM','KRFT','WTW0','CHEV','COKE','BAKK']
    dateOfFileCreation = ''
    sizeOfFile = 0
    dataSetCollection = [['ErrorMessage']]

    
    # Loop Through Directory & Folders in Directory
    for path, subdir, files in os.walk(folderLocation):

        print('Reviewing Files...', subdir)

        for file in files:
            loaderFile = os.path.join(path,file)
            if len(dataSetCollection) > 2500:
                    # print(dataSetCollection)
                    return dataSetCollection
            
            #Only Review if '.csv' (ignore folders, any random files)
            if not '.csv' in loaderFile:
                # print('Ingore Type Of:', file) # DEBUG
                continue

            try:
                dateOfFileCreation = str(datetime.fromtimestamp(os.path.getctime(loaderFile)))[:10]
                sizeOfFile = os.path.getsize(loaderFile)
            except:
                print('error getting properties of (',os.path.basename(loaderFile)[:70],')')
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
            
            sflFileFound = 0
            for x in sflCodeList:
                if x in file:
                    sflFileFound = 1
                    # print('Ingore Name Of:', file) # DEBUG
                    break

            if sflFileFound == 0:
                continue
                # print('Ingore Name Of:', file) # DEBUG

            print('Read Name Of:', file) # DEBUG
            # Open and Read File
            try:
                with open(loaderFile, 'r', newline='') as csv_file:
                    csv_reader= csv.reader(csv_file)

                    # Loop Through Each Row on the File
                    for line in csv_reader:
                        error = line[-2]
                        # print(error)
                        if 'enderCode" cannot be changed once it is set (current value' in error: 
                            continue

                        if [error] in dataSetCollection:
                            continue
                        else:
                            dataSetCollection.append([error])
            except UnicodeDecodeError: 
                print('issue with file: ',loaderFile)
                pass
            except:
                print('Unspecified issue with file: ',loaderFile)
    return dataSetCollection


def printResults(dataSetCollection):
    reportOutputLocation = r'X:\Learning Files\Python'
    # print("Results:") # DEBUG
    print('Review Complete: Outputing Results File')
    # Output CSV File with Results 
    # Determine File Name
    username = os.getlogin()
    reportName = "ErrorCollection_" + str(datetime.today())[:19].replace(':','') + username + ".csv"
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


        print('File Output Complete')

if __name__ == "__main__":
    data = main()
    print(len(data))
    if len(data) > 1:
        printResults(data)