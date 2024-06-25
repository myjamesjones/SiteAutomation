import requests
import json

# ====================================================================================== Obtain Access Token
def get_access_token(clearpass_url, client_id, client_secret):
    token_url = f"{clearpass_url}/api/oauth"
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    
    response = requests.post(token_url, data=payload)
    
    if response.status_code == 200:
        token_data = response.json()
        return token_data['access_token']
    else:
        print("Failed to obtain access token")
        print(response.status_code, response.text)
        return None


# ====================================================================================== Create a Network Device
def create_network_device(clearpass_url, access_token, device_data):
    api_url = f"{clearpass_url}/api/network-device"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    response = requests.post(api_url, headers=headers, json=device_data)
    
    if response.status_code == 201:
        return response.json()
    else:
        print("Failed to create network device")
        print(response.status_code, response.text)
        return None

# ====================================================================================== Get group id from group name
def get_device_group_id(clearpass_url, access_token, GroupName):
    api_url = f"{clearpass_url}/api/network-device-group/name/{GroupName}"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.get(api_url, headers=headers)
    
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to return device group")
        print(response.status_code, response.text)
        return response[id]





# ====================================================================================== Add network to group
def add_device_to_group(clearpass_url, access_token, IPAddress, group_id, value):
    add_device_url = f"{clearpass_url}/api/network-device-group/{group_id}"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    print("Current List:",value)
    value = value + ", " + IPAddress
    print("New List:",value)

    payload = {
        'value': value
    }

    response = requests.patch(add_device_url, headers=headers, data=json.dumps(payload))

    return response
