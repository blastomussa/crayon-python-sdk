from os import getenv
from cloudiq import CloudIQ

ID = getenv('CLIENT_ID')
SECRET = getenv('CLIENT_SECRET')
USER = getenv('CLOUDIQ_USER')
PASS = getenv('CLOUDIQ_PW')

orgID=123456

# Initialize API instance
crayon_api = CloudIQ(ID,SECRET,USER,PASS)

# product filter
# https://apidocs.crayon.com/resources/AgreementProductFilter.html
productFamilyName = 'Office 365'
filter = {
    'Include.ProductFamilyNames': productFamilyName
}

response = crayon_api.getAgreementProducts(orgID, filter)

# filter for successful calls 
if(int(response.status_code)  == 200):
    data = response.json()

    print("-----------------------------------------------------------")
    print("ProductName: PartNumber/SKU")
    print("-----------------------------------------------------------")
    # data['Items'] contains filtered product results
    for d in data['Items']:
        name = d['ProductVariant']['Product']['ItemLegalName']
        partNumber = d['ProductVariant']['Product']['PartNumber']
        print(name + ": " + partNumber)

        # list product families
        for d in data['ProductFamilies']:
            print(d['Key'])

        # list AgreementProductsCollection resource keys
        for d in data:
            print(d)

        # list getAgreementProducts() possible filters
        for d in data['Filter']:
            if(d == 'Include'):
                for i in data['Filter']['Include']:
                    print('Include.' + i)
            elif(d == 'Exclude'):
                for e in data['Filter']['Exclude']:
                    print('Exclude.' + e)
            else: print(d)

        # list all returned Product Variants
        for d in data['Items']:
            print(d['ProductVariant'])

        # list all returned Products
        for d in data['Items']:
            print(d['ProductVariant']['Product'])
else:
    print(response.status_code)

