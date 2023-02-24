# Author: Joe Courtney
# Date: 7/25/22
import requests
from time import time
from requests.auth import HTTPBasicAuth
from time import strftime

class CloudIQ():
    """
    SDK for Crayon's CloudIQ API for use in the development of Python scripts
    and applications. Provides a simple interface to test API calls with python
    for individuals who are inexperienced in C#.

    Attributes:
        baseURL (string): Base URL of CloudIQ API https://api.crayon.com/api/v1
        tokenData (dictionary/json): Token used to authenticate REST methods
    """
    def __init__(self, client_id=None, client_secret=None, username=None, password=None):
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
        self.baseURL = 'https://api.crayon.com/api/v1'
        self.tokenData = None
        self.unixTTL = None


    #------------------------ Authorization and Authentication -----------------
    def getToken(self):
        # research implicit flow implimentation
        """
        Posts client credentials and secrets to https://api.crayon.com/api/v1/connect/token/
        which returns an access token if credentials are valid. Uses ResourcePasswordFlow.
        https://apidocs.crayon.com/scenarios/token-get.html

        Returns:
            tokenData (dictionary): Token json; includes AccessToken and ExpiresIn
                https://apidocs.crayon.com/resources/Token.html
        """
        tokenURL  = f"{self.baseURL}/connect/token"
        basic = HTTPBasicAuth(self.client_id,self.client_secret)
        header = {'Content-Type': 'application/x-www-form-urlencoded'}
        params = {
            'grant_type': 'password',
            'username': self.username,
            'password': self.password,
            'scope': 'CustomerApi'
        }
        try:
            response = requests.post(tokenURL, auth=basic, headers=header, data=params)
            if(int(response.status_code) == 200):
                self.tokenData = response.json()
                self.unixTTL = int(time()) + int(self.tokenData['ExpiresIn']) # Default TTL = 3600 seconds
                return self.tokenData
            elif(int(response.status_code) == 400):
                print("400 Bad Request. Please check the API credentials you provided.")
                try:
                    print(response.json())
                except requests.exceptions.JSONDecodeError:
                    print(response)
                exit(1)
            else:
                print(f"{response.status_code} Error")
                try:
                    print(response.json())
                except requests.exceptions.JSONDecodeError:
                    print(response)
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
        elif(self.unixTTL > (int(time()) - 600)): #test for expiration within 10 minutes
            self.getToken()   
        return self.tokenData['AccessToken']


    #----------------------------- REST METHODS --------------------------------
    def get(self, path, params=None):
        """
        Retrieves valid token, assembles Authorization Header and makes a GET
        request to a specified endpoint.

        Args:
            path (string): API endoint; DOES NOT include 'https://api.crayon.com/api/v1/'
            params (dictionary): filters and parameters for GET requests

        Returns:
            response.json (dictionary): resource schema 
        """
        header = {
            'Authorization': f"Bearer {self.validateToken()}",
            'Accept': 'application/json',
            'Content-Type': 'application/json'
            }
        try:
            response = requests.get(url=path, headers=header, params=params)
            if(int(response.status_code) == 200):
                return response.json()
            else:
                print(f"{response.status_code} Error")
                try:
                    print(response.json())
                except requests.exceptions.JSONDecodeError:
                    print(response)
                exit(1)

        except requests.exceptions.ConnectionError:
            print("Connection Error. Please check your connection to the internet.")
            exit(1)


    def post(self, path, data):
        """
        Retrieves valid token, assembles Authorization Header and makes a POST
        request to a specified endpoint.
  
        Args:
            path (string): API endoint; DOES NOT include 'https://api.crayon.com/api/v1/'
            data (dictionary): resource schema in json(dict) form

         Returns:
            response.json (dictionary): resource schema 
        """
        header = {
            'Authorization': f"Bearer {self.validateToken()}",
            'Content-Type': 'application/json'
            }
        try:
            response = requests.post(url=path, headers=header, json=data)
            if(int(response.status_code) == 200):
                return response.json()
            elif(int(response.status_code) == 500):
                print(f"{response.status_code} Error. Check your schema definition.")
                print(response.json())
            else:
                print(f"{response.status_code} Error")
                try:
                    print(response.json())
                except requests.exceptions.JSONDecodeError:
                    print(response)
                exit(1)

        except requests.exceptions.ConnectionError:
            print("Connection Error. Please check your connection to the internet.")
            exit(1)


    # TEST WITH: /api/v1/Clients/{clientID}
    def put(self, path, data):
        """
        Retrieves valid token, assembles Authorization Header and makes a PUT
        request to a specified endpoint.

        Args:
            path (string): API endoint; DOES NOT include 'https://api.crayon.com/api/v1/'
            data (dictionary): resource schema in json(dict) form
        
         Returns:
            response.json (dictionary): resource schema 
        """
        header = {
            'Authorization': f"Bearer {self.validateToken()}",
            'Accept': 'application/json',
            'Content-Type': 'application/json'
            }
        try:
            response = requests.post(url=path, headers=header, json=data)
            if(int(response.status_code) == 200):
                return response.json()
            else:
                print(f"{response.status_code} Error")
                try:
                    print(response.json())
                except requests.exceptions.JSONDecodeError:
                    print(response)
                exit(1)

        except requests.exceptions.ConnectionError:
            print("Connection Error. Please check your connection to the internet.")
            exit(1)


    # test with Azure subscription rename
    # Check Content type in header
    def patch(self, path, data):
        """
        Retrieves valid token, assembles Authorization Header and makes a PATCH
        request to a specified endpoint. Only used for two operations: renaming 
        Azure Subscription and updating product container row

        Args:
            path (string): API endoint; DOES NOT include 'https://api.crayon.com/api/v1/'
            data (dictionary): resource schema in json(dict) form

         Returns:
            response.json (dictionary): resource schema 
        """
        header = {
            'Authorization': f"Bearer {self.validateToken()}",
            'Accept': 'application/json',
            'Content-Type': 'application/json'
            }
        try:
            response = requests.patch(url=path, headers=header, json=data)
            if(int(response.status_code) == 200):
                return response.json()
            else:
                print(f"{response.status_code} Error")
                try:
                    print(response.json())
                except requests.exceptions.JSONDecodeError:
                    print(response)
                exit(1)

        except requests.exceptions.ConnectionError:
            print("Connection Error. Please check your connection to the internet.")
            exit(1)


    # Should this return any data (api mostly returns boolean for delete) or just status code
    def delete(self, path, params=None):
        """
        Retrieves valid token, assembles Authorization Header and makes a DELETE
        request to a specified endpoint.

        Args:
            path (string): API endoint; DOES NOT include 'https://api.crayon.com/api/v1/'
            params (dictionary): optional parameters used for some calls

        Returns:
            response.status_code (dictionary): JSON response to DELETE request
        """
        header = {
            'Authorization': f"Bearer {self.validateToken()}",
            'Accept': '*/*',
            }
        try:
            response = requests.delete(url=path, headers=header, params=params)
            return response.status_code

        except requests.exceptions.ConnectionError:
            print("Connection Error. Please check your connection to the internet.")
            exit(1)        


    #----------------------------- API METHODS ---------------------------------
    def ping(self):
        """
        Unauthenticated ping to determine if a connection to the API can be established.

        Returns:
            json (dictionary): Version and Environment Information
        """
        try:
            url = f"{self.baseURL}/ping"
            header = {'accept': '*/*'}
            response = requests.get(url, headers=header)
            if(int(response.status_code) == 200):
                return response.json()
            else:
                print(f"{response.status_code} Error")
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
        path = f"{self.baseURL}/Me"
        return self.get(path)


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
        path = f"{self.baseURL}/ActivityLogs"
        params = {'Id': entityID}
        if(filter): params.update(filter)
        return self.get(path, params)       


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
        path = f"{self.baseURL}/organizations/{orgID}/Addresses"
        return self.get(path, filter)       


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
        path = f"{self.baseURL}/organizations/{orgID}/Addresses/{addressID}"
        return self.get(path, filter)


                              ####AgreementProducts####
    def getAgreementProducts(self, orgID, filter=None):
        """
        Gets a list of products available to an organization.
        https://apidocs.crayon.com/scenarios/agreementproducts-get.html

        Args:
            orgID (integer): organization ID; REQUIRED
            filter (dictionary): optional filter results
                https://apidocs.crayon.com/resources/AgreementProductFilter.html
                * Filtering capabilities and parameters are better documented
                  in Swagger UI

        Returns:
            json (dictionary): AgreementProductCollection Resource
        """
        path = f"{self.baseURL}/AgreementProducts"
        params = {'OrganizationId': orgID}
        if(filter): params.update(filter)
        return self.get(path, params)


    # 'ErrorCode': '500 InternalServerError', 'Message': "Ops. Something broke'
    def getSupportedBillingCycles(self, partNumber, filter=None):
        """
        Gets the supported billing cycles of a product

        Args:
            partNumber (string): Part Number of Product; REQUIRED
            filter (dictionary): optional filter results

        Returns:
            json (dictionary): BillingCycleEnum Resource
        """
        path = f"{self.baseURL}/AgreementProducts/{partNumber}/supportedbillingcycles"
        return self.get(path, params=filter)

    
    '''
    # post prototype
    def create(self, schema):
        """
        Create a resource

        Args:
            schema (dictionary): required

        Returns:
            json: resource schema
        """
        path = f"{self.baseURL}"
        return self.post(path, schema)
    '''

    '''
    # post prototype
    def create(self, schema):
        """
        Create a resource

        Args:
            schema (dictionary): required

        Returns:
            json: resource schema
        """
        path = f"{self.baseURL}"
        return self.post(path, schema)
    '''


                              ####Agreements####
    def getAgreements(self, filter=None):
        """
        Get Agreements

        Args:
            filter (dictionary): optional filter

        Returns:
            json (dictionary): Agreement Resource
        """
        path = f"{self.baseURL}/Agreements"
        return self.get(path, filter)


                              ####AgreementReports####
    def getAgreementReports(self, productContainerId):
        """
        Get Agreement Reports

        Args:
            productContainerId (integer): REQUIRED

        Returns:
            json (dictionary): Agreement Report Resource
        """
        path = f"{self.baseURL}/AgreementReports/{productContainerId}"
        return self.get(path)


                              ####Assets####
    def deleteAssetTag(self, assetID):
        """
        Delete an Asset tag

        Args:
            assetID: Required 

        Returns:
            status code (int): 200 success
        """
        path = f"{self.baseURL}/Assets/{assetID}/tags"
        return self.delete(path)


    '''
    # post prototype
    def create(self, schema):
        """
        Create a resource

        Args:
            schema (dictionary): required

        Returns:
            json: resource schema
        """
        path = f"{self.baseURL}"
        return self.post(path, schema)
    '''

    '''
    # post prototype
    def create(self, schema):
        """
        Create a resource

        Args:
            schema (dictionary): required

        Returns:
            json: resource schema
        """
        path = f"{self.baseURL}"
        return self.post(path, schema)
    '''


    '''
    # post prototype
    def create(self, schema):
        """
        Create a resource

        Args:
            schema (dictionary): required

        Returns:
            json: resource schema
        """
        path = f"{self.baseURL}"
        return self.post(path, schema)
    '''
    


                              ####AWS Accounts####


                              ####Azure Plans####
    def getAzurePlan(self, azurePlanID):
        """
        Get an Azure Plan

        Args:
            azurePlanID (int): required; can be found using getCustomerTenantAzurePlan()

        Returns:
            json (dict): Azure plan resource schema

        """
        path = f"{self.baseURL}/AzurePlans/{azurePlanID}"
        return self.get(path)


    def getAzureSubscriptions(self, azurePlanID, filter=None):
        """
        Get Azure Subscriptions in an Azure Plan

        Args:
            azurePlanID (int): required; can be found using getCustomerTenantAzurePlan()
            filter : Page and PageSize required to make this call

        Returns:
            json (dict): Azure Subscription resource schema

        """
        path = f"{self.baseURL}/AzurePlans/{azurePlanID}/azureSubscriptions"
        return self.get(path,filter)


    '''
    # post prototype
    def create(self, schema):
        """
        Create a resource

        Args:
            schema (dictionary): required

        Returns:
            json: resource schema
        """
        path = f"{self.baseURL}"
        return self.post(path, schema)
    '''

    '''
    # post prototype
    def create(self, schema):
        """
        Create a resource

        Args:
            schema (dictionary): required

        Returns:
            json: resource schema
        """
        path = f"{self.baseURL}"
        return self.post(path, schema)
    '''

    '''
    # post prototype
    def create(self, schema):
        """
        Create a resource

        Args:
            schema (dictionary): required

        Returns:
            json: resource schema
        """
        path = f"{self.baseURL}"
        return self.post(path, schema)
    '''


    # TEST THIS
    def renameAzureSubscription(self, azurePlanID, subscriptionID, data):
        """
        Rename an Azure Subscription

        Args:
            azurePlanID: Azure Plan ID; required
            subscriptionID: required
            data (dictionary): AzureSubscriptionRename Schema; required
        
        Returns:
            json (dictionary): AzureSubscriptionUpdated Resource
        """
        path = f"{self.baseURL}/AzurePlans/{azurePlanID}/azureSubscriptions/{subscriptionID}/rename"
        return self._patch(path,data)


                              ####Billing Cycles####
    def getBillingCycles(self, includeUnknown=False):
        """
        Get Billing Cycles

        Args:
            includeUnknown (boolean): optional filter

        Returns:
            json (dictionary): BillingCycle Resource
        """
        path = f"{self.baseURL}/BillingCycles"
        params = {'includeUnknown': includeUnknown}
        return self.get(path, params)


    def getProductVariantBillingCycles(self, productVariantId):
        """
        Get Billing Cycles for a specific Product Variant

        Args:
            productVariantId (integer): REQUIRED

        Returns:
            json (dictionary): BillingCycle Resource
        """
        path = f"{self.baseURL}/BillingCycles/productVariant/{productVariantId}"
        return self.get(path)
        

    def getBillingCyclesNameDictionary(self):
        """
        Get Billing Cycle CSP Name Dictionary

        Returns:
            json (dictionary): Billing Cycle Name Dictionary
        """
        path = f"{self.baseURL}/BillingCycles/cspNameDictionary"
        return self.get(path)


                        ####Billing Statements####
    def getBillingStatements(self, orgID, filter=None):
        """
        Get Billing Statements

        Args:
            orgID: organization ID; REQUIRED
            filter (dictionary): optional filter

        Returns:
            json (dictionary): BillingStatement Resource
        """
        path = f"{self.baseURL}/BillingStatements"
        params = {'OrganizationId': orgID}
        if(filter): params.update(filter)
        return self.get(path, params)


    def getGroupedBillingStatements(self, orgID, filter=None):
        """
        Get Billing Statements

        Args:
            orgID: organization ID; REQUIRED
            filter (dictionary): optional filter

        Returns:
            json (dictionary): GroupedBillingStatement Resource
        """
        path = f"{self.baseURL}/BillingStatements/grouped"
        params = {'OrganizationId': orgID}
        if(filter): params.update(filter)
        return self.get(path, params)
        

    def getBillingStatementExcel(self, statementID):
        """
        Get Billing statement Excel file

        Args:
            statementID (integer): REQUIRED

        Returns:
            json (dictionary): byte array of excel file
        """
        path = f"{self.baseURL}/BillingStatements/file/{statementID}"
        return self.get(path)
        

    def getBillingStatementCSV(self, statementID):
        """
        Get billing statement reconciliation file

        Args:
            statementID (integer): REQUIRED

        Returns:
            json (dictionary): byte array of CSV file
        """
        path = f"{self.baseURL}/BillingStatements/{statementID}/reconciliationfile"
        return self.get(path)    


    def getBillingStatementJSON(self, statementID):
        """
        Get billing statement JSON file

        Args:
            statementID (integer): REQUIRED

        Returns:
            json (dictionary): byte array of JSON file
        """
        path = f"{self.baseURL}/BillingStatements/{statementID}/billingrecordsfile"
        return self.get(path)
        

                            ####Blog Items####
    def getBlogItems(self, filter=None):
        """
        Get Blog Items

        Args:
            orgID (integer): REQUIRED

        Returns:
            json (dictionary): BlogItem Resource
        """
        path = f"{self.baseURL}/BlogItems"
        return self.get(path, filter)
        

                            ####Clients####
    def getClients(self, filter=None):
        """
        Get list of API Clients

        Args:
            filter (dictionary): optional

        Returns:
            json (dictionary): list of Client Resources
        """
        path = f"{self.baseURL}/Clients"
        return self.get(path, filter)     


    def getClient(self, clientID):
        """
        Get API Client

        Args:
            clientID (string): REQUIRED

        Returns:
            json (dictionary): Client Resource
        """
        path = f"{self.baseURL}/Clients/{clientID}"
        return self.get(path)
        

    def deleteClient (self, clientID):
        """
        Delete an API Client. Disables Client but doesn't remove it?

        Args:
            clientID: Required 

        Returns:
            status code (int): 200 success
        """
        path = f"{self.baseURL}/Clients/{clientID}"
        status_code = self.delete(path)
        return status_code


    def createClient(self, schema):
        """
        Create an API Client

        Args: 
            schema (dictionary): Client Schema; null unknown fields

        Returns:
            json (dictionary): Client Schema
        """
        path = f"{self.baseURL}/Clients"
        return self.post(path, schema)     


    # NOT WORKING; MIGHT BE SCHEMA MIGHT BE SOMETHING ELSE 405 error
    def updateClient(self, clientID, schema):
        """
        """
        path = f"{self.baseURL}/Clients/{clientID}"
        print(schema)
        return self._put(path, schema)
        

                            ####Consumers####
    def getConsumers(self, orgID, filter=None):
        """
        Get list of Consumers

        Args:
            orgID: REQUIRED
            filter (dictionary): optional

        Returns:
            json (dictionary): list of Consumer Resources
        """
        path = f"{self.baseURL}/Consumers"
        params = {'OrganizationId': orgID}
        if(filter): params.update(filter)
        return self.get(path, params)
        

    def getConsumer(self, consumerID):
        """
        Get Consumer

        Args:
            consumerID (integer): REQUIRED

        Returns:
            json (dictionary): Consumer Resource
        """
        path = f"{self.baseURL}/Consumers/{consumerID}"
        return self.get(path)
        
    
    '''
    # post prototype
    def create(self, schema):
        """
        Create a resource

        Args:
            schema (dictionary): required

        Returns:
            json: resource schema
        """
        path = f"{self.baseURL}"
        return self.post(path, schema)
    '''


    def deleteConsumer (self, consumerID):
        """
        Delete a Consumer

        Args:
            consumerID: Required 

        Returns:
            status code (int): 200 success
        """
        path = f"{self.baseURL}/Consumers/{consumerID}"
        status_code = self.delete(path)
        return status_code


                            ####CrayonAccounts####
    def getCrayonAccounts(self, orgID, filter=None):
        """
        Get list of Crayon Accounts

        Args:
            orgID (integer): REQUIRED
            filter (dictionary): optional

        Returns:
            json (dictionary): list of CrayonAccount Resources
        """
        path = f"{self.baseURL}/CrayonAccounts"
        params = {'OrganizationId': orgID}
        if(filter): params.update(filter)
        return self.get(path, params)    


    '''
    # post prototype
    def create(self, schema):
        """
        Create a resource

        Args:
            schema (dictionary): required

        Returns:
            json: resource schema
        """
        path = f"{self.baseURL}"
        return self.post(path, schema)
    '''


    def getCrayonAccount(self, accountID):
        """
        Get Crayon Account

        Args:
            accountID (integer): REQUIRED

        Returns:
            json (dictionary): CrayonAccount Resource
        """
        path = f"{self.baseURL}/CrayonAccounts/{accountID}"
        return self.get(path)
        

                        ####CustomerTenantsAgreements####
    def getCustomerTenantAgreements(self, tenantID, AgreementTypeConsent):
        """
        Get a customer tenant agreement

        Args:
            tenantID (integer): REQUIRED
            AgreementTypeConsent (integer): 0 or 1; REQUIRED

        Returns:
            json (dictionary): ServiceAccountAgreement Resource
        """
        path = f"{self.baseURL}/CustomerTenants/{tenantID}/Agreements"
        params = {'AgreementTypeConsent': AgreementTypeConsent}
        return self.get(path, params)
        

    '''
    # post prototype
    def create(self, schema):
        """
        Create a resource

        Args:
            schema (dictionary): required

        Returns:
            json: resource schema
        """
        path = f"{self.baseURL}"
        return self.post(path, schema)
    '''


                            ####CustomerTenants####
    def getCustomerTenants(self, orgID, filter=None):
        """
        Get a list of Customer Tenants

        Args:
            orgID (integer): REQUIRED
            filter (dictionary): optional

        Returns:
            json (dictionary): List of CustomerTenant Resources
        """
        path = f"{self.baseURL}/CustomerTenants"
        params = {'OrganizationId': orgID}
        if(filter): params.update(filter)
        return self.get(path, params)
        

    
    '''
    # post prototype
    def create(self, schema):
        """
        Create a resource

        Args:
            schema (dictionary): required

        Returns:
            json: resource schema
        """
        path = f"{self.baseURL}"
        return self.post(path, schema)
    '''


    def getCustomerTenant(self, tenantID):
        """
        Get a single customer tenant

        Args:
            tenantID (integer): REQUIRED

        Returns:
            json (dictionary): CustomerTenant Resource
        """
        path = f"{self.baseURL}/CustomerTenants/{tenantID}"
        return self.get(path)
        


    def getCustomerTenantDetails(self, tenantID):
        """
        Get detailed information on a customer tenant

        Args:
            tenantID (integer): REQUIRED

        Returns:
            json (dictionary): CustomerTenantDetailed Resource
        """
        path = f"{self.baseURL}/CustomerTenants/{tenantID}/detailed"
        return self.get(path)
        

    
    '''
    # post prototype
    def create(self, schema):
        """
        Create a resource

        Args:
            schema (dictionary): required

        Returns:
            json: resource schema
        """
        path = f"{self.baseURL}"
        return self.post(path, schema)
    '''


    def getCustomerTenantAzurePlan(self, tenantID):
        """
        Get the Azure plan associated with a customer tenant

        Args:
            tenantID (integer): REQUIRED

        Returns:
            json (dictionary): AzurePlan Resource
        """
        path = f"{self.baseURL}/CustomerTenants/{tenantID}/AzurePlan"
        return self.get(path)
        


    def deleteCustomerTenant (self, tenantID):
        """
        Delete a

        Args:
            tenantID: Required 

        Returns:
            status code (int): 200 success
        """
        path = f"{self.baseURL}/CustomerTenants/{tenantID}"
        status_code = self.delete(path)
        return status_code


                            ####FacebookOrders####

    '''
    # post prototype
    def create(self, schema):
        """
        Create a resource

        Args:
            schema (dictionary): required

        Returns:
            json: resource schema
        """
        path = f"{self.baseURL}"
        return self.post(path, schema)
    '''

                            ####GoogleOrders####
    '''
    # post prototype
    def create(self, schema):
        """
        Create a resource

        Args:
            schema (dictionary): required

        Returns:
            json: resource schema
        """
        path = f"{self.baseURL}"
        return self.post(path, schema)
    '''


                            ####Groupings####
    def getGroupings(self, orgID, filter=None):
        """
        Get a list of Groupings

        Args:
            orgID (integer): REQUIRED
            filter (dictionary): optional

        Returns:
            json (dictionary): List of Grouping Resources
        """
        path = f"{self.baseURL}/Groupings"
        params = {'OrganizationId': orgID}
        if(filter): params.update(filter)
        return self.get(path, params)
        

    
    '''
    # post prototype
    def create(self, schema):
        """
        Create a resource

        Args:
            schema (dictionary): required

        Returns:
            json: resource schema
        """
        path = f"{self.baseURL}"
        return self.post(path, schema)
    '''


    def getGrouping(self, groupingID):
        """
        Get a grouping

        Args:
            groupingID (integer): REQUIRED

        Returns:
            json (dictionary): Grouping Resource
        """
        path = f"{self.baseURL}/Groupings/{groupingID}"
        return self.get(path)
        


 
    def deleteGroupings (self, groupingID):
        """
        Delete a Groouping

        Args:
            groupingID: Required 

        Returns:
            status code (int): 200 success
        """
        path = f"{self.baseURL}/Groupings/{groupingID}"
        status_code = self.delete(path)
        return status_code



                            ####InvoiceProfiles####
    def getInvoiceProfiles(self, orgID, filter=None):
        """
        Get a list of invoice profiles

        Args:
            orgID (integer): REQUIRED
            filter (dictionary): optional

        Returns:
            json (dictionary): List of InvoiceProfile Resources
        """
        path = f"{self.baseURL}/InvoiceProfiles"
        params = {'OrganizationId': orgID}
        if(filter): params.update(filter)
        return self.get(path, params)
        

    
    '''
    # post prototype
    def create(self, schema):
        """
        Create a resource

        Args:
            schema (dictionary): required

        Returns:
            json: resource schema
        """
        path = f"{self.baseURL}"
        return self.post(path, schema)
    '''

    # Returning None. Bug?
    def getInvoiceProfile(self, invoiceProfileID):
        """
        Get an InvoiceProfile

        Args:
            invoiceProfileID (integer): REQUIRED

        Returns:
            json (dictionary): InvoiceProfile Resource
        """
        path = f"{self.baseURL}/InvoiceProfiles/{invoiceProfileID}"
        return self.get(path)


    def deleteInvoiceProfile(self, invoiceprofileID):
        """
        Delete an Invoice Profile

        Args:
            invoiceprofileID: Required 

        Returns:
            status code (int): 200 success
        """
        path = f"{self.baseURL}/InvoiceProfiles/{invoiceprofileID}"
        status_code = self.delete(path)
        return status_code


                            ####ManagementLinks####
    # snagged; need subscriptionID filter?
    # RETEST!!
    def _getManagementLinks(self, filter=None):
        """
        Get a list of ManagementLinks

        Args:
            filter (dictionary): optional

        Returns:
            json (dictionary): List of ManagementLinks Resources
        """
        path = f"{self.baseURL}/ManagementLinks"
        return self.get(path, filter)
        


    # 403 Forbidden Error message
    def _getGroupedManagementLinks(self, filter=None):
        """
        Get a list of ManagementLinks

        Args:
            filter (dictionary): optional

        Returns:
            json (dictionary): List of ManagementLinkGrouped Resources
        """
        path = f"{self.baseURL}/ManagementLinks/grouped"
        return self.get(path, filter)
        


                            ####OrganizationAccess####
    # 'ErrorCode': '401 Unauthorized', 'Message': 'Invalid token'???
    def _getOrganizationAccessGrant(self, filter=None):
        """
        Get a list of an organizations access grants.

        Args:
            filter (dictionary): optional

        Returns:
            json (dictionary): OrganizationAccess Resource
        """
        path = f"{self.baseURL}/OrganizationAccess/grant"
        return self.get(path, filter)
        


    # 'ErrorCode': '401 Unauthorized', 'Message': 'Invalid token'???
    def _getOrganizationAccess(self, filter=None):
        """
        Get a list of an organizations access grants.

        Args:
            filter (dictionary): optional

        Returns:
            json (dictionary): OrganizationAccess Resource
        """
        path = f"{self.baseURL}/OrganizationAccess"
        return self.get(path, filter)
        


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
        path = f"{self.baseURL}/Organizations"
        return self.get(path, filter)
        


    def getOrganization(self, orgID):
        """
        Get an organization by OrgID
        https://apidocs.crayon.com/scenarios/organization-get.html

        Args:
            orgID (integer): organization ID; REQUIRED

        Returns:
            json (dictionary): Organization Resource
                https://apidocs.crayon.com/resources/Organization.html
        """
        path = f"{self.baseURL}/Organizations/{orgID}"
        return self.get(path)
        


    def getOrganizationSalesContact(self, orgID):
        """
        Get the Sales Contact for an organization

        Args:
            orgID (integer): organization ID; REQUIRED

        Returns:
            json (dictionary): OrganizationSalesContact Resource
        """
        path = f"{self.baseURL}/Organizations/{orgID}/salescontact"
        return self.get(path)
        


    def getOrganizationHasAccess(self, orgID):
        """
        Test if current API credentials have access to an organization

        Args:
            orgID (integer): organization ID; REQUIRED

        Returns:
            access (boolean): True or False
        """
        path = f"{self.baseURL}/Organizations/HasAccess/{orgID}"
        access = self.get(path)
        return access


                            ####ProductContainers####
    def getProductContainers(self, orgID, filter=None):
        """
        Get a list of product containers

        Args:
            orgID (integer): REQUIRED
            filter (dictionary): optional

        Returns:
            json (dictionary): List of ProductContainer Resources
        """
        path = f"{self.baseURL}/ProductContainers"
        params = {'OrganizationId': orgID}
        if(filter): params.update(filter)
        return self.get(path, params)
        

    def getProductContainer(self, productContainerID):
        """
        Get a product containers

        Args:
            productContainerID (integer): REQUIRED

        Returns:
            json (dictionary): ProductContainer Resource
        """
        path = f"{self.baseURL}/ProductContainers/{productContainerID}"
        response = self.get(path)
        return response


    def getProductContainerRowIssues(self, productContainerID):
        """
        Get a product container row issues

        Args:
            productContainerID (integer): REQUIRED

        Returns:
            json (dictionary): ProductContainer Resource
        """
        path = f"{self.baseURL}/ProductContainers/rowissues/{productContainerID}"
        response = self.get(path)
        return response


    def getProductContainerShoppingCart(self, orgID):
        """
        Get a product container shopping cart

        Args:
            orgID (integer): REQUIRED

        Returns:
            json (dictionary): ProductContainer Resource
        """
        path = f"{self.baseURL}/ProductContainers/getorcreateshoppingcart"
        params = {'OrganizationId': orgID}
        response = self.get(path, params)
        return response


    def deleteProductContainer (self, productcontainerID):
        """
        Delete a Product Container

        Args:
            productcontainerID: Required 

        Returns:
            status code (int): 200 success
        """
        path = f"{self.baseURL}/ProductContainers/{productcontainerID}"
        status_code = self.delete(path)
        return status_code


    '''
    # post prototype
    def create(self, schema):
        """
        Create a resource

        Args:
            schema (dictionary): required

        Returns:
            json: resource schema
        """
        path = f"{self.baseURL}"
        return self.post(path, schema)
    '''


    # DEPENDANT ON UNTESTED API METHOD
    def patchProductContainerRow(self, containerID, rowID, data):
        """
        Rename an Azure Subscription

        Args:
            containerID: Product Container ID; required
            rowID: required
            data (dictionary): ProductRowPatch Schema; required
        
        Returns:
            json (dictionary): ProductContainer Resource
        """
        path = f"{self.baseURL}/ProductContainers/{containerID}/row/{rowID}"
        return self._patch(path,data)


                            ####Programs####
    def getPrograms(self, filter=None):
        """
        Get a list of programs

        Args:
            filter (dictionary): optional

        Returns:
            json (dictionary): List of Program Resources
        """
        path = f"{self.baseURL}/Programs"
        return self.get(path, filter)
        

    def getProgram(self, programID):
        """
        Get a program

        Args:
            programID (integer): REQUIRED

        Returns:
            json (dictionary): Program Resource
        """
        path = f"{self.baseURL}/Programs/{programID}"
        response = self.get(path)
        return response


                            ####Publishers####
    def getPublishers(self, filter=None):
        """
        Get a list of publishers

        Args:
            filter (dictionary): optional

        Returns:
            json (dictionary): List of publisher Resources
        """
        path = f"{self.baseURL}/publishers"
        return self.get(path, filter)
        


    def getPublisher(self, publisherID):
        """
        Get a publisher

        Args:
            publisherID (integer): REQUIRED

        Returns:
            json (dictionary): publisher Resource
        """
        path = f"{self.baseURL}/publishers/{publisherID}"
        response = self.get(path)
        return response


                            ####Regions####
    def getRegions(self, filter=None):
        """
        Get a list of Regions

        Args:
            filter (dictionary): optional

        Returns:
            json (dictionary): List of Region Resources
        """
        path = f"{self.baseURL}/Regions"
        return self.get(path, filter)
        

    def getRegionByCode(self, regionCode):
        """
        Get a Region

        Args:
            regionCode (integer): REQUIRED

        Returns:
            json (dictionary): Region Resource
        """
        path = f"{self.baseURL}/Regions/bycode"
        params = {'regionCode': regionCode}
        response = self.get(path, params)
        return response


                            ####ResellerSalesPrices####

    '''
    # post prototype
    def create(self, schema):
        """
        Create a resource

        Args:
            schema (dictionary): required

        Returns:
            json: resource schema
        """
        path = f"{self.baseURL}"
        return self.post(path, schema)
    '''

    def deleteResellerSalesPrices (self, objectID, filter=None):
        """
        Delete Reseller Sales Prices

        Args:
            objectID: Required 
            filter (dictionary): optional

        Returns:
            status code (int): 200 success
        """
        params  = {"objectID": objectID}
        if(filter): params.update(filter)
        path = f"{self.baseURL}/ResellerSalesPrices"
        status_code = self.delete(path, params)
        return status_code

    '''
    # post prototype
    def create(self, schema):
        """
        Create a resource

        Args:
            schema (dictionary): required

        Returns:
            json: resource schema
        """
        path = f"{self.baseURL}"
        return self.post(path, schema)
    '''

                            ####Secrets####
    def createSecret(self, schema):
        """
        Create an API Client Secret

        Args: 
            schema (dictionary): Secret Schema; null unknown fields

        Returns:
            json (dictionary): Secret Schema
        """
        path = f"{self.baseURL}/Secrets"
        return self.post(path, schema)
        

 
    def deleteSecret (self, clientID, secretID):
        """
        Delete a API Client Secret

        Args:
            clientID: Required 
            secretID: Required

        Returns:
            status code (int): 200 success
        """
        path = f"{self.baseURL}/Secrets"
        params = {
            'clientID': clientID,
            'secretID': secretID
        }
        status_code = self.delete(path, params)
        return status_code


                            ####Subscriptions####
    def deleteSubscriptionTag (self, subscriptionID):
        """
        Delete a Subscription Tag

        Args:
            subscriptionID: Required 

        Returns:
            status code (int): 200 success
        """
        path = f"{self.baseURL}/Subscriptions/{subscriptionID}/tags"
        status_code = self.delete(path)
        return status_code

    '''
    # post prototype
    def create(self, schema):
        """
        Create a resource

        Args:
            schema (dictionary): required

        Returns:
            json: resource schema
        """
        path = f"{self.baseURL}"
        return self.post(path, schema)
    '''
    '''
    # post prototype
    def create(self, schema):
        """
        Create a resource

        Args:
            schema (dictionary): required

        Returns:
            json: resource schema
        """
        path = f"{self.baseURL}"
        return self.post(path, schema)
    '''
    '''
    # post prototype
    def create(self, schema):
        """
        Create a resource

        Args:
            schema (dictionary): required

        Returns:
            json: resource schema
        """
        path = f"{self.baseURL}"
        return self.post(path, schema)
    '''
    '''
    # post prototype
    def create(self, schema):
        """
        Create a resource

        Args:
            schema (dictionary): required

        Returns:
            json: resource schema
        """
        path = f"{self.baseURL}"
        return self.post(path, schema)
    '''
    '''
    # post prototype
    def create(self, schema):
        """
        Create a resource

        Args:
            schema (dictionary): required

        Returns:
            json: resource schema
        """
        path = f"{self.baseURL}"
        return self.post(path, schema)
    '''
    '''
    # post prototype
    def create(self, schema):
        """
        Create a resource

        Args:
            schema (dictionary): required

        Returns:
            json: resource schema
        """
        path = f"{self.baseURL}"
        return self.post(path, schema)
    '''
    '''
    # post prototype
    def create(self, schema):
        """
        Create a resource

        Args:
            schema (dictionary): required

        Returns:
            json: resource schema
        """
        path = f"{self.baseURL}"
        return self.post(path, schema)
    '''
    '''
    # post prototype
    def create(self, schema):
        """
        Create a resource

        Args:
            schema (dictionary): required

        Returns:
            json: resource schema
        """
        path = f"{self.baseURL}"
        return self.post(path, schema)
    '''
    

                            ####UsageCost####
    def getUsageCost(self, orgID, filter=None):
        """
        Get a Usage Cost

        Args:
            orgID (integer): REQUIRED
            filter (disctionary): time range

        Returns:
            json (dictionary): OrganizationUsageCost Resource
        """
        path = f"{self.baseURL}/UsageCost/organization/{orgID}"
        response = self.get(path, filter)
        return response

    '''
    # post prototype
    def create(self, schema):
        """
        Create a resource

        Args:
            schema (dictionary): required

        Returns:
            json: resource schema
        """
        path = f"{self.baseURL}"
        return self.post(path, schema)
    '''
    '''
    # post prototype
    def create(self, schema):
        """
        Create a resource

        Args:
            schema (dictionary): required

        Returns:
            json: resource schema
        """
        path = f"{self.baseURL}"
        return self.post(path, schema)
    '''
    '''
    # post prototype
    def create(self, schema):
        """
        Create a resource

        Args:
            schema (dictionary): required

        Returns:
            json: resource schema
        """
        path = f"{self.baseURL}"
        return self.post(path, schema)
    '''
    '''
    # post prototype
    def create(self, schema):
        """
        Create a resource

        Args:
            schema (dictionary): required

        Returns:
            json: resource schema
        """
        path = f"{self.baseURL}"
        return self.post(path, schema)
    '''
    '''
    # post prototype
    def create(self, schema):
        """
        Create a resource

        Args:
            schema (dictionary): required

        Returns:
            json: resource schema
        """
        path = f"{self.baseURL}"
        return self.post(path, schema)
    '''


                            ####Users####
    def getUsers(self, filter=None):
        """
        Get a list of Users

        Args:
            filter (dictionary): optional

        Returns:
            json (dictionary): List of User Resources
        """
        path = f"{self.baseURL}/Users"
        return self.get(path, filter)
        

    
    '''
    # post prototype
    def create(self, schema):
        """
        Create a resource

        Args:
            schema (dictionary): required

        Returns:
            json: resource schema
        """
        path = f"{self.baseURL}"
        return self.post(path, schema)
    '''


    def getUser(self, UserID):
        """
        Get a User

        Args:
            UserID (integer): REQUIRED

        Returns:
            json (dictionary): User Resource
        """
        path = f"{self.baseURL}/Users/{UserID}"
        response = self.get(path)
        return response


    def getUsername(self, username):
        """
        Get a User

        Args:
            Username (string): REQUIRED

        Returns:
            json (dictionary): User Resource
        """
        path = f"{self.baseURL}/Users/user"
        params = {'userName': username}
        response = self.get(path, params)
        return response


    def deleteUser (self, userID):
        """
        Delete a User

        Args:
            userID: Required 

        Returns:
            status code (int): 200 success
        """
        path = f"{self.baseURL}/Users/{userID}"
        status_code = self.delete(path)
        return status_code

   
    def createTenant(self, data):
        """
        Create a CSP tenant through the Cloud-IQ API
        Args: 
            data (dictionary): CustomerTenantDetailed Schema; null unknown/non-required fields
                Required Fields: https://apidocs.crayon.com/scenarios/customertenant-create.html
                Schema: https://apidocs.crayon.com/resources/CustomerTenantDetailed.html
        Returns:
            json (dictionary): CustomerTenantDetailed Schema
        """
        path = f"{self.baseURL}/CustomerTenants"
        return self.post(path, data)  


    def createSubscription(self, data):
        """
        Create a subscriptions for a product(license)
        Args: 
            data (dictionary): SubscriptionDetailed Schema; null unknown/non-required fields
                Required fields: https://apidocs.crayon.com/scenarios/subscription-create.html 
                Schema: https://apidocs.crayon.com/resources/SubscriptionDetailed.html
        Returns:
            json (dictionary): SubscriptionDetailed Schema
        """
        path = f"{self.baseURL}/Subscriptions"
        return self.post(path, data) 


    def createTenantAgreement(self, customerTenantId, data):
        """
        Create a Microsoft Consent Agreement for tenant
        Args: 
            data (dictionary): ServiceAccountAgreement Schema
        Returns:
            json (dictionary): ServiceAccountAgreement Schema
        """
        path = f"{self.baseURL}/customertenants/{customerTenantId}/agreements"
        return self.post(path, data) 


    #----------------------------- API SCHEMA ---------------------------------
    class CustomerTenantDetailed():
        """
        """
        def __init__(
            self,
            tenant_name,
            domain_prefix,
            org_id,
            invoice_profile_id, 
            contact_firstname,
            contact_lastname,
            contact_email,
            contact_phone,
            address_firstname,
            address_lastname,
            address_address,
            address_city,
            address_countrycode,
            address_region,
            address_zipcode,
            username=None,
            invoice_profile_name="Default", 
            tenant_type=1, 
            org_name=None,
            org_reg_number=None,
        ):
            self.tenant = {
                "Tenant": {
                    "Name": tenant_name,
                        "Publisher": {              
                            "Id": 2, 
                            "Name": "Microsoft"
                        },
                        "DomainPrefix": domain_prefix,
                        "Organization": {
                            "Id": org_id,             
                            "Name": org_name, 
                            "ParentId": 0
                        },
                        "InvoiceProfile": {
                            "Id": invoice_profile_id,             
                            "Name": invoice_profile_name     
                        },
                        "CustomerTenantType": tenant_type,  # T1=1, T2=2; All tenants will be T1 for this project according to Matt Clayton
                    },
                "Profile": {
                    "Contact": {
                        "FirstName": contact_firstname,
                        "LastName": contact_lastname,
                        "Email": contact_email,
                        "PhoneNumber": contact_phone
                    },
                    "Address": {
                        "FirstName": address_firstname,
                        "LastName": address_lastname,
                        "AddressLine1": address_address,
                        "City": address_city,
                        "CountryCode": address_countrycode,
                        "CountryName": None,
                        "Region": address_region,
                        "PostalCode": address_zipcode,
                    },
                },
                "Company": {
                    "OrganizationRegistrationNumber": org_reg_number   #null??
                },
                "User": {
                    "UserName": username,
                }
            }


    class CustomerTenantAgreement():
        """
        TEST: 
            1. date - leave it out or create it with time module 
            2. does this need to be done after every tenant is created?
        """
        def __init__(self,firstname,lastname,phone_number,email):
            self.agreement = {
                "firstName": firstname,
                "lastName": lastname,
                "phoneNumber": phone_number,
                "email": email,
                "dateAgreed": strftime('%Y-%m-%dT%H:%M:%S'),   
                "agreementType": 1                      
            }


    class SubscriptionDetailed():
        """
        """
        def __init__(self,name,tenant_id,part_number,quantity,billing_cycle,duration):
            self.subscription = {
                "name": name,
                "customerTenant": {
                    "id": tenant_id
                },
                "product": {
                    "partNumber": part_number
                },
                "quantity": quantity,
                "billingCycle": billing_cycle,
                "termDuration": duration 
            }