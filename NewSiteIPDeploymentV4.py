import logging
from sys import path
from sys import exit
import os
path.append(os.path.join(os.path.dirname(__file__), 'common'))
import math
import time
from requests.auth import HTTPBasicAuth
import urllib3
import customtkinter as tk
from tkinter import Button as btn
from tkinter import Listbox as lst
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter.messagebox import showinfo


path.append('..\\common')
import common.ClearpassMethods as CP
from common.EfficientIPMethods import GetSiteId
from common.EfficientIPMethods import GetSubnetListGUI
from common.EfficientIPMethods import CreateSubnet
from common.EfficientIPMethods import GetSubnetStartingIP
from common.EfficientIPMethods import UpdateParentName
from common.CreateStandardSubnetDefinitions import CreateStandardSubnets
from common.EfficientIPMethods import CreateDHCPPool
from common.EfficientIPMethods import GetDHCPScopeID
from common.EfficientIPMethods import UpdateDNS
from common.CreateStandardSubnetDefinitions import GetRegionDNS
from common.logging.LogModule import LogEntry
from common.errors import StandardErrorPopup

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
log_file=""

# --------------------------------------------------------- GUI Subroutines ------------------------------------------
def login_clicked():
    """ callback when the login button clicked """
    global User
    global Password
    global SiteCode
    global City
    global State
    global selectedsubnet
    User = EIP_User.get()
    Password = EIP_PWD.get()
    SiteCode = strSiteCode.get()
    City = strCity.get()
    State = strState.get()
    root.destroy()

def select_file():
    global log_file 
    log_file = fd.askdirectory(
        title='Log file destination'
    )

def items_selected(event):
    global selectedsubnetIndex
    global selectedsubnetValue
    selected_indices = listbox.curselection()
    selected_subnet = ",".join([listbox.get(i) for i in selected_indices])
    selectedsubnetValue = selected_subnet
    selectedsubnetIndex = selected_indices[0]
    root.destroy()


# ================================================================================================================ GUI FORM
tk.set_appearance_mode("dark")
tk.set_default_color_theme("dark-blue")
root =tk.CTk()

root.title('EfficientIP Script')
root.geometry('600x500+50+50')
root.resizable(True,True)

# Sign in frame
signin = tk.CTkFrame(root)
signin.pack(padx=10, pady=10, fill='x', expand=True)
regionFrame = tk.CTkFrame(root)
regionFrame.pack(padx=10, pady=10, fill='x', expand=True)
loginFrame = tk.CTkFrame(root)
loginFrame.pack(padx=60, pady=10, fill='x', expand=True)
logsFrame = tk.CTkFrame(root)
logsFrame.pack(padx=90, pady=10, fill='x', expand=True)


# User
EIP_User = tk.StringVar()
EIP_User_label = ttk.Label(signin, text="EIP_User:",font=("Helvetica",18))
EIP_User_label.pack(fill='x', expand=True)
EIP_User_entry = ttk.Entry(signin, textvariable=EIP_User,font=("Helvetica",18))
EIP_User_entry.pack(fill='x', expand=True)
EIP_User_entry.focus()

# EIP_PWD
EIP_PWD = tk.StringVar()
EIP_PWD_label = ttk.Label(signin, text="EIP_PWD:",font=("Helvetica",18))
EIP_PWD_label.pack(fill='x', expand=True)
EIP_PWD_entry = ttk.Entry(signin, textvariable=EIP_PWD, show="*",font=("Helvetica",18))
EIP_PWD_entry.pack(fill='x', expand=True)

# Site Code
strSiteCode = tk.StringVar()
strSiteCode = ttk.Label(signin, text="Site Code:",font=("Helvetica",18))
strSiteCode.pack(fill='x', expand=True)
strSiteCode = ttk.Entry(signin, textvariable=strSiteCode,font=("Helvetica",18))
strSiteCode.pack(fill='x', expand=True)

# City
strCity = tk.StringVar()
strCity = ttk.Label(signin, text="City:",font=("Helvetica",18))
strCity.pack(fill='x', expand=True)
strCity = ttk.Entry(signin, textvariable=strCity,font=("Helvetica",18))
strCity.pack(fill='x', expand=True)

# State
strState = tk.StringVar()
strState = ttk.Label(signin, text="State:",font=("Helvetica",18))
strState.pack(fill='x', expand=True)
strState = ttk.Entry(signin, textvariable=strState,font=("Helvetica",18))
strState.pack(fill='x', expand=True)

#------------------------------------------------------------------------------ Select Region for DNS
strRegion = tk.StringVar(value="Central")
regions = ["West","Central","East"]
regionVar1 = tk.CTkRadioButton(regionFrame,text="East",value="East",variable=strRegion,font=("Helvetica",18),corner_radius=1,)
regionVar1.pack()
regionVar2 = tk.CTkRadioButton(regionFrame,text="Central",value="Central",variable=strRegion,font=("Helvetica",18),corner_radius=1)
regionVar2.pack()
regionVar3 = tk.CTkRadioButton(regionFrame,text="West",value="West",variable=strRegion,font=("Helvetica",18),corner_radius=1)
regionVar3.pack()


