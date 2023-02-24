# Cloud-IQ API Tenant Provisioning via Azure Pipelines

## **Description**

This pipeline provisions new tenants to Microsoft via Crayon's Cloud-IQ API and assigns necessary licensing to the tenants. 
It uses a CSV file from a specified Azure blob as an input and outputs a csv file containing the temporary admin credentials of the tenants that were created to the same blob. The script currently assigns one Azure P2 Subscription and variable Exchange Online Subscriptions to each created tenant.

**This pipeline will fail if:** there are domain prefix collisions, the tenants.csv file can't be copied from the Blob, there are missing fields in tenants.csv, the admin_creds.csv file can't be uploaded to the Blob. 

___

## **Setup**

### **Create API Client Credentials**

1. Login to Cloud IQ
2. Choose Manage -> API Management from the top menu
3. Press the + Add Client button
4. Choose a name of the client
5. Choose Resource Flow as the authentication type
6. Save the Client ID and the Client Secret for use in the pipeline

### **Create Blob and SAS token**

1. Create a Blob in Azure
2. Create a Container inside the blob
3. Generate a SAS token for the container
4. Save the Container URL and the SAS Token for use in the pipeline

### **Create Pipeline**

1. In ADO, navigate to Pipelines
2. Create a new pipeline
3. Choose Azure Repo git
4. Choose the repository
5. Choose Existing Azure Pipline YAML file
6. Specify the azure_pipelines.yml file in the root directory of the respository. 
7. Save credentials to the ADO Pipeline Variables
    1. In the top right corner click the Variables button.
    2. Add the following variables. Save the values marked as **SECRET** as secret variables.
        * CLIENT_ID = Client ID from Cloud-IQ **SECRET**
        * CLIENT_SECRET = Client Secret from from Cloud-IQ **SECRET**
        * CLOUDIQ_USER = Username of Cloud-IQ admin user
        * CLOUDIQ_PW = Password for Cloud-IQ admin user **SECRET**
        * BLOB_URL = URL of Container
        * SAS_TOKEN = SAS token for container **SECRET**
8. Click the carrot symbol next to the Run button and choose Save.

### **Check Contact Information**

1. Open provision_tenants.py
2. Ensure that the contact details in the **crayon_api.CustomerTenantDetailed** and **crayon_api.CustomerTenantAgreement** objects are correct 
___

## **Provision Tenants**

### **Copy tenant.csv to Blob**

1. Create a CSV file called **tenants.csv** with the following header fields __Do not use leading spaces__
    ```
    tenant_name,domain_prefix,exo_quantity
    ```
2. Add tenant names, domain prefixes, and quantity of EXO licenses to the CSV file. Ex:
    ```
    tenant_name,domain_prefix,exo_quantity
    Test Tenant,apitest120938,6
    ```
3. Upload the CSV file to the Azure Blob container from the Setup section

### **Run the ADO Pipeline**

1. Navigate to Pipelines in Azure DevOps
2. Choose the previously created pipeline
3. Click the Run pipeline button in the top right corner to manually trigger the pipeline 

### **Retrieve Admin Credentials**

1. Navigate to the Azure blob container.
2. Download the admin_creds.csv file.
3. All temporary admin credentials from preceeding pipeline run will be in this file 