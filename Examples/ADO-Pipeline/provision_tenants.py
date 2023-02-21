# Description: Automates the provisioning and licesning of Azure tenants through
# Crayon's Cloud-IQ API in an Azure Pipeline. Requires a csv saved in the working directory named tenants.csv, 
# populated with domain prefixes,tenant names, and license quantities. Outputs a csv named 
# admin_creds.csv containing admin credentials for newly created tenants. 
# This script can be modified to set any variable needed through tenants.csv

import csv
from os import getenv
from time import sleep
from cloudiq import CloudIQ

# Get ENV variables passed from Azure pipeline
# REQUIRES ENV VARIABLES TO BE SET BY SOME METHOD BEFORE SCRIPT IS RUN
ID = getenv('CLIENT_ID')
SECRET = getenv('CLIENT_SECRET')
USER = getenv('CLOUDIQ_USER')
PASS = getenv('CLOUDIQ_PW')

# Path to CSV files; just filename if in working directory
CSV_PATH = "tenants.csv"
ADMIN_CSV = "admin_creds.csv"

def main():
    # Initialize SDK
    crayon_api = CloudIQ(ID,SECRET,USER,PASS)

    # Loop through tenants in CSV file
    with open(CSV_PATH) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            
            # Set Unique Tenant Variables from CSV
            tenant_name = row["tenant_name"]
            domain_prefix = row["domain_prefix"]
            exo_quantity = row["exo_quantity"]

            # Intialize Tenant and Agreement objects
            tenant = crayon_api.CustomerTenantDetailed(
                tenant_name=tenant_name,
                domain_prefix=domain_prefix,
                org_id=111111,
                org_name="Fake Org",
                invoice_profile_id=80408, # Default
                contact_firstname="First",
                contact_lastname="Last",
                contact_email="email@example.com",
                contact_phone="5555555555",
                address_firstname="First",
                address_lastname="Last",
                address_address="75 NoWhere Lane",
                address_city="Boston",
                address_countrycode="US",
                address_region="MA",
                address_zipcode="02109"
            )

            agreement = crayon_api.CustomerTenantAgreement(
                firstname="First",
                lastname="Last",
                phone_number="5555555555",
                email="email@example.com"
            )

            #Create New Tenant
            new_tenant = crayon_api.create_tenant(tenant.tenant)
            print(new_tenant)

            # Parse Admin Credentials and write to CSV
            admin = [[tenant_name,domain_prefix,new_tenant["User"]["UserName"],new_tenant["User"]["Password"]]]
            with open(ADMIN_CSV, 'a') as csvfile: 
                csvwriter = csv.writer(csvfile) 
                csvwriter.writerows(admin)

            # Agree to Microsoft Customer Agreement
            tenant_id = new_tenant["Tenant"]["Id"]  
            agree = crayon_api.create_tenantagreement(tenant_id,agreement.agreement)
            print(agree)

            # Create Subscription objects
            azure_subscription = crayon_api.SubscriptionDetailed(
                name="Azure P2 Subscription",
                tenant_id=tenant_id,
                part_number="CFQ7TTC0LFK5:0001",
                quantity=1,
                billing_cycle=1,
                duration="P1M"
            )

            exo_subscription = crayon_api.SubscriptionDetailed(
                name="Exchange Online Subscription",
                tenant_id=tenant_id,
                part_number="CFQ7TTC0LH16:0001",
                quantity=int(exo_quantity),
                billing_cycle=2,
                duration="P1Y"
            )

            # Create Azure P2 Subsription
            sub = crayon_api.create_subscription(azure_subscription.subscription)
            print(sub)

            # Create EXO Subsription
            sub = crayon_api.create_subscription(exo_subscription.subscription)
            print(sub)

            # Sleep to stay under API rate limit
            sleep(1)


if __name__ == "__main__":
    main()