#------------------------------------------------------------------------------ Select Log File
open_button = btn(logsFrame, text='Log File Destination',
                  command=select_file,
                  font=("Helvetica, 12"),
                  relief="raised",
                  bd=5,
                  )
open_button.pack(expand=True)

# login button
login_button = btn(loginFrame, text="Execute", 
                          command=login_clicked,
                          font=("Helvetica, 18"),
                          relief="raised",
                          bd=7,
                          )
login_button.pack(fill='x', expand=True, pady=10)

root.mainloop()

# ------------------------------------------------------------------------------------ End of Main Form -------------------------------

# ------------------------------------------------------------------------------------ Set Site Variables
EIP_User = User
EIP_PWD = Password
strSiteCode = SiteCode
strCity = City
strState = State

# ------------------------------------------------------------------------------------ Validate Form
logging == True
if log_file=="": logging=False

if EIP_User=='':
    if logging == True:
        LogEntry('error','No User ID entered!',log_file)
    StandardErrorPopup("What did you do?", "No User ID entered. Exiting...")
    exit()
    
if EIP_PWD=='':
    if logging == True:
        LogEntry('error','No Password entered!',log_file)
    StandardErrorPopup("What did you do?", "No Password entered. Exiting...")
    exit()

if strSiteCode=='':
    if logging == True:
        LogEntry('error','No Site Code entered!',log_file)
    StandardErrorPopup("What did you do?", "No Site Code entered. Exiting...")
    exit()
    
if strCity=='':
    if logging == True:
        LogEntry('error','No City entered!',log_file)
    StandardErrorPopup("What did you do?", "No Password entered. Exiting...")
    exit()

if strState=='':

    if logging == True:
        LogEntry('error','No State entered!',log_file)
    StandardErrorPopup("What did you do?", "No State entered. Exiting...")
    exit()


# ==================================================================================== EfficientIP Section

# ------------------------------------------------------------------------------------ Login Parameters
EIP_URL="https://efficientip.burnsmcd.com/rest/"
AUTH = HTTPBasicAuth(EIP_User,EIP_PWD)
headers = {
'cache-control': "no-cache"
}

# ------------------------------------------------------------------------------------ Get Site ID from SiteName
siteName="RFC1918"
siteId=GetSiteId(EIP_URL, AUTH, headers, siteName)

# ------------------------------------------------------------------------------------ Get List of Subnets named "OPEN"
subnetName="OPEN"
subnetSize = 4096 #/20
    
subnets=GetSubnetListGUI(EIP_URL, AUTH, headers, subnetName, subnetSize)

# ------------------------------------------------------------------------------------ Subnet Selection Form
radio_keys = []
for entry in subnets:
    cidr = str(32-int(math.log(int(entry['subnet_size']), 2)))
    field=entry["start_hostaddr"]+"/"+cidr
    radio_keys.append(field)

root = tk.CTk()

root.title('Select Range')
root.geometry('200x500+50+50')
root.resizable(True,True)

# Sign in frame
IPRangesMenu = tk.CTkFrame(root)
IPRangesMenu.grid(column=0, row=0)
#IPRangesMenu.pack(fill='x', expand=True)

var = tk.Variable(value=radio_keys)
listbox = lst(
    root,
    listvariable=var,
    height=30,
    font=("Helvetica",14),
    selectmode="single"
)
listbox.grid(column=0,row=0)
#listbox.pack(expand=True, fill=tk.BOTH)
listbox.bind('<<ListboxSelect>>', items_selected)
root.mainloop()

selectedsubnet = selectedsubnetIndex    
    
print(selectedsubnet)
# ------------------------------------------------------------------------------------ End of Subnet Form -----------------------

# ------------------------------------------------------------------------------------ get subnet id for selected subnet
strParentSubnetId = subnets[selectedsubnet]['subnet_id'] 
print(strParentSubnetId)

# ------------------------------------------------------------------------------------ Get Starting IP Number
parentSubnetId=int(strParentSubnetId)   
StartingIP = GetSubnetStartingIP(EIP_URL, AUTH, headers, parentSubnetId)
print()

# ------------------------------------------------------------------------------------ Get Standard Subnets
print("Getting standard subnet list")
print()
newSubnets = CreateStandardSubnets(StartingIP,strSiteCode)
    # --------------------- List Order
    # - SubnetName
    # - SubnetIP
    # - Subnet_Gateway
    # - DHCP Pool Name
    # - DHCP Start
    # - DHCP End
    # ---------------------------------

# ------------------------------------------------------------------------------------ Update Parent Name
strParentName = f"{strSiteCode} - {strCity}, {strState}"
UpdateParentName(EIP_URL,AUTH,headers,strParentName,strParentSubnetId,siteId)

