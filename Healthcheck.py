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

#Determine the liveness status to determine if the system is normal and healthy state
liveness = hub.healthCheckliveness()
items = liveness['healthy']
a=True
if items == a:
    print("Server is Healthy")
else:
    print("Not Healthy")

#Determine the readiness status to determine if the system is ready to receive requests.
readiness = hub.healthCheckliveness()
items = readiness['healthy']
a=True
if items == a:
    print("Server is Healthy and ready to accept request")
else:
    print("Server is not Healthy, Will not accept any request at this moment")