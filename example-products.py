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
    orgID = config['CRAYON_API']['orgID']
except configparser.Error:
    print("Configuration Error...config.ini not found")
    exit()
except KeyError:
    print("Configuration Error...configuration not found in config.ini")
    exit()

# Initialize API instance
crayon_api = CloudIQ(ID,SECRET,USER,PASS)

# product filter
# https://apidocs.crayon.com/resources/AgreementProductFilter.html
productFamilyName = 'Intune'
filter = {
    'Include.ProductFamilyNames': productFamilyName
}

response = crayon_api.getAgreementProducts(orgID, filter)

# response['Items'] contains filtered prodcut results
for r in response['Items']:
    name = r['ProductVariant']['Product']['ItemLegalName']
    partNumber = r['ProductVariant']['Product']['PartNumber']
    print(name + ": " + partNumber)

for r in response['Items']:
    print(r['ProductVariant']['Product'])

'''
# list product families
for r in response['ProductFamilies']:
    print(r)

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
