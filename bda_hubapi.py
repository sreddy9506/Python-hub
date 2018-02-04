import requests

#A class containing API Methods for Black Duck Hub
# For educational purposes only
class HubAPI:

    #When initializing this class it will store the endpoint of
    # the hub instance. Must include the full path.
    #eg http://myhubendpoint.mydomain:8080
    def __init__(self, endpoint):
        self.URL = endpoint
        #Hub uses session authentication.
        #This object will store the session and must be passed to each request
        #to authenticate
        self.aSession = requests.Session()
        ### Hub 4.0 and later all operations are in https
        ## Please work iwth your IT infrastructure to manage HTTP certificates
        self.aSession.verify=False
        requests.packages.urllib3.disable_warnings()
        # Variable to hold CSRF token which must be included in the header of all
        # requests that attempt to modify the system.
        self.CSRF = ''
    #Helper method to build path
    def urlCompose(self, path=''):
        return self.URL + '/' + path

    #Helper method to get Hub API links from Response
    #Params -- self - required pythont parameter
    #          meta  - the meta section of an API Response
    #          tag   -  the name of the link to get
    def getLink(self, meta, tag):
        for i in range(len(meta['links'])):
            if meta['links'][i]['rel'] == tag:
                return meta['links'][i]['href']
        print( "ERROR: getLink(" + tag +') failed. Tag not found')
        return 0

    #Helper method to get Hub API links from Response
    #Params -- self - required pythont parameter
    #          meta  - the meta section of an API Response
    #          tag   -  the name of the link to get

    def getversionLink(self, meta):
        for i in range(len(meta)):
            return meta['items'][i]['_meta']['href']
        return 0

    def getversionLink1(self, meta):
        i= 0
        for i in range(len(meta)):
            return meta[i]['_meta']['href']
    #Authenticates the session
    def authenticate( self, username, password):
        # Username and password will be sent in body of post request
        authParam = {'j_username':username, 'j_password':password}
        #Send a post request to authentication endpoint
        response = self.aSession.post(self.urlCompose('j_spring_security_check'),
            data = authParam)

        #check for Success
        if response.ok:
            self.CSRF = response.headers['x-csrf-token']
            return 1
        else:
            print("Error in authentication")
            return 0

    #Sends request to project endpoint. Parameters are optional and mapped directly
    # from API documentation.
    def getProjects( self, limit=100, offset=0,sort='',q=''):
        payload = {'limit':limit, 'offset':offset, 'sort':sort, 'q':q}
        response = self.aSession.get(self.urlCompose('api/projects'), params=payload)
        if response.ok:
            return response.json()
        else:
            print('Bad response in getProjects')
            return response.json()

    #Sends request to version endpoint for a given project.
    #This endpoint will be retrived from the project response data and passed
    # directly here as projectURL.
    def getVersions( self, projectURL, limit=100, offset=0, sort='', q=''):
        payload = {'limit':limit, 'offset':offset,'sort':sort, 'q':q}
        response = self.aSession.get(projectURL, params=payload)
        if response.ok:
            return response.json()
        else:
            print('Bad response in getVersions')
            return response.json()

    #Sends post request to have Hub create a report about a version of a project.
    # reportURL comes from the body of the getVersion response.
    def generateReport( self, reportURL):
        reportFormat = {'reportFormat':'CSV'}
        response = self.aSession.post(reportURL, json = reportFormat, headers={'x-csrf-token':self.CSRF})
        if response.ok:
            return response.text
        else:
            print("Error: bad request in generateReport()")
            return response.text

    def getReports( self, reportURL):
        response = self.aSession.get(reportURL)
        if response.ok:
            return response.json()
        else:
            print("Error: bad request in getReports")
    #Downloads the report from reportURL to dest
    def downloadReport(self, reportURL, dest='report.zip'):
        response = self.aSession.get(reportURL)
        with open(dest, 'wb') as output:
            for chunk in response.iter_content(2000):
                output.write(chunk)

    #Sends request to list all user's. Parameters are optional and mapped directly
    # from API documentation.
    def getUsers( self, limit=100, offset=0,sort='',q=''):
        payload = {'limit':limit, 'offset':offset, 'sort':sort, 'q':q}
        response = self.aSession.get(self.urlCompose('api/users'), params=payload)
        if response.ok:
            return response.json()
        else:
            print('Bad response in getUsers')
            return response.json()

    # Create a project
    @property
    def createproject( self ):
        projectname = raw_input("pls, enter your project name \n")
        API_ENDPOINT = "https://bdhub-01.bdhub.crate.farm/api/projects"
        data = {"description": "api test","name": projectname,"projectLevelAdjustments": "true","projectOwner": "srkontha","distribution": "EXTERNAL","phase": "PLANNING","versionName": "1.0.2"}
        response = self.aSession.post(self.urlCompose('api/projects'),headers={'x-csrf-token':self.CSRF},json=data)
        if response.ok:
            return response.text
        else:
            print("Error: bad request in createproject()")
            return response.text

    # delete a project
    def deleteProject( self ):
        x = raw_input("pls, enter your project name that you wan to delete \n")
        DELETE_URL = "api/projects/%s"%x
        token = {'x-csrf-token': self.CSRF}
        print("https://bdhub-01.bdhub.crate.farm:443/api/projects/%s"%x)
        response = self.aSession.delete(self.urlCompose(DELETE_URL),headers={'x-csrf-token':self.CSRF})
        if response.ok:
            return response.text
        else:
            print("Error: bad request in deleteproject()")
            return response.text

    def healthCheckliveness( self ):
            response = self.aSession.get(self.urlCompose('api/health-checks/liveness'), headers={'x-csrf-token':self.CSRF})
            if response.ok:
                return response.json()
            else:
                print('Bad response in healthCheckliveness()')
                return response.json()

    def healthCheckreadiness( self ):
            response = self.aSession.get(self.urlCompose('api/health-checks/readiness'), headers={'x-csrf-token':self.CSRF})
            if response.ok:
                return response.json()
            else:
                print('Bad response in healthCheckreadiness()')
                return response.json()
