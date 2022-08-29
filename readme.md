# Crayon CloudIQ SDK for Python

This project is an SDK for Crayon's CloudIQ API that can be used in Python
scripts and applications. Provides a simple interface to test Cloud IQ API calls
with python for individuals who are inexperienced in C#.

**As of right now, this is a non-destructive test suite that _only provides the GET
REST method._ PUT, POST, and DELETE will be implemented at a later date.**

## Installation

1. Clone the repository using the following command:
	```
	git clone https://github.com/blastomussa/crayon-python-sdk.git
	```

2. Navigate to the root directory of the project and run:
	```
	pip install -r requirements.txt
	```

3. Copy cloudiqSDK.py to the root directory of an existing project.

4. Import the CloudIQ class from cloudiq.py using the following command:
	```
	from cloudiqSDK import CloudIQ
	```

5. Initialize an instance of the CloudIQ class with valid user credentials:
	```
	CLIENT_ID = xxxxxxx-xxxx-xxxx-xxxx-xxxxxx
	CLIENT_SECRET = xxxxxxx-xxxx-xxxx-xxxx-xxxxxx
	USERNAME = example@example.com
	PASSWORD = Password123456

	crayon_api = CloudIQ(CLIENT_ID,CLIENT_SECRET,USERNAME,PASSWORD)
	```

6. Make a test call to the API:
	```
	# retrieves all organizations associated with account
	response = crayon_api.getOrganizations()
	print(response)
	```

7. Make a raw GET request:
	```
	# retrieves all products in the Azure Active Directory product family within Org 123456
	params = {
		'OrganizationId': 123456,
		'Include.ProductFamilyNames': 'Azure Active Directory'
	}
	response = crayon_api.get("https://api.crayon.com/api/v1/agreementproducts",params)
	print(response)
	```

8. Retrieve a valid authorization token:
	```
	response = crayon_api.getToken()
	print(response)
	```

## Example Scripts

In order to use the example scripts, open example-config.ini with your favorite
text editor. Replace the dummy credentials with the those of a registered API
user and **save the file as config.ini.**
```
python3 example-products.py
```

## Methods currently implemented in CloudIQ class

1. get()
2. getToken()
3. validateToken()
4. getOrganizations()
5. getAgreementProducts()

###  How to retrieve detailed docstring information on CloudIQ class

```
from cloudiqSDK import CloudIQ
help(cloudIQ)
```
