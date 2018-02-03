from bda_hubapi import HubAPI
import time

### Local Parameters == You must update these for this script to run
ENDPOINT = 'https://bdhub-01.bdhub.crate.farm:443'
USERNAME = 'sysadmin'
PASSWORD = 'blackduck'
##### +++++++++++++++++++++++++++++++
# Create an instance of HubAPI with your endpoint
hub = HubAPI(ENDPOINT)

# Authenticate with your username and password
hub.authenticate(USERNAME, PASSWORD)

# creates a project
create = hub.createproject

# list all projects
projects = hub.getProjects()
items = projects['items']
print('\033[1m' + 'List of all projects.' + '\033[0m')
for i in range(0, len(items) - 1):
    print(items[i]['name'])

#deleteProjects
dell = hub.deleteProject()

# list all projects
projects = hub.getProjects()
items = projects['items']
print('\033[1m' + 'List of all projects.' + '\033[0m')
for i in range(0, len(items) - 1):
    print(items[i]['name'])
