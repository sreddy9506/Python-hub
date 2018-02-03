# Gets the version report for the canonical version of a project.

from bda_hubapi import HubAPI
import time
### Local Parameters == You must update these for this script to run
ENDPOINT ='https://bdhub-01.bdhub.crate.farm:443'
USERNAME = 'sysadmin'
PASSWORD = 'blackduck'
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

#Get link to Cannonical version
#canVersionLink = hub.getLink(project_metaData, 'canonicalVersion')

#Get link to Cannonical version
VersionLink = hub.getLink(project_metaData, 'versions')


#Get the version JSON from Hub
versionData = hub.getVersions(VersionLink)


#Get the meta section of the version
version_metaData = hub.getversionLink(versionData)
print(version_metaData[0])
i = 0
for i in range(len(version_metaData)):
    reportLink = hub.getLink(version_metaData, 'versionReport')
    report = ''
    while report is not 'done':
        reportsList = hub.getReports(reportLink)
        mostRecentReport = reportsList['items'][0]
        if 'finishedAt' in mostRecentReport:
            report = 'done'
        else:
            time.sleep(3)
        i += 1
    downloadLink = hub.getLink(mostRecentReport['_meta'],'download')
    hub.downloadReport(downloadLink)
