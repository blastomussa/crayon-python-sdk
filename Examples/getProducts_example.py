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


print("-----------------------------------------------------------")
print("ProductName: PartNumber/SKU")
print("-----------------------------------------------------------")
# response['Items'] contains filtered prodcut results
for r in response['Items']:
    name = r['ProductVariant']['Product']['ItemLegalName']
    partNumber = r['ProductVariant']['Product']['PartNumber']
    print(name + ": " + partNumber)

'''
# list product families
for r in response['ProductFamilies']:
    print(r['Key'])

# list AgreementProductsCollection resource keys
for r in response:
    print(r)

# list getAgreementProducts() possible filters
for r in response['Filter']:
    if(r == 'Include'):
        for i in response['Filter']['Include']:
            print('Include.' + i)
    elif(r == 'Exclude'):
        for e in response['Filter']['Exclude']:
            print('Exclude.' + e)
    else: print(r)

# list all returned Product Variants
for r in response['Items']:
    print(r['ProductVariant'])

# list all returned Products
for r in response['Items']:
    print(r['ProductVariant']['Product'])
'''
