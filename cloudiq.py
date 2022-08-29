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
            if(response.status_code == 200):
                self.tokenData = response.json()
                ttl = int(time())+ int(self.tokenData['ExpiresIn']) # Default TTL = 3600 seconds
                expiration_time = {'UnixExpiration': ttl}
                self.tokenData.update(expiration_time) # Add expiration time to tokenData
                return self.tokenData
            elif(response.status_code == 400):
                print("400 Bad Request. Please check the API credentials you provided.")
                exit(1)
            else:
                print(response.status_code + " Error.")
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
            if(response.status_code == 200):
                return response.json()
            else:
                print(response.status_code + " Error")
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
    def getOrganizations(self, filter=None):
        """
        Get a list of all organizations associated with account.
        https://apidocs.crayon.com/scenarios/organizations-get.html

        Returns:
            json (dictionary): JSON response to GET request
        """
        path = 'Organizations'
        json = self.get(path, filter)
        return json


    def getAgreementProducts(self, orgID, filter=None):
        """
        https://apidocs.crayon.com/scenarios/agreementproducts-get.html

        Args:
            orgID (integer): organization ID; REQUIRED PARAMETER *
            filter (dictionary): filter results
                https://apidocs.crayon.com/resources/AgreementProductFilter.html
                * Filtering capabilities and parameters are better documented
                  in Swagger UI

        Returns:
            json (dictionary): JSON response to GET request
        """
        path = 'AgreementProducts'
        params = {'OrganizationId': orgID}
        params.update(filter)
        json = self.get(path, params)
        return json
