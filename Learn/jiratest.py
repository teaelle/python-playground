from jira import JIRA
import os

def main():

    #jira = JIRA('https://jira.atlassian.com')
    # https://jira.extendhealth.com
    jiraUserName = os.getlogin()
    jiraPassword = '00Norton!'
    jiraURL = 'https://jira.extendhealth.com'

    # jira = JIRA(
    # basic_auth=(jiraUserName, jiraPassword), 
    # options = {'server': 'https://jira.extendhealth.com'}
    # )
    options = {'server': jiraURL}
    jira = JIRA(options, basic_auth=(jiraUserName, jiraPassword))
    try: 
        issue = jira.issue('CLDS-9087')
        status = issue.fields.status
        project = jira.project('CLDS')
        print(issue.fields.project.key) 
        print(issue.fields.issuetype.name) 
        print(issue.fields.reporter.displayName)
        print(status)
        print(project)
    except:
        print('nope.')
        exit


if __name__== "__main__" :
     main()