# Gets the version report for the canonical version of a project.

from bda_hubapi import HubAPI
import time
### Local Parameters == You must update these for this script to run
ENDPOINT ='https://bdhub-01.bdhub.crate.farm:443'
USERNAME = ''
PASSWORD = ''
##### +++++++++++++++++++++++++++++++
#Create an instance of HubAPI with your endpoint
hub = HubAPI(ENDPOINT)

#Authenticate with your username and password
hub.authenticate(USERNAME, PASSWORD)

#Prompt for the project name
projectName = raw_input('Please enter the name of a valid project in the Black Duck Hub at '
    + ENDPOINT + '""')

#Get the project JSON from Hub
projectData = hub.getProjects(q='name:'+projectName)


# Get meta section for parseing
#Python dictionarys make it easy to traverse JSON data
#In this case we want the '_meta' section from the first entry of the 'items' list
project_metaData = projectData['items'][0]['_meta']

print project_metaData
#Get link to Cannonical version
canVersionLink = hub.getLink(project_metaData, 'canonicalVersion')

#Get the version JSON from Hub
versionData = hub.getVersions(canVersionLink)

#Get the meta section of the version
version_metaData = versionData['_meta']

#Get the link to make the project report
reportLink = hub.getLink(version_metaData, 'versionReport')

#Send a request to have the report run
hub.generateReport(reportLink)

#Sometimes it can take some time for the report to run.
#We will check with the hub once per second to see if the report is complete
#We know that the report is complete when the finished at key has a time value and
# not an empty string.

report = ''
while report is not 'done':
    reportsList = hub.getReports(reportLink)
    mostRecentReport = reportsList['items'][0]
    if 'finishedAt' in mostRecentReport:
        report = 'done'
    else:
        time.sleep(1)

downloadLink = hub.getLink(mostRecentReport['_meta'],'download')
hub.downloadReport(downloadLink)
