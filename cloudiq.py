# Author: Blastomussa
# Date: 7/25/22
import requests
from time import time
from requests.auth import HTTPBasicAuth

class CloudIQ():
    """
    SDK for Crayon's CloudIQ API for use in the development of Python scripts
    and applications. Provides a simple interface to test API calls with python
    for individuals who are inexperienced in C#.

    Attributes:
        baseURL (string): Base URL of CloudIQ API https://api.crayon.com/api/v1
        tokenData (dictionary/json): Token used to authenticate REST methods
    """
    def __init__(self, client_id, client_secret, username, password):
        """
        Initiates class with credentials necessary for Resource Password Flow Auth
        https://apidocs.crayon.com/getting-started/authentication.html#resourcepasswordflow

        Args:
            client_id (string): Client ID for registered API user
            client_secret (string): Client secret for registered API user
            username (string): Username for CloudIQ Admin account
            password (string): Password for CloudIQ Admin account
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.baseURL = 'https://api.crayon.com/api/v1/'
        self.tokenData = None


    #------------------------ Authorization and Authentication -----------------
    def getToken(self):
        """
        Posts client credentials and secrets to https://api.crayon.com/api/v1/connect/token/
        which returns an access token if credentials are valid.
        https://apidocs.crayon.com/scenarios/token-get.html

        Returns:
            tokenData (dictionary): Token json; includes AccessToken and ExpiresIn
                https://apidocs.crayon.com/resources/Token.html
        """
        tokenURL  = self.baseURL + 'connect/token'
        basic = HTTPBasicAuth(self.client_id,self.client_secret)
        header = {'Content-Type': 'application/x-www-form-urlencoded'}
        params = {
            "grant_type": "password",
            "username": self.username,
            "password": self.password,
            "scope": "CustomerApi"
        }
        try:
            response = requests.post(tokenURL, auth=basic, headers=header, data=params)
            if(int(response.status_code) == 200):
                self.tokenData = response.json()
                ttl = int(time())+ int(self.tokenData['ExpiresIn']) # Default TTL = 3600 seconds
                expiration_time = {'UnixExpiration': ttl}
                self.tokenData.update(expiration_time) # Add expiration time to tokenData
                return self.tokenData
            elif(int(response.status_code) == 400):
                print("400 Bad Request. Please check the API credentials you provided.")
                print(response.json())
                exit(1)
            else:
                print(str(response.status_code) + " Error.")
                print(response.json())
                exit(1)
        except requests.exceptions.ConnectionError:
            print("Connection Error. Please check your connection to the internet.")
            exit(1)


    def validateToken(self):
        """
        Validates Token by testing for definition and expiration

        Returns:
            tokenData['AccessToken'] (string): Token used in Authorization Header
        """
        if(not self.tokenData):  #test for tokenData definition
            self.getToken()
        elif(self.tokenData['UnixExpiration'] > (int(time()) - 15)): #test for expiration
            self.getToken()
        else: pass
        return self.tokenData['AccessToken']


    #----------------------------- REST METHODS --------------------------------
    def get(self, path, params=None):
        """
        Retrieves valid token, assembles Authorization Header and makes a GET
        requests to a specified endpoint.

        Args:
            path (string): API endoint; DO NOT include 'https://api.crayon.com/api/v1/'
            params (dictionary): filters and parameters for GET requests

        Returns:
            response.json (dictionary): JSON response to GET request
        """
        auth = 'Bearer ' + self.validateToken()
        header = {
            'Authorization': auth,
            'Accept': 'application/json',
            'Content-Type': 'application/json'
            }
        url = self.baseURL + path
        try:
            response = requests.get(url, headers=header, params=params)
            if(int(response.status_code) == 200):
                return response.json()
            else:
                print(str(response.status_code) + " Error")
                try:
                    print(response.json())
                except requests.exceptions.JSONDecodeError:
                    print(response)
                exit(1)

        except requests.exceptions.ConnectionError:
            print("Connection Error. Please check your connection to the internet.")
            exit(1)


    # DO NOT IMPLEMENT YET
    # TODO: find resource that can be created and deleted easily
    def _post(self, path, data):
        pass


    # DO NOT IMPLEMENT YET
    # TODO: find resource that can be updated easily and non-destructively
    def _put(self, path, data):
        pass


    # DO NOT IMPLEMENT YET
    # TODO: find resource that can be created and deleted easily; least destructive
    def _delete(self, path):
        pass


    #----------------------------- API METHODS ---------------------------------
    def ping(self):
        """
        Unauthenticated ping to determine if a connection to the API can be established.

        Returns:
            json (dictionary): Version and Environment Information
        """
        try:
            url = self.baseURL + "ping"
            header = {'accept': '*/*'}
            response = requests.get(url, headers=header)
            if(int(response.status_code) == 200):
                return response.json()
            else:
                print(str(response.status_code) + " Error")
                print(response.json())
                exit(1)

        except requests.exceptions.ConnectionError:
            print("Connection Error. Please check your connection to the internet.")
            exit(1)


    def me(self):
        """
        Get information about the currently authenticated user

        Returns:
            json (dictionary): Me Resource including username, userID, token and claims
        """
        path = 'Me'
        json = self.get(path)
        return json


                              ####Activity Logs####
    # 'ErrorCode': '500 InternalServerError', 'Message': "Ops. Something broke'
    def getActivityLogs(self, entityID, filter=None):
        """
        Get Activity Logs for organization

        Args:
            entityID (integer): organization ID REQUIRED
            filter (dictionary): optional

        Returns:
            json (dictionary): Activity Log Item Resource
        """
        path = 'ActivityLogs'
        params = {"Id": entityID}
        if(filter): params.update(filter)
        json = self.get(path, params=params)
        return json


                              ####Addresses####
    # 'ErrorCode': '500 InternalServerError', 'Message': "Ops. Something broke'
    def getAddresses(self, orgID, filter=None):
        """
        Get Addresses associated with an Organization

        Args:
            orgID (integer): Organization ID; REQUIRED
            filter (dictionary): optional

        Returns:
            json (dictionary): Address Resources
        """
        path = 'organizations/' + str(orgID) + '/Addresses'
        json = self.get(path, params=filter)
        return json


    # 'ErrorCode': '500 InternalServerError', 'Message': "Ops. Something broke'
    def getAddress(self, orgID, addressID, filter=None):
        """
        Get Address associated with an Organization

        Args:
            orgID (integer): Organization ID ; REQUIRED
            addressID: Address ID (from getAddresses); REQUIRED
            filter (dictionary): optional

        Returns:
            json (dictionary):
        """
        path = 'organizations/' + str(orgID) + '/Addresses/' + str(addressID)
        json = self.get(path, params=filter)
        return json


                              ####AgreementProducts####
    def getAgreementProducts(self, orgID, filter=None):
        """
        Gets a list of products available to an organization.
        https://apidocs.crayon.com/scenarios/agreementproducts-get.html

        Args:
            orgID (integer): organization ID; REQUIRED PARAMETER *
            filter (dictionary): optional filter results
                https://apidocs.crayon.com/resources/AgreementProductFilter.html
                * Filtering capabilities and parameters are better documented
                  in Swagger UI

        Returns:
            json (dictionary): AgreementProductCollection Resource
        """
        path = 'AgreementProducts'
        params = {'OrganizationId': orgID}
        if(filter): params.update(filter)
        json = self.get(path, params)
        return json


    # 'ErrorCode': '500 InternalServerError', 'Message': "Ops. Something broke'
    def getSupportedBillingCycles(self, partNumber, filter=None):
        """
        Gets the supported billing cycles of a product

        Args:
            partNumber (string): Part Number of Product; REQUIRED PARAMETER *
            filter (dictionary): optional filter results

        Returns:
            json (dictionary): BillingCycleEnum Resource
        """
        path = 'AgreementProducts/'+ str(partNumber)+ '/supportedbillingcycles'
        json = self.get(path, params=filter)
        return json



                              ####Organizations####
    def getOrganizations(self, filter=None):
        """
        Get a list of all organizations associated with account.
        https://apidocs.crayon.com/scenarios/organizations-get.html

        Args:
            filter (dictionary): optional

        Returns:
            json (dictionary): OrganizationCollection Resource
                https://apidocs.crayon.com/resources/OrganizationCollection.html
        """
        path = 'Organizations'
        json = self.get(path, filter)
        return json


    def getOrganization(self, orgID):
        """
        Get an organization by OrgID
        https://apidocs.crayon.com/scenarios/organization-get.html

        Args:
            orgID (integer): organization ID; REQUIRED PARAMETER *

        Returns:
            json (dictionary): Organization Resource
                https://apidocs.crayon.com/resources/Organization.html
        """
        path = 'Organizations/' + str(orgID)
        json = self.get(path)
        return json


    def getOrganizationSalesContact(self, orgID):
        """
        Get the Sales Contact for an organization

        Args:
            orgID (integer): organization ID; REQUIRED PARAMETER *

        Returns:
            json (dictionary): OrganizationSalesContact Resource
        """
        path = 'Organizations/' + str(orgID) + "/salescontact"
        json = self.get(path)
        return json


    def organizationHasAccess(self, orgID):
        """
        Test if current API credentials have access to an organization

        Args:
            orgID (integer): organization ID; REQUIRED PARAMETER *

        Returns:
            access (boolean): True or False
        """
        path = "Organizations/HasAccess/" + str(orgID)
        access = self.get(path)
        return access
