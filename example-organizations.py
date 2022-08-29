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

response = crayon_api.getOrganizations()
print(response)
