import csv
import os
import os.path, time
import datetime
import random


def randomFileGenerating():

        # Set Directory?
        # os.chdir('M:/Coding Documents/Python Data Testing/Generated Sample Data')

        # Set Possible Data Points
        possibleFirstNames = ['Billy','Bobby','John','Jack','Jeff','Mary']
        possibleLastNames = ['Anderson','Joe','Smith','Doe','Miller','Johnson']
        possibleJr = ['Jr','','','','','']
        possibleError = ['','SsnInUse:Primary','SsnInUse:Dependent','HRA Error','GUID Error','CMID Error']
        possibleFileCode = ['ABCD','XYZC','SATI','PECK','VIBE']
        # possibleFileNameAddition = ['fix','analystChange']
        increasingFileDate = datetime.date(2018,8,1)
        fileFolderLocation = "M:/Coding Documents/Python Data Testing/Generated Sample Data/"

        # Generate Files for Date Range 180
        numberOfFileDates = 180
        for j in range(numberOfFileDates):

                # Set New Date for File Path Name
                increasingFileDate += datetime.timedelta(days=1)

                # Generate Random # of Files 10 - 15 Per Date
                # createThisManyFiles = random.randint(10,15)
                for x in range(2):

                        # Set File Path Name
                        fileNumber = random.randint(454,65481)
                        rFileCode = random.choice(possibleFileCode)
                        filepath = fileFolderLocation + str(increasingFileDate) + "_" + str(x) + "_" + str(fileNumber) + "_" +  rFileCode + "fix" + str(x) + ".csv" 

                        # Generate File with Name Specified
                        with open(filepath, 'w', newline='') as f:
                                thewriter = csv.writer(f)

                                # Generate Random # of Rows
                                fileRows = random.randint(50,500)
                                for i in range(fileRows):
                                        rPhone = random.randint(1111111111,9999999999)
                                        rFirst = random.choice(possibleFirstNames)
                                        rLast = random.choice(possibleLastNames)
                                        rJr = random.choice(possibleJr)
                                        rError1 = random.choice(possibleError)
                                        rError2 = random.choice(possibleError)
        
                                        while rError1 == rError2:
                                                rError2 = random.choice(possibleError)

                                        thewriter.writerow([rFirst , rLast + ' ' + rJr, rPhone , rError1 + ';' + rError2])


def main():

        randomFileGenerating()

main()