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
                try:
                    print(response.json())
                except requests.exceptions.JSONDecodeError:
                    print(response)
                exit(1)
            else:
                print(str(response.status_code) + " Error.")
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
        elif(self.tokenData['UnixExpiration'] > (int(time()) - 15)): #test for expiration
            self.getToken()
        else: pass
        return self.tokenData['AccessToken']


    #----------------------------- REST METHODS --------------------------------
    def get(self, url, params=None):
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
    # TODO: find resource that can be created and deleted easily;
    # TEST WITH: /api/v1/Clients
    def _post(self, path, data):
        pass


    # DO NOT IMPLEMENT YET
    # TODO: find resource that can be updated easily and non-destructively
    # TEST WITH: /api/v1/Clients/{clientID}
    def _put(self, path, data):
        pass


    # DO NOT IMPLEMENT YET
    # used by 2-3 endpoints
    def _patch(self, path, data):
        pass


    # DO NOT IMPLEMENT YET
    # TODO: find resource that can be created and deleted easily; least destructive
    # TEST WITH: /api/v1/Clients/{clientID}
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
        path = self.baseURL + 'Me'
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
        path = self.baseURL + 'ActivityLogs'
        params = {"Id": entityID}
        if(filter): params.update(filter)
        json = self.get(path, params)
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
        path = self.baseURL + 'organizations/' + str(orgID) + '/Addresses'
        json = self.get(path, filter)
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
        path = self.baseURL + 'organizations/' + str(orgID) + '/Addresses/' + str(addressID)
        json = self.get(path, filter)
        return json


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
        path = self.baseURL + 'AgreementProducts'
        params = {'OrganizationId': orgID}
        if(filter): params.update(filter)
        json = self.get(path, params)
        return json


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
        path = self.baseURL + 'AgreementProducts/'+ str(partNumber)+ '/supportedbillingcycles'
        json = self.get(path, params=filter)
        return json


                              ####Agreements####
    def getAgreements(self, filter=None):
        """
        Get Agreements

        Args:
            filter (dictionary): optional filter

        Returns:
            json (dictionary): Agreement Resource
        """
        path = self.baseURL + 'Agreements'
        json = self.get(path, filter)
        return json


    def getAgreementReports(self, productContainerId):
        """
        Get Agreement Reports

        Args:
            productContainerId (integer): REQUIRED

        Returns:
            json (dictionary): Agreement Report Resource
        """
        path = self.baseURL + 'AgreementReports/' + str(productContainerId)
        json = self.get(path)
        return json


                              ####Billing Cycles####
    def getBillingCycles(self, includeUnknown=False):
        """
        Get Billing Cycles

        Args:
            includeUnknown (boolean): optional filter

        Returns:
            json (dictionary): BillingCycle Resource
        """
        path = self.baseURL + 'BillingCycles'
        params = {'includeUnknown': includeUnknown}
        json = self.get(path, params)
        return json


    def getProductVariantBillingCycles(self, productVariantId):
        """
        Get Billing Cycles for a specific Product Variant

        Args:
            productVariantId (integer): REQUIRED

        Returns:
            json (dictionary): BillingCycle Resource
        """
        path = self.baseURL + 'BillingCycles/productVariant/' + str(productVariantId)
        json = self.get(path)
        return json


    def getBillingCyclesNameDictionary(self):
        """
        Get Billing Cycle CSP Name Dictionary

        Returns:
            json (dictionary): Billing Cycle Name Dictionary
        """
        path = self.baseURL + 'BillingCycles/cspNameDictionary'
        json = self.get(path)
        return json


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
        path = self.baseURL + 'BillingStatements'
        params = {'OrganizationId': orgID}
        if(filter): params.update(filter)
        json = self.get(path, params)
        return json


    def getGroupedBillingStatements(self, orgID, filter=None):
        """
        Get Billing Statements

        Args:
            orgID: organization ID; REQUIRED
            filter (dictionary): optional filter

        Returns:
            json (dictionary): GroupedBillingStatement Resource
        """
        path = self.baseURL + 'BillingStatements/grouped'
        params = {'OrganizationId': orgID}
        if(filter): params.update(filter)
        json = self.get(path, params)
        return json


    def getBillingStatementExcel(self, statementID):
        """
        Get Billing statement Excel file

        Args:
            statementID (integer): REQUIRED

        Returns:
            json (dictionary): byte array of excel file
        """
        path = self.baseURL + 'BillingStatements/file/' + str(statementID)
        json = self.get(path)
        return json


    def getBillingStatementCSV(self, statementID):
        """
        Get billing statement reconciliation file

        Args:
            statementID (integer): REQUIRED

        Returns:
            json (dictionary): byte array of CSV file
        """
        path = self.baseURL + 'BillingStatements/' + str(statementID) + '/reconciliationfile'
        json = self.get(path)
        return json


    def getBillingStatementJSON(self, statementID):
        """
        Get billing statement JSON file

        Args:
            statementID (integer): REQUIRED

        Returns:
            json (dictionary): byte array of JSON file
        """
        path = self.baseURL + 'BillingStatements/' + str(statementID) + '/billingrecordsfile'
        json = self.get(path)
        return json


                            ####Blog Items####
    def getBlogItems(self, filter=None):
        """
        Get Blog Items

        Args:
            orgID (integer): REQUIRED

        Returns:
            json (dictionary): BlogItem Resource
        """
        path = self.baseURL + 'BlogItems'
        json = self.get(path, filter)
        return json


                            ####Clients####
    def getClients(self, filter=None):
        """
        Get list of API Clients

        Args:
            filter (dictionary): optional

        Returns:
            json (dictionary): list of Client Resources
        """
        path = self.baseURL + 'Clients'
        json = self.get(path, filter)
        return json


    def getClient(self, clientID):
        """
        Get API Client

        Args:
            clientID (string): REQUIRED

        Returns:
            json (dictionary): Client Resource
        """
        path = self.baseURL + 'Clients/' + str(clientID)
        json = self.get(path)
        return json


    def _createClient(self):
        pass


    def _updateClient(self):
        pass


    def _deleteClient(self):
        pass


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
        path = self.baseURL + 'Consumers'
        params = {'OrganizationId': orgID}
        if(filter): params.update(filter)
        json = self.get(path, params)
        return json


    def getConsumer(self, consumerID):
        """
        Get Consumer

        Args:
            consumerID (integer): REQUIRED

        Returns:
            json (dictionary): Consumer Resource
        """
        path = self.baseURL + 'Consumers/' + str(consumerID)
        json = self.get(path)
        return json


    def _createConsumer(self):
        pass


    def _updateConsumer(self):
        pass


    def _deleteConsumer(self):
        pass


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
        path = self.baseURL + 'CrayonAccounts'
        params = {'OrganizationId': orgID}
        if(filter): params.update(filter)
        json = self.get(path, params)
        return json


    def getCrayonAccount(self, accountID):
        """
        Get Crayon Account

        Args:
            accountID (integer): REQUIRED

        Returns:
            json (dictionary): CrayonAccount Resource
        """
        path = self.baseURL + 'CrayonAccounts/' + str(accountID)
        json = self.get(path)
        return json


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
        path = self.baseURL + 'CustomerTenants/' + str(tenantID) + '/Agreements'
        params = {'AgreementTypeConsent': AgreementTypeConsent}
        json = self.get(path, params)
        return json



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
        path = self.baseURL + 'CustomerTenants'
        params = {'OrganizationId': orgID}
        if(filter): params.update(filter)
        json = self.get(path, params)
        return json


    def getCustomerTenant(self, tenantID):
        """
        Get a single customer tenant

        Args:
            tenantID (integer): REQUIRED

        Returns:
            json (dictionary): CustomerTenant Resource
        """
        path = self.baseURL + 'CustomerTenants/' + str(tenantID)
        json = self.get(path)
        return json


    def getCustomerTenantDetails(self, tenantID):
        """
        Get detailed information on a customer tenant

        Args:
            tenantID (integer): REQUIRED

        Returns:
            json (dictionary): CustomerTenantDetailed Resource
        """
        path = self.baseURL + 'CustomerTenants/' + str(tenantID) + '/detailed'
        json = self.get(path)
        return json


    def getCustomerTenantAzurePlan(self, tenantID):
        """
        Get the Azure plan associated with a customer tenant

        Args:
            tenantID (integer): REQUIRED

        Returns:
            json (dictionary): AzurePlan Resource
        """
        path = self.baseURL + 'CustomerTenants/' + str(tenantID) + '/AzurePlan'
        json = self.get(path)
        return json


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
        path = self.baseURL + 'Groupings'
        params = {'OrganizationId': orgID}
        if(filter): params.update(filter)
        json = self.get(path, params)
        return json


    def getGrouping(self, groupingID):
        """
        Get a grouping

        Args:
            groupingID (integer): REQUIRED

        Returns:
            json (dictionary): Grouping Resource
        """
        path = self.baseURL + 'Groupings/' + str(groupingID)
        json = self.get(path)
        return json


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
        path = self.baseURL + 'InvoiceProfiles'
        params = {'OrganizationId': orgID}
        if(filter): params.update(filter)
        json = self.get(path, params)
        return json

    # Returning None. Bug?
    def getInvoiceProfile(self, invoiceProfileID):
        """
        Get an InvoiceProfile

        Args:
            invoiceProfileID (integer): REQUIRED

        Returns:
            json (dictionary): InvoiceProfile Resource
        """
        path = self.baseURL + 'InvoiceProfiles/' + str(invoiceProfileID)
        json = self.get(path)


                            ####ManagementLinks####
    # snagged; need subscriptionID filter?
    def _getManagementLinks(self, filter=None):
        """
        Get a list of ManagementLinks

        Args:
            filter (dictionary): optional

        Returns:
            json (dictionary): List of ManagementLinks Resources
        """
        path = self.baseURL + 'ManagementLinks'
        json = self.get(path, filter)
        return json


    # 403 Forbidden Error message
    def _getGroupedManagementLinks(self, filter=None):
        """
        Get a list of ManagementLinks

        Args:
            filter (dictionary): optional

        Returns:
            json (dictionary): List of ManagementLinkGrouped Resources
        """
        path = self.baseURL + 'ManagementLinks/grouped'
        json = self.get(path, filter)
        return json


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
        path = self.baseURL + 'OrganizationAccess/grant'
        json = self.get(path, filter)
        return json


    # 'ErrorCode': '401 Unauthorized', 'Message': 'Invalid token'???
    def _getOrganizationAccess(self, filter=None):
        """
        Get a list of an organizations access grants.

        Args:
            filter (dictionary): optional

        Returns:
            json (dictionary): OrganizationAccess Resource
        """
        path = self.baseURL + 'OrganizationAccess'
        json = self.get(path, filter)
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
        path = self.baseURL + 'Organizations'
        json = self.get(path, filter)
        return json


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
        path = self.baseURL + 'Organizations/' + str(orgID)
        json = self.get(path)
        return json


    def getOrganizationSalesContact(self, orgID):
        """
        Get the Sales Contact for an organization

        Args:
            orgID (integer): organization ID; REQUIRED

        Returns:
            json (dictionary): OrganizationSalesContact Resource
        """
        path = self.baseURL + 'Organizations/' + str(orgID) + "/salescontact"
        json = self.get(path)
        return json


    def getOrganizationHasAccess(self, orgID):
        """
        Test if current API credentials have access to an organization

        Args:
            orgID (integer): organization ID; REQUIRED

        Returns:
            access (boolean): True or False
        """
        path = self.baseURL + "Organizations/HasAccess/" + str(orgID)
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
        path = self.baseURL + 'ProductContainers'
        params = {'OrganizationId': orgID}
        if(filter): params.update(filter)
        json = self.get(path, params)
        return json


    def getProductContainer(self, productContainerID):
        """
        Get a product containers

        Args:
            productContainerID (integer): REQUIRED

        Returns:
            json (dictionary): ProductContainer Resource
        """
        path = self.baseURL + "ProductContainers/" + str(productContainerID)
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
        path = self.baseURL + "ProductContainers/rowissues/" + str(productContainerID)
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
        path = self.baseURL + "ProductContainers/getorcreateshoppingcart"
        params = {'OrganizationId': orgID}
        response = self.get(path, params)
        return response


                            ####Programs####
    def getPrograms(self, filter=None):
        """
        Get a list of programs

        Args:
            filter (dictionary): optional

        Returns:
            json (dictionary): List of Program Resources
        """
        path = self.baseURL + 'Programs'
        json = self.get(path, filter)
        return json


    def getProgram(self, programID):
        """
        Get a program

        Args:
            programID (integer): REQUIRED

        Returns:
            json (dictionary): Program Resource
        """
        path = self.baseURL + "Programs/" + str(programID)
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
        path = self.baseURL + 'publishers'
        json = self.get(path, filter)
        return json


    def getPublisher(self, publisherID):
        """
        Get a publisher

        Args:
            publisherID (integer): REQUIRED

        Returns:
            json (dictionary): publisher Resource
        """
        path = self.baseURL + "publishers/" + str(publisherID)
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
        path = self.baseURL + 'Regions'
        json = self.get(path, filter)
        return json


    def getRegionByCode(self, regionCode):
        """
        Get a Region

        Args:
            regionCode (integer): REQUIRED

        Returns:
            json (dictionary): Region Resource
        """
        path = self.baseURL + "Regions/bycode"
        params = {'regionCode': regionCode}
        response = self.get(path, params)
        return response
