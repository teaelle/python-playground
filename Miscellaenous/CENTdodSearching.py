import csv
import os
import os.path, time
from datetime import date
from datetime import datetime

def fileReview():
    

    fileSearchLocation = r'\\secureshare\Encrypted Share\Delivery Management\Eligibility\Clients\CenturyLink\Client Originals'

    # Initialize Variables
    # Get primary SSN's
    inputString = input('Enter SSN to Search (or comma delimited list): ')
    searchList = inputString.split(",")
    # testResults = (336245609,529409871,531366868,421623250,99340966,521545531,522446885,546635867,536485196,528946779,190382076,518666592)
    # account for leading zero's?
    dodFound = False
    resultMessage = ''
    results = [['SSN','DOD','FileDate']]

    for ssn in searchList:

        # print('Searching...', primarySSN, ('(may take a minute)'))
        print(str(datetime.today())[11:19],'Searching...', ssn, ('(may take a minute)'))
        # Loop Through Directory & Folders in Directory
        for path, subdir, files in os.walk(fileSearchLocation):
            for file in files:
                loaderFile = os.path.join(path,file)
                # print('Loc:',loaderFile) # DEBUG
                if 'Client Originals\\2011\\' in loaderFile:
                    # print('skipped 2011')  # DEBUG
                    continue
                
                # stop looking at files when found
                if dodFound == True:
                    break

                #Only Review if '.csv' (ignore folders, any random files)
                if not '.csv' or not '.txt' in loaderFile:
                    # print('Ingore Type Of:', file) # DEBUG
                    continue

                # Open and Read File
                with open(loaderFile, 'r', newline='') as csv_file:
                    csv_reader= csv.reader(csv_file)

                    # print('Opened:', file) # DEBUG

                    # Loop Through Each Row on the File
                    try: 
                        for line in csv_reader:
                            
                            # Review First Column in Row for SSN value
                            if str(ssn) in line[0]:
                                # check for DOD field 7
                                if line[7] != '':
                                    resultMessage = str(ssn) + ' DOD FOUND: ' + line[7] + ' on ' + file[-12:]
                                    print(resultMessage)
                                    results.append([ssn,line[7],file[-12:]])
                                    dodFound = True
                                    break # stop looking at rows when found
                    except UnicodeDecodeError:
                        # can't read encrypted files
                        #  print('Can Not Read:', file) # DEBUG
                        pass
                    except  IndexError:
                        #  can't read files with less than 7 columns (some have bad formatting)
                        # print('Can Not Read:', file) # DEBUG
                        pass

        
        if dodFound == False:
            resultMessage = str(ssn) + ' No DOD Found'
            print(resultMessage)
            results.append([ssn,'NULL','NULL'])

        # Reset for Next SSN Search
        dodFound = False

    print(str(datetime.today())[11:19],'SEARCH COMPLETE -- Results: ')
    
    for x in results: 
        print(x)
    
    # print to CSV
    username = os.getlogin()
    reportOutputLocation = '\\\\secureshare\\Encrypted Share\\Delivery Management\\ETL Load Checklists\\In Progress\\Tamilyn Peck\\Tools and Testing\\Python\\ReportOutput' # TESTING LOCATION
    reportName = "CENTSsnSearch_" + str(datetime.today())[:19].replace(':','') + username + ".csv"
    reportOutputFilePathName = os.path.join(reportOutputLocation, reportName)
    # Open File to Write
    with open(reportOutputFilePathName, 'w', newline='') as reportFile:
        thewriter = csv.writer(reportFile)

        # Loop Through Results List and Write to CSV
        for x in range(0,len(results)):
            thewriter.writerow(results[x])
            # print(dataSetByDate[dateSet]) # DEBUG
    print('results in ReportOutput')
    repeatCheck()


def repeatCheck():
    search = input('Press 0 to exit or 1 to search another: ')
    if search == '1': 
        fileReview()


def main():
    fileReview()
    


main()