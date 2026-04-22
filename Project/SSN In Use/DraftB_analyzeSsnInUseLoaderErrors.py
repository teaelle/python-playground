import csv
import os
import os.path, time
from datetime import date
from datetime import datetime


def fileReportingReview():

    ## Set Search Parameters

    # Set File Paths for Review and Output
    notImportedFilesLocation = '\\\\qajobdata.extendhealth.com\\EligibilityFileImportForProductionFileTestingNotImported' # TESTING LOCATION
    reportOutputLocation = '\\\\secureshare\\Encrypted Share\\Delivery Management\\ETL Load Checklists\\In Progress\\Tamilyn Peck\\Tools and Testing\\ReportOutput' # TESTING LOCATION

    # Set Date Range for Review
    earliestFileCreationDateToReview = '2018-01-01' # TESTING DATE RANGE
    latestFileCreateDateToReview = str(datetime.today())

    # Initialize Variables
    dateOfFileCreation = ''
    sizeOfFile = 0
    countOfFilesForDate = 0
    countOfRecordsWithError = 0
    countOfParticipantsWithError = 0
    countOfTotalRecords = 0
    dataSetByDate = [['File Creation Date','Count of Files','Total Loader Errors','Count of Errors by Record','Count Of Errors by Participant']] # [dateOfFileCreation,countOfTotalRecords,countOfRecordsWithError,countOfParticipantsWithError]
    fileDataSaved = False
    errorOnRecord = False

    print('Reviewing Files...')
    # Loop Through Directory & Folders in Directory
    for path, subdir, files in os.walk(notImportedFilesLocation):
        for file in files:
            loaderFile = os.path.join(path,file)
            # print('loop:',file) # DEBUG

            #Only Review if '.csv' (ignore folders, any random files)
            if not '.csv' in loaderFile:
                # print('Ingore Type Of:', file) # DEBUG
                continue

            # Get File Creation Date and Size, Print Error if Cannot Access Properties
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

            # Don't Review Files with Certiain Naming Conventions
            if "AnalystFix" in file:
                # print('Ingore Name Of:', file) # DEBUG
                continue
            if "AnalystChange" in file:
                # print('Ingore Name Of:', file) # DEBUG
                continue
            if "CampaignSegmentChange" in file:
                # print('Ingore Name Of:', file) # DEBUG
                continue


            # Open and Read File
            with open(loaderFile, 'r', newline='') as csv_file:
                csv_reader= csv.reader(csv_file)

                # print('Opened:', file, dateOfFileCreation) # DEBUG

                # Loop Through Each Row on the File
                for line in csv_reader:
                    countOfTotalRecords += 1
                    
                    # Review Last Column in Row for Error Message/Portal Code
                    if "SsnAlreadyInUseInSystem:socialSecurityNumber" in line[-1]:
                        countOfParticipantsWithError += 1
                        errorOnRecord = True
                    if "SsnAlreadyInUseInSystem:dependentSocialSecurityNumber" in line[-1]:
                        countOfParticipantsWithError += 1
                        errorOnRecord = True
                    if errorOnRecord:
                        countOfRecordsWithError += 1
                    # Reset for Next Row Review Loop
                    errorOnRecord = False 

                # Save Data Points Collected from File Reviewed
                # First File Review Entry
                if len(dataSetByDate) == 1: 
                    countOfFilesForDate = 1
                    dataSetByDate.insert(len(dataSetByDate),[dateOfFileCreation,countOfFilesForDate,countOfTotalRecords,countOfRecordsWithError,countOfParticipantsWithError])
                # After First File Review Entry
                else:
                    # For Each Date (skip header) Identify if Current File Review Date Exists in List
                    for dates in range(1,len(dataSetByDate)):

                        # Add to Total if File Creation Date Exists in List
                        if dataSetByDate[dates][0] == dateOfFileCreation:
                            dataSetByDate[dates][1] = dataSetByDate[dates][1] + countOfFilesForDate
                            dataSetByDate[dates][2] = dataSetByDate[dates][2] + countOfTotalRecords
                            dataSetByDate[dates][3] = dataSetByDate[dates][3] + countOfRecordsWithError
                            dataSetByDate[dates][4] = dataSetByDate[dates][4] + countOfParticipantsWithError
                            # print(dataSetByDate) # DEBUG
                            fileDataSaved = True
                    
                    # Track New File Creation Date if Date Didn't Exisit in Previous Loop
                    if fileDataSaved == False:
                            countOfFilesForDate = 1
                            dataSetByDate.insert(len(dataSetByDate),[dateOfFileCreation,countOfFilesForDate,countOfTotalRecords,countOfRecordsWithError,countOfParticipantsWithError])  
            
                # Reset the Counting Variables for Next File Review Loop
                countOfRecordsWithError = 0
                countOfParticipantsWithError = 0
                countOfTotalRecords = 0
                fileDataSaved = False

    # print("Results:") # DEBUG
    print('Review Complete: Outputing Results File')
    # Output CSV File with Results 
    # Determine File Name
    username = os.getlogin()
    reportName = "SsnInUseReviewReport_" + str(datetime.today())[:19].replace(':','') + username + ".csv"
    reportOutputFilePathName = os.path.join(reportOutputLocation, reportName)

    # Open File to Write
    with open(reportOutputFilePathName, 'w', newline='') as reportFile:
        thewriter = csv.writer(reportFile)

        # Loop Through Results List and Write to CSV
        for dateSet in range(0,len(dataSetByDate)):
            thewriter.writerow(dataSetByDate[dateSet])
            # print(dataSetByDate[dateSet]) # DEBUG


    print('File Output Complete')
def main():
    fileReportingReview()

main()