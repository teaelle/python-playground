import csv
import os
import os.path, time
import fnmatch
from datetime import date
from datetime import datetime


def main():

    folderLocation = r'\\prodjobdata.extendhealth.com\EligibilityFileImportNotImported\2017\10'

    # Set Date Range for Review
    earliestFileCreationDateToReview = '2017-10-06' # TESTING DATE RANGE
    latestFileCreateDateToReview = '2017-10-10'
    # latestFileCreateDateToReview = str(datetime.today())

    # Initialize Variables
    dateOfFileCreation = ''
    sizeOfFile = 0
    dataSetCollection = [['File Date','Error Length']]
    
    # Loop Through Directory & Folders in Directory
    for path, subdir, files in os.walk(folderLocation):

        print('Reviewing Files...')

        for file in files:
            loaderFile = os.path.join(path,file)
            if len(dataSetCollection) > 3376086:
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

            # # Don't Review Files with Certiain Naming Conventions
            # if "AnalystFix" in file:
            #     # print('Ingore Name Of:', file) # DEBUG
            #     continue
            # if "AnalystChange" in file:
            #     # print('Ingore Name Of:', file) # DEBUG
            #     continue
            # if "CampaignSegmentChange" in file:
            #     # print('Ingore Name Of:', file) # DEBUG
            #     continue

            # Open and Read File
            with open(loaderFile, 'r', newline='') as csv_file:
                csv_reader= csv.reader(csv_file)

                # Loop Through Each Row on the File
                for line in csv_reader:
                    errorLength = len(line)
                    break
                    # stop on first row!!!!!!!!!!!!!
                    # print(errorLength)
                
                # print([dateOfFileCreation,errorLength])
                # Loop Through Array
                if len(dataSetCollection) == 1: 
                    dataSetCollection.append([dateOfFileCreation,errorLength])
                else: 
                    for row in range(1,len(dataSetCollection)):
                        if dataSetCollection[row][0] == dateOfFileCreation and dataSetCollection[row][1] == errorLength:
                            # print([dateOfFileCreation,errorLength])
                            continue
                        else:
                            try: 
                                dataSetCollection.append([dateOfFileCreation,errorLength])
                                # print([dateOfFileCreation,errorLength])
                            except MemoryError:
                                print("Memory Error at ",len(dataSetCollection))

                            

    return dataSetCollection

    
def printResults(dataSetCollection):
    reportOutputLocation = r'X:\Learning Files\Python'
    # print("Results:") # DEBUG
    print('Review Complete: Outputing Results File')
    # Output CSV File with Results 
    # Determine File Name
    username = os.getlogin()
    reportName = "ErrorLenReview_" + str(datetime.today())[:19].replace(':','') + username + ".csv"
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
                print(dataSetCollection[dateSet])
                thewriter.writerow(dataSetCollection[dateSet])
                # print(dataSetByDate[dateSet]) # DEBUG

        print('File Output Complete')

if __name__ == "__main__":
    data = main()
    if len(data) > 1:
        printResults(data)
    else: 
        print("No results to print.")