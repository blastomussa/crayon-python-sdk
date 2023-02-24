# **Crayon CloudIQ SDK for Python**

This project is an SDK for Crayon's CloudIQ API that can be used in Python
scripts and applications. Provides a simple interface for individuals who are
inexperienced in C# to test Cloud IQ API calls with Python.


MIT License: https://github.com/blastomussa/crayon-python-sdk/blob/master/LICENSE 

## **Installation**

1. Clone the repository using the following command:
	```
	pip install crayon-cloudiq-sdk
	```

2. Create a new python script

4. Import the CloudIQ class
	```
	from cloudiq import CloudIQ
	```

5. Initialize an instance of the CloudIQ class with valid user credentials:
	```
	from cloudiq import CloudIQ

	CLIENT_ID = xxxxxxx-xxxx-xxxx-xxxx-xxxxxx
	CLIENT_SECRET = xxxxxxx-xxxx-xxxx-xxxx-xxxxxx
	USERNAME = "example@example.com"
	PASSWORD = "Password123456"

	crayon_api = CloudIQ(CLIENT_ID,CLIENT_SECRET,USERNAME,PASSWORD)
	```
	**The prefered way of importing credentials is through ENV variables.**
	```
	from os import getenv
	from cloudiq import CloudIQ

	CLIENT_ID = getenv('CLIENT_ID')
	CLIENT_SECRET = getenv('CLIENT_SECRET')
	USERNAME = getenv('CLOUDIQ_USER')
	PASSWORD = getenv('CLOUDIQ_PW')

	crayon_api = CloudIQ(CLIENT_ID,CLIENT_SECRET,USERNAME,PASSWORD)
	```
	ENV variables can be set using various methods including injection if using containers and pipelines or through a secrets manager such as Azure KeyVault. To set them on a local system using bash run the following commands:
	```
	export CLIENT_ID="xxxxxxx-xxxx-xxxx-xxxx-xxxxxx"
	export CLIENT_SECRET="xxxxxxx-xxxx-xxxx-xxxx-xxxxxx"
	export USERNAME="example@example.com"
	export PASSWORD="Password123456"
	```
	An alternative method is to use a config.ini file containing the credentials and retrive them using the configparser module.
	```
	import configparser
	from cloudiq import CloudIQ

	# Parse configuration file
	try:
		config = configparser.ConfigParser()
		config.read('config.ini')
		ID = config['CRAYON_API']['ID']
		SECRET = config['CRAYON_API']['SECRET']
		USER = config['CRAYON_API']['USER']
		PASS = config['CRAYON_API']['PASS']
	except configparser.Error:
		print("Configuration Error...config.ini not found")
		exit()
	except KeyError:
		print("Configuration Error...configuration not found in config.ini")
		exit()

	crayon_api = CloudIQ(CLIENT_ID,CLIENT_SECRET,USERNAME,PASSWORD)
	```
	**SEE EXAMPLES FOLDER FOR AUTHENTICATION DEMONTRATIONS USING CONFIGPARSER, ENV VARIABLES, AND ADO PIPELINES**

6. Make a test call to the API:
	```
	# retrieves all organizations associated with account
	response = crayon_api.ping()
	print(response)

	response = crayon_api.me()
	print(response)
	```

7. Make a raw GET request:
	```
	# retrieves all products in the Azure Active Directory product family within Org 123456
	params = {
		'OrganizationId': 123456,
		'Include.ProductFamilyNames': 'Azure Active Directory'
	}
	# make a GET request to https://api.crayon.com/api/v1/AgreementProducts
	response = crayon_api.get("https://api.crayon.com/api/v1/AgreementProducts",params)
	print(response)
	```
	Data can be sent to the API as a standard Python dictionary object 

8. Retrieve a valid authorization token:
	```
	response = crayon_api.getToken()
	print(response)
	```

##  **How to retrieve detailed Docstring information on CloudIQ class**

```
from cloudiq import CloudIQ
help(CloudIQ)
```

## **Schema currently implemented in CloudIQ class**

1. CustomerTenantDetailed
2. CustomerTenantAgreement
3. SubscriptionDetailed


## **Methods currently implemented in CloudIQ class**

1. get()
2. ping()
3. me()
4. getToken()
5. validateToken()
6. getOrganizations()
7. getOrganization()
8. getOrganizationSalesContact()
9. getAgreementProducts()
10. getActivityLogs()
11. getOrganizationHasAccess()
12. getAddresses()
13. getAddress()
14. getSupportedBillingCycles()
15. getAgreements()
16. getAgreementReports()
17. getCustomerTenants()
18. getCustomerTenant()
19. getCustomerTenantDetails()
20. getCustomerTenantAzurePlan()
21. getCustomerTenantAgreements()
22. getBillingCycles()
23. getProductVariantBillingCycles()
24. getBillingCyclesNameDictionary()
25. getBillingStatements()
26. getGroupedBillingStatements()
27. getBillingStatementExcel()
28. getBillingStatementCSV()
29. getBillingStatementJSON()
30. getBlogItems()
31. getClients()
32. getClient()
33. getConsumers()
34. getConsumer()
35. getCrayonAccounts()
36. getCrayonAccount()
37. getGroupings()
38. getGrouping()
39. getInvoiceProfiles()
40. getInvoiceProfile()
41. getProductContainers()
42. getProductContainer()
43. getProductContainerRowIssues()
44. getProductContainerShoppingCart()
45. getPrograms()
46. getProgram()
47. getPublishers()
48. getPublisher()
49. getRegions()
50. getRegionByCode()
51. getUsers()
52. getUser()
53. getUsername()
54. getUsageCost()
55. delete()
56. patch() 
57. post()
58. put()
59. createClient()
60. deleteClient()
61. createTenant()
62. createSubscription()
63. createTenantAgreement

## **References**

1. Crayon API Documentation: https://apidocs.crayon.com/
2. Swagger UI (includes all valid schemas): https://api.crayon.com/docs/index.html

