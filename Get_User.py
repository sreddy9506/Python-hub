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

#Get the users JSON from Hub
users = hub.getUsers()
items = users['items']
print('\033[1m' + 'User Name' + "\t""\t" + "Email" + '\033[0m')
for i in range(0,len(items) -1):
    print(items[i]['userName'] + "\t""\t" + items[i]['email'])
#groups = users['items']
#for j in range(0,len(groups) -1):
#    print(items[j]['_meta'])