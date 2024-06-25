import requests
import common.ClearpassMethods as CP

# -------------------------------------------------------------------------------------- Login Configuration
clearpass_url = "https://rds-prod.burnsmcd.com"
client_id = "AutomationTest"
client_secret = "yqdRJr/9dq4xEYFDruQneJyeT47VyaQHXg7S0s/QbQ8c"

# -------------------------------------------------------------------------------------- NETWORK DATA
Description="JamesTestDevice"
NetworkName="JamesNetworkDevice"
IpAddress="5.5.5.0/20"
RadiusSecret="8F1yCYDuidup"
TacacsSecret="8F1yCYDuidup"
VendorName = "Aruba"
GroupID = "BMcD_Aruba_IAP"
GroupName = "JamesTestGroup"


# ====================================================================================== CLEARPASS SCRIPT CALLS
# -------------------------------------------------------------------------------------- Obtain access token
access_token = CP.get_access_token(clearpass_url, client_id, client_secret)

# -------------------------------------------------------------------------------------- Create Network Device
if access_token: # --------------------------------------------------------------------- Validate Authentication
    device_data = {
        "description": Description,
        "name": NetworkName,
        "ip_address": IpAddress,
        "radius_secret": RadiusSecret,
        "tacacs_secret": TacacsSecret,
        "vendor_name" : VendorName,
    }
    network_device = CP.create_network_device(clearpass_url, access_token, device_data)
    
    if network_device: # --------------------------------------------------------------- Validate Device Creation in Clearpass
#        print("Network device created successfully")
        print("Network Device - ",network_device['name'],network_device['id'])

        # ------------------------------------------------------------------------------ Get Device group id
        GroupID = CP.get_device_group_id(clearpass_url,access_token,GroupName) 
        print("Group Name     - ",GroupID['name'],GroupID['id'])
        # ------------------------------------------------------------------------------ Add device to group
        
        group_response = CP.add_device_to_group(clearpass_url, access_token, network_device['ip_address'], GroupID['id'],GroupID['value'])
        
        if group_response:
            print("Device added to group successfully")
            print(group_response)
        else:
            print("Failed to add device to group")

    else:
        print("Failed to create network device")

else:
    print("Could not obtain access token")