# ------------------------------------------------------------------------------------ Create Subnets
print("Creating Subnets and dhcp pools")
for subnet in range(len(newSubnets)):
    Subnet_Name = newSubnets[subnet]["Name"]
    Subnet_IP = newSubnets[subnet]["Subnet_IP"]
    Network_prefix = newSubnets[subnet]["Prefix"]
    Subnet_Mask = newSubnets[subnet]["Mask"]
    Subnet_Gateway = newSubnets[subnet]["Subnet_Gateway"]
    DHCP_Pool_Name = newSubnets[subnet]["DHCP_Pool_Name"]
    DHCP_Start = newSubnets[subnet]["DHCP_Start_Addr"]
    DHCP_End = newSubnets[subnet]["DHCP_End_Addr"]

    print("Creating Subnet - ",Subnet_Name," - ",Subnet_IP)
    Subnet_ID = CreateSubnet(EIP_URL, AUTH, headers, Subnet_Name, Subnet_IP, Subnet_Gateway, Network_prefix, siteId, strParentSubnetId)

    DHCPScope_ID = GetDHCPScopeID(EIP_URL, AUTH, headers,Subnet_IP,Subnet_Mask)

    if Subnet_Name == strSiteCode+"-GUEST":
        DNS_1 = "208.67.222.222"
        DNS_2 = "208.67.220.220"
    else: 
        DNS_1,DNS_2 = GetRegionDNS(strRegion)

# ------------------------------------------------------------------------------------ Update DNS for Region                
    UpdateDNS(EIP_URL, AUTH, headers, DHCPScope_ID, DNS_1, DNS_2)

# ------------------------------------------------------------------------------------ Create DHCP Pools
    CreateDHCPPool(EIP_URL, AUTH, headers, DHCP_Start, DHCP_End, DHCP_Pool_Name, siteId)




# ==================================================================================== ClearPass Section
# -------------------------------------------------------------------------------------- Login Configuration
clearpass_url = "https://rds-prod.burnsmcd.com"
client_id = "AutomationTest"
client_secret = "yqdRJr/9dq4xEYFDruQneJyeT47VyaQHXg7S0s/QbQ8c"

# -------------------------------------------------------------------------------------- NETWORK DATA FOR CLEARPASS ----------------------------------
MerakiDescription="MerakiSwitches"
WirelessDescription="Wireless"
MerakiNetworkName=SiteCode + "SF-01-01"
WirelessNetworkName=SiteCode + "WirelessNet"
MerakiSubnet=newSubnets[6]['Subnet_IP']+"/"+str(newSubnets[6]['Prefix']) # Meraki Switch Subnet (see order in create CreateStandardSubnetDefinitions)
WirelessSubnet = newSubnets[1]['Subnet_IP']+"/"+str(newSubnets[1]['Prefix']) # Wireless Mgmt Subnet (see order in create CreateStandardSubnetDefinitions)
RadiusSecret="8F1yCYDuidup"
TacacsSecret="8F1yCYDuidup"
WirelessGroupName = "AMER-Wireless"
MerakiGroupName = "Meraki Switches"

CPData = [
    {"Description": MerakiDescription, "NetworkName":MerakiNetworkName , "IPAddress":MerakiSubnet,"GroupName":MerakiGroupName, "VendorName":"Meraki"},
    {"Description": WirelessDescription, "NetworkName":WirelessNetworkName , "IPAddress":WirelessSubnet,"GroupName":WirelessGroupName, "VendorName":"Cisco"}
]

# ====================================================================================== CLEARPASS SCRIPT CALLS
# -------------------------------------------------------------------------------------- Obtain access token
access_token = CP.get_access_token(clearpass_url, client_id, client_secret)

for entry in range(len(CPData)):
    # -------------------------------------------------------------------------------------- Create Network Device
    if access_token: # --------------------------------------------------------------------- Validate Authentication
        device_data = {
            "description": CPData[entry]['Description'],
            "name": CPData[entry]['NetworkName'],
            "ip_address": CPData[entry]['IPAddress'],
            "radius_secret": RadiusSecret,
            "tacacs_secret": TacacsSecret,
            "vendor_name": CPData[entry]['VendorName']
        }
        network_device = CP.create_network_device(clearpass_url, access_token, device_data)
        
        if network_device: # --------------------------------------------------------------- Validate Device Creation in Clearpass
    #        print("Network device created successfully")
            print("Network Device - ",network_device['name'],network_device['id'])
            print("Pausing 5 seconds")
            time.sleep(5) # ---------------------------------------------------------------- Add 5 second pause
            # ------------------------------------------------------------------------------ Get Device group id
            GroupID = CP.get_device_group_id(clearpass_url,access_token,CPData[entry]["GroupName"]) 
            print("Group Name     - ",GroupID['name'],GroupID['id'])
            # ------------------------------------------------------------------------------ Add device to group
            
            group_response = CP.add_device_to_group(clearpass_url, access_token, network_device['ip_address'], GroupID['id'],GroupID['value'])
            
            if group_response:
                print("Device added to group successfully")
            #    print(group_response)
            #    wait = input("Close Window?")
            #    print("The information on the screen is will not be saved.")
            #    wait = input("Are you sure?")
            else:
                print("Failed to add device to group")
                wait = input("Close Window?")

        else:
            print("Failed to create network device")
            wait = input("Close Window?")

    else:
        print("Could not obtain access token")
        wait = input("Close Window?")

