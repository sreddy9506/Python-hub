# Gets the version report for all version of a project.
#Downloads and scp to /nfs/blackduck/user...
from bda_hubapi import HubAPI
import time
from urlparse import urlparse
### Local Parameters == You must update these for this script to run
ENDPOINT ='https://bdhub-01.bdhub.crate.farm:443'
USERNAME = 'sysadmin'
PASSWORD = 'blackduck'
##### +++++++++++++++++++++++++++++++
#Create an instance of HubAPI with your endpoint
hub = HubAPI(ENDPOINT)
#Authenticate with your username and password
hub.authenticate(USERNAME, PASSWORD)
projectData = hub.getProjects()
# Get meta section for parseing
#Python dictionarys make it easy to traverse JSON data
#In this case we want the '_meta' section from the first entry of the 'items' list
for i in range(len(projectData['items'])):
    projectName = projectData['items'][i]['name']
    projectId = projectData['items'][i]['_meta']['href']
    totalProjects = projectData['totalCount']
    deleteProject = hub.deleteProject(projectId)
    print("Total count of projects on hub: %s "% (totalProjects))
    project_metaData = projectData['items'][i]['_meta']
#Get User data here
    user = hub.getLink(project_metaData, 'users')
    userData = hub.getusergroups(user)
    uname = []
    for i in range(len(userData['items'])):
        ProjectVersion = userData['items'][i]['name']
        uname.append(ProjectVersion)

# Get group data here
    usergroup = hub.getLink(project_metaData, 'usergroups')
    groupData = hub.getusergroups(usergroup)
    groupid = []
    gname =[]
    for i in range(len(groupData['items'])):
        ProjectVersion = groupData['items'][i]['group']
        url = ProjectVersion
        id=url.split("/")[-1:]
        groupid.append(id)
        for i in range(len(groupid)):
            gid = groupid[i][0]
            groupsjson = hub.getgroups(gid)
            for j in range(len(groupsjson['items'])):
                groupuser = groupsjson['items'][j]['userName']
                gname.append(groupuser)
    userName = list(set(uname + gname))
#Get link to version
    VersionLink = hub.getLink(project_metaData, 'versions')
#From the version JSON from Hub.
#We will grab version id and store
    versionData = hub.getVersions(VersionLink)
    res = []
    v = []
    for i in range(len(versionData['items'])):
        ProjectVersion = versionData['items'][i]['versionName']
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
        CodeLocations = hub.getLink(reportLink[j]['_meta'], 'codelocations')
        CodeLocationId = hub.getcodelocation(CodeLocations)
        new_report = reportsList
        if len(reportsList['items']) == 0:
            hub.generateReport(VMetaReport)
            reportsListjson = hub.getReports(VMetaReport)
            while report is not 'done':
                mostRecentReport = reportsListjson['items'][0]
                if 'finishedAt' in mostRecentReport:
                    downloadLink = hub.getLink(mostRecentReport['_meta'], 'download')
                    filename = mostRecentReport['fileName']
                    print("Generating new report for project: %s  version: %s  reportName: %s " % (projectName, ProjectVersion, filename))
                    for j in range(len(userName)):
                        uName = userName[j]
                        dest = "/nfs/blackduck/%s/%s/%s/reports/%s" %(uName,projectName,ProjectVersion,filename)
                        hub.downloadReport(downloadLink, filename)
                    #Delete Report
                    print("Report deleted: %s  version: %s  reportName: %s " % (projectName, ProjectVersion, filename))
                    deletejson = mostRecentReport['_meta']['href']
                    deleteReport = hub.deleteReport(deletejson)
                    report = 'done'
                else:
                    time.sleep(1)
                    reportsListjson = hub.getReports(VMetaReport)
                    mostRecentReport = reportsListjson['items'][0]
        else:
            if len(reportsList['items']) > 0:
                for i in range(0,len(reportsList)-1):
                    mostRecentReport = reportsList['items'][i]
                    downloadLink = hub.getLink(mostRecentReport['_meta'], 'download')
                    filename = mostRecentReport['fileName']
                    print("Report already exits, download exiting one for project: %s  version: %s  reportName: %s " % (projectName, ProjectVersion, filename))
                    for j in range(len(userName)):
                        uName = userName[j]
                        dest = "C:\Users\srkontha\Desktop\upg\ubdhub\%s\%s\%s\eports\%s" % (uName,projectName,ProjectVersion,filename)
                        #print(dest)
                        hub.downloadReport(downloadLink,filename)
                    #Delete Report
                    deletejson = mostRecentReport['_meta']['href']
                    deleteReport = hub.deleteReport(deletejson)
                    print("Report deleted: %s  version: %s  reportName: %s " % (projectName, ProjectVersion, filename))
                    report = 'done'
        #####Delete CodeLocations
        CodelocationsURL = CodeLocationId[u'items'][0][u'_meta'][u'href']
        deleteCodeLocation = hub.deleteCodeLocation(CodelocationsURL)
        print("Deleted Codelocation for version" +ProjectVersion)
    deleteProject = hub.deleteProject(projectId)
    print ("Deleted project" +projectName)
    print ("skia")
