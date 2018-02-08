# Gets the version report for all version of a project.
#Downloads and scp to /nfs/blackduck/user...
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

#Get link to version
VersionLink = hub.getLink(project_metaData, 'versions')

#From the version JSON from Hub.
#We will grab version id and store
versionData = hub.getVersions(VersionLink)
res = []
v = []
for i in range(len(versionData['items'])):
    res = versionData['items'][i]['_meta']['href']
    v.append(res)
#Variable
versionMetaData = v #Store the version id value
reportLink = []
reportsList = []
mostRecentReport = []
VData = []
#Iterating trough all version id and get the report id link for all
for i in range(len(versionMetaData)):
    rLink = hub.getVersions(versionMetaData[i])
    reportLink.append(rLink)
VMetaReport = []
vReport = []
report = ''
for j in range(len(reportLink)):
    VMetaReport = hub.getLink(reportLink[j]['_meta'], 'versionReport')
    reportsList = hub.getReports(VMetaReport)
    if len(reportsList['items']) == 0:
        hub.generateReport(VMetaReport)
        reportsListjson = hub.getReports(VMetaReport)
        while report is not 'done':
            mostRecentReport = reportsListjson['items'][0]
            if 'finishedAt' in mostRecentReport:
                report = 'done'
                break
            else:
                time.sleep(1)
    if len(reportsList['items']) > 0:
        for i in range(len(reportsList)):
            mostRecentReport = reportsList['items'][i]
            downloadLink = hub.getLink(mostRecentReport['_meta'], 'download')
            filename = (projectName +".zip")
            print(filename)
            hub.downloadReport(downloadLink,filename)

#    vReport.append(VMetaReport)

    # Sometimes it can take some time for the report to run.
    # We will check with the hub once per second to see if the report is complete
    # We know that the report is complete when the finished at key has a time value and
    # not an empty string.


#
