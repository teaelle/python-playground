import csv
import os
import os.path, time
import fnmatch
from datetime import date
from datetime import datetime


def main():

    # folderLocation = r'\\prodjobdata.extendhealth.com\EligibilityFileImportNotImported\2019'
    folderLocation = r'\\secureshare\Encrypted Share\Delivery Management\Eligibility\ErrorOutputs\EtlErrors'

    # Set Date Range for Review
    earliestFileCreationDateToReview = '2018-06-01' # TESTING DATE RANGE
    latestFileCreateDateToReview = '2019-10-31'
    # latestFileCreateDateToReview = str(datetime.today())

    # Initialize Variables
    ignoreFileFound = 0
    # SFL ['LABC','FARM','MDLZ','LIBM','KRFT','WTW0','CHEV','COKE','BAKK']
    # Fidelity (non IBM) ['AGIL',' BAYR',' CMSE',' DISN',' FDMC',' FFMR',' FMAC',' GEND',' NEXT',' NLSN',' NOGU',' PEPS',' TEXI']
    excludeCodeList = ['LABC','FARM','MDLZ','LIBM','KRFT','WTW0','CHEV','COKE','BAKK']
    includeCodeList = ['AGIL','BAYR','CMSE','DISN','FDMC','FFMR','FMAC','GEND','NEXT',' NLSN','NOGU','PEPS',' TEXI']
    dateOfFileCreation = ''
    sizeOfFile = 0
    dataSetCollection = [['ErrorMessage']]

    
    # Loop Through Directory & Folders in Directory
    for path, subdir, files in os.walk(folderLocation):

        print('Reviewing Files...')

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
            
            # reset
            ignoreFileFound = 0

            for x in excludeCodeList:
                if x in file:
                    ignoreFileFound = 1
                    # print('Ingore Name Of:', file) # DEBUG
                    break

            for x in includeCodeList:
                if x not in file:
                    ignoreFileFound = 1
                    # print('Ingore Name Of:', file) # DEBUG
                    break

            if ignoreFileFound == 1:
                # print('Ingore Name Of:', file) # DEBUG
                continue
                
            # Open and Read File
            with open(loaderFile, 'r', newline='') as csv_file:
                csv_reader= csv.reader(csv_file)

                # Loop Through Each Row on the File
                for line in csv_reader:
                    error = line[-2]
                    # print(error)

                    if "PK_V_FundedPerson_personId_fundingSourceId" in error:
                        continue
                    if 'The value of column "campaignSegmentGuid" cannot be changed once it is set' in error:
                        continue
                    if "Cannot insert duplicate key in object 'dbo.PartnerPersonIdentificationMap'" in error: 
                        continue
                    if "ProdExtendHealth	Only one spouse is allowed to be added to primary shopp" in error: 
                        continue
                    if 'The value of column "clientMemberId" cannot be changed once it is set (current value "' in error: 
                        continue
                    if 'The value of column "dependentClientMemberId" cannot be changed once it is set (current value "' in error: 
                        continue
                    if 'The value of column "hraAllocationScheduleStartDate" cannot be changed once it is set' in error: 
                        continue
                    if 'The value of column "dependentHraAllocationScheduleStartDate" cannot be changed once it' in error: 
                        continue
                    if "Required field StateCode was not provided." in error: 
                        continue
                    if "since a record already exists for this organization with the same first initial, last name, and date of birth." in error: 
                        continue
                    if 'The value of column "dependentSocialSecurityNumber" cannot be changed once it is set (current value "' in error: 
                        continue
                    if 'The primary person is a dependent on another eligibility record with the same company.' in error: 
                        continue
                    if 'CampaignSegmentGuid change requests must be within the same funding source' in error: 
                        continue
                    if "Violation of PRIMARY KEY constraint 'PK_HealthInsuranceClaimNumberPersonMap_healthInsuranceClaimNumber'." in error: 
                        continue
                    if 'The dependent person is the primary, or is associated with the primary, on another eligibility record with the same company.' in error: 
                        continue
                    if 'The value of column "genderCode" cannot be changed once it is set (current value ' in error: 
                        continue
                    if 'Three-tiered relationships are not supported.  The primary person may not become related to another.' in error: 
                        continue
                    if 'The value of column "dependentGenderCode" cannot be changed once it is set (current value "' in error: 
                        continue
                    if 'PhoneNumber1 was not a valid length (10).' in error: 
                        continue
                    if 'CampaignSegmentGuid and DependentCampaignSegmentGuid were for different campaigns.' in error: 
                        continue
                    if 'The value of column "dependentCampaignSegmentGuid" cannot be changed once it is set (current value "' in error: 
                        continue
                    if 'A participant previosly loaded in the system as a dependent and now sent in the primary position cannot have an additional dependent provided.' in error: 
                        continue
                    if 'HRA allocation fields were partially provided for Primary person. All 3 must be populated or none of them.' in error: 
                        continue
                    if 'HraAllocationScheduleStartDate cannot precede ProgramEligibilityStartDate for Primary person based on the current campaign configuration.' in error: 
                        continue
                    if 'HraAllocationScheduleStartDate was not the first of the month for Primary person.' in error: 
                        continue
                    errorInList = [error]
                    try:
                        if fnmatch.filter(errorInList, 'ZipCode "?????" was not found in the database.')[0] in error:
                            continue
                    except IndexError:
                        pass
                    if 'Required field "SocialSecurityNumber" is empty.' in error: 
                        continue
                    if 'The value of column "hraAllocationScheduleFrequencyCode" cannot be changed once it is set (current value' in error: 
                        continue
                    if 'The value of column ""dependentHraAllocationScheduleFrequencyCode cannot be changed once it is set (current value' in error: 
                        continue
                    if 'Required field FirstName was not provided on Dependent person. Required field LastName was not provided on Dependent person. Required field DateOfBirth was not provided on Dependent person. Required field GenderCode was not provided on Dependent person. GenderCode was not an accepted value (M,F,U) for Dependent person.' in error: 
                        continue
                    if 'Value for field "CampaignSegmentGuid" could not be parsed:' in error: 
                        continue
                    if 'Value for field "DependentCampaignSegmentGuid" could not be parsed:' in error: 
                        continue
                    if 'Length of value for field "PhoneNumber2" is greater than maximum length (15).' in error: 
                        continue
                    if 'HraAllocationScheduleStartDate cannot precede ProgramEligibilityStartDate for Dependent person based on the current campaign configuration.' in error: 
                        continue
                    if 'HRA allocation fields were partially provided for Dependent person. All 3 must be populated or none of them.' in error: 
                        continue
                    if 'Length of value for field "CountryCode" is greater than maximum length (3).' in error: 
                        continue
                    if 'Required field "clientOriginalFileName" is empty.' in error: 
                        continue
                    if 'Length of value for field "SocialSecurityNumber" is greater than maximum length (9).' in error: 
                        continue
                    if 'Length of value for field "DependentSocialSecurityNumber" is greater than maximum length (9).' in error: 
                        continue
                    if 'Only one spouse is allowed to be related to primary shopper' in error: 
                        continue
                    if 'HraAllocationScheduleStartDate was not the first of the month for Dependent person.' in error: 
                        continue
                    if 'CK_PartnerPerson_VL_eligibilityStartDate__IsFirstDayOfMonth' in error: 
                        continue               
                    if 'CK_HealthInsuranceClaimNumberPersonMap_healthInsuranceClaimNumber__UppercaseAlphaNumericOnly' in error: 
                        continue     
                    if 'ProgramEligibilityStartDate is earlier than the year 2005 for Primary person.' in error: 
                        continue
                    if 'Required field "FirstName" is empty' in error: 
                        continue
                    if 'Required field "GenderCode" is empty.' in error: 
                        continue
                    if 'was not found for ZipCode' in error: 
                        continue
                    if 'ProdExtendHealth.Longitude.AnnuityParticipantOriginalData' in error: 
                        continue
                    if 'Required field "CampaignSegmentGuid" is empty.' in error: 
                        continue
                    if 'Required field "CityName" is empty.' in error: 
                        continue
                    if 'Length of value for field "DependentEventCode" is greater than maximum length (2).' in error: 
                        continue
                    if 'Length of value for field "Honorific" is greater than maximum length (3).' in error: 
                        continue
                    if 'Length of value for field "DependentHonorific" is greater than maximum length (3).' in error: 
                        continue
                    # if err not like SSN in use
                    if "SSN " in error: 
                        continue
                    # ETL Errors
                    if 'as a valid DateTime' in error: 
                        continue
                    if 'The DateTime represented by the string is not supported in calendar System.Globalization.GregorianCalendar' in error: 
                        continue
                    if 'exists multiple times with different data' in error: 
                        continue
                    if 'exists as dependent on another row' in error: 
                        continue
                    if 'exists on another row' in error: 
                        continue
                    # Could not read some data on row: Retiree XXXXXXXXX. Please consult original file to ensure integrity of data
                    if 'Could not read some data on row' in error: 
                        continue
                    if 'Primary sent in multiple Campaigns with overlapping eligibility' in error: 
                        continue
                    if 'XXX' in error: 
                        continue
                    if 'XXX' in error: 
                        continue

                    if [error] in dataSetCollection:
                        continue
                    else:
                        dataSetCollection.append([error])

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
    printResults(data)