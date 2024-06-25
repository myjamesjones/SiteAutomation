import requests
from requests.auth import HTTPBasicAuth
import urllib.parse
from sys import path
from sys import exit
import logging
import json
from pprint import pprint
import math
import sys
path.append('..\\common')
from common.errors import StandardErrorPopup

def GetSiteId(EIP_URL, AUTH, headers, siteName):  #-------------------------------------------- Return SiteID for SiteName
    URLADDON = "ip_site_list"
    EIP_URL = EIP_URL + URLADDON
    parameters = {
        "WHERE": "site_name='{}'".format(siteName),
        #"limit": "1"
    }
    try:
        rest_answer = requests.get(EIP_URL,params=parameters,headers=headers,verify=False,auth=AUTH)
        myjson = {} # ----------------------------------------------------------- initialize dictionary
        myjson = rest_answer.json() # -------------------------------------------------- dump output to json dictionary
        siteID = myjson[0]["site_id"]
    except KeyError:
        StandardErrorPopup("No Sites Returned","Are you sure you entered you username/password correctly?")
        sys.exit()
    except:
        StandardErrorPopup("ERROR","Something went wrong attempting to get Site Code")
        sys.exit()
        
    return siteID
#==========================================================================================================================


def GetSubnetList(EIP_URL, AUTH, headers, subnetName, subnetSize): #-------------------------------------- Return subnets named OPEN
    URLADDON = "ip_block_subnet_list"
    EIP_URL = EIP_URL + URLADDON
    WHERE = "subnet_name='" + subnetName + "' AND subnet_size=" + str(subnetSize) + "AND is_terminal='0'"
    parameters = {
        "WHERE": WHERE
    #    "TAGS": "network.gateway"
	}
        
    try:
        rest_answer = requests.get(EIP_URL,params=parameters,headers=headers,verify=False,auth=AUTH)
        myjson = {} # ----------------------------------------------------------- initialize dictionary
        myjson = rest_answer.json() # -------------------------------------------------- dump output to json dictionary

        print("Subnet ID","Subnet","CIDR")
        for entry in myjson:
            cidr = str(32-int(math.log(int(entry['subnet_size']), 2)))
            print(entry["subnet_id"],entry["start_hostaddr"],"/"+cidr)
    except:
        StandardErrorPopup("No Subnets Returned","There may not be any appropriate sized subnets available.")
        sys.exit()



    return rest_answer 
#===============================================================================================================

def GetSubnetListGUI(EIP_URL, AUTH, headers, subnetName, subnetSize): #-------------------------------------- Return subnets named OPEN
    URLADDON = "ip_block_subnet_list"
    EIP_URL = EIP_URL + URLADDON
    WHERE = "subnet_name='" + subnetName + "' AND subnet_size=" + str(subnetSize) + "AND is_terminal='0'"
    parameters = {
        "WHERE": WHERE
    #    "TAGS": "network.gateway"
	}
        
    try:
        rest_answer = requests.get(EIP_URL,params=parameters,headers=headers,verify=False,auth=AUTH)
        myjson = {} # ----------------------------------------------------------- initialize dictionary
        myjson = rest_answer.json() # -------------------------------------------------- dump output to json dictionary
    except:
        StandardErrorPopup("No Subnets Returned","There may not be any appropriate sized subnets available.")
        sys.exit()

    return myjson 
#===============================================================================================================

def GetSubnetStartingIP(EIP_URL, AUTH, headers, parentSubnetId): #-------------------------------------- Return subnets named OPEN
    URLADDON = "ip_block_subnet_info"
    EIP_URL = EIP_URL + URLADDON
    parameters = {
        "subnet_id": parentSubnetId,
    #    "TAGS": "network.gateway"
    }
    
    try:
        rest_answer = requests.get(EIP_URL,params=parameters,headers=headers,verify=False,auth=AUTH)
        myjson = {} # ----------------------------------------------------------- initialize dictionary
        myjson = rest_answer.json() # -------------------------------------------------- dump output to json dictionary
        for entry in myjson:
            startingIP=entry["start_hostaddr"]

        print("Starting Subnet:",startingIP)
    except:
        StandardErrorPopup("Something is wrong","Could not find the starting IP of supernet")
        sys.exit()


    return startingIP
#===============================================================================================================



#=============================================================================================================== Update Parent Subnet Name
def UpdateParentName(EIP_URL, AUTH, headers, strParentName, StrParentSubnetId, siteId):
    URLADDON = "ip_subnet_add"
    EIP_URL = EIP_URL + URLADDON

    parameters = {
        "subnet_name": strParentName,
        "subnet_id": StrParentSubnetId,
        "site_name": siteId
	}
    
    try:
        rest_answer = requests.post(EIP_URL,params=parameters,headers=headers,verify=False,auth=AUTH)
    except:
        StandardErrorPopup("Could not update Parent Name","I could not update the parent's name.")
        sys.exit()

    return 


#===============================================================================================================
def CreateSubnet(EIP_URL, AUTH, headers, Subnet_Name, Subnet_IP, Subnet_Gateway, Network_prefix, siteId, StrParentSubnetId):

    URLADDON = "ip_subnet_add"
    EIP_URL = EIP_URL + URLADDON

#    param1 = "'dns_view_name=0&rev_dns_view_name=%23all&use_ipam_name=0&ipv6_mapping=0&dns_id=12&rev_dns_id=3&dns_update=1&dhcp_failover_name=failover-cloud-dhcp.burnsmcd.smart&dhcpstatic=0&__eip_description=&domain=burnsmcd.com&"
#    gateway = "gateway="+Subnet_Gateway
#    param2 = "&__eip_cloud_azure_rg_uid=&__eip_cloud_azure_vn_uid=&__eip_cloud_azure_region=&__eip_cloud_azure_tenant_uid=&__eip_cloud_azure_subnet_uid=&__eip_cloud_aws_vpc_uid=&__eip_cloud_aws_region=&__eip_cloud_aws_owner_uid=&__eip_cloud_aws_subnet_uid=&__eip_cloud_aws_az=&domain_list=burnsmcd.com&dns_name=cor-dc-01-sc-us.burnsmcd.com&rev_dns_name=internal-dns.burnsmcd.smart&dhcpsn_name=&__eip_cloud_azure_subscription_uid='"
#    subnet_class_parameters = param1 + gateway + param2

    p01 = "dns_view_name=0"
    p02 = "rev_dns_view_name=%23all"
    p03 = "use_ipam_name=0"
    p04 = "ipv6_mapping=0"
    p05 = "rev_dns_id=3"
    p06 = "dns_update=1"
    p07 = "dhcp_failover_name=failover-cloud-dhcp.burnsmcd.smart"
    p08 = "dhcpstatic=0"
    p09 = "__eip_description="
    p10 = "domain=burnsmcd.com"
    p11 = "gateway="+Subnet_Gateway
    p12 = "__eip_cloud_azure_rg_uid="
    p13 = "__eip_cloud_azure_region="
    p14 = "__eip_cloud_azure_tenant_uid="
    p15 = "__eip_cloud_azure_subnet_uid="
    p16 = "__eip_cloud_aws_vpc_uid="
    p17 = "__eip_cloud_aws_region="
    p18 = "__eip_cloud_aws_owner_uid="
    p19 = "__eip_cloud_aws_subnet_uid="
    p20 = "__eip_cloud_aws_az="
    p21 = "domain_list=burnsmcd.com&dns_name=cor-dc-01-sc-us.burnsmcd.com"
    p22 = "rev_dns_name=internal-dns.burnsmcd.smart"
    p23 = "__eip_cloud_azure_subscription_uid="
    amp = "&"
    subnet_class_parameters = "'" + p01 + amp + p02 + amp + p03 + amp + p04 + amp + p05 + amp + p06 + amp + p07 + amp + p08 + amp + p09 + amp + p10 + amp
    subnet_class_parameters = subnet_class_parameters + p11 + amp + p12 + amp + p13 + amp + p14 + amp + p15 + amp + p16 + amp + p17 + amp + p18 + amp + p19 + amp + p20 + amp
    subnet_class_parameters = subnet_class_parameters + p21 + amp + p22 + amp + p23 + "'"


    parameters = {
        "parent_subnet_id": StrParentSubnetId,
        "subnet_addr": Subnet_IP,
        "subnet_name": Subnet_Name,
        "subnet_prefix": Network_prefix,
        "subnet_class_parameters": subnet_class_parameters,
#        "site_name": siteId,
        "is_terminal": 1
	}    
    
    try:
        rest_answer = requests.post(EIP_URL,params=parameters,headers=headers,verify=False,auth=AUTH)
        myjson = {} # ----------------------------------------------------------- initialize dictionary
        myjson = rest_answer.json() # -------------------------------------------------- dump output to json dictionary
        Subnet_ID=myjson[0]["ret_oid"]
    except:
        StandardErrorPopup("Could not create Subnets","I could not create the subnets.")
        sys.exit()

    return Subnet_ID
#===============================================================================================================

def CreateDHCPPool(EIP_URL, AUTH, headers, DHCP_Start, DHCP_End, DHCP_Pool_Name, siteId):

    URLADDON = "ip_pool_add"
    EIP_URL = EIP_URL + URLADDON

    PoolClassParameters = "dns_view_name=0&rev_dns_view_name=%23all&use_ipam_name=0&ipv6_mapping=0&dns_id=12&rev_dns_id=3&dns_update=1&dhcp_failover_name=failover-cloud-dhcp.burnsmcd.smart&dhcpstatic=0&__eip_description=&dhcprange=1&domain=burnsmcd.com&gateway=10.88.242.1&__eip_cloud_azure_rg_uid=&__eip_cloud_azure_vn_uid=&__eip_cloud_azure_region=&__eip_cloud_azure_tenant_uid=&__eip_cloud_azure_subnet_uid=&__eip_cloud_aws_vpc_uid=&__eip_cloud_aws_region=&__eip_cloud_aws_owner_uid=&__eip_cloud_aws_subnet_uid=&__eip_cloud_aws_az=&dns_name=cor-dc-01-sc-us.burnsmcd.com&rev_dns_name=internal-dns.burnsmcd.smart&__eip_cloud_azure_subscription_uid=%27&'dns_view_name=0&__eip_cloud_gcp_project_uid=&__eip_cloud_gcp_network=&__eip_cloud_gcp_region=&__eip_cloud_gcp_subnetwork_uid=&__eip_cloud_gcp_subnetwork_unique_uid=&__eip_cloud_gcp_sync_uid=",

    parameters = {
        "start_addr": DHCP_Start,
        "end_addr": DHCP_End,
        "site_id": siteId,
        "pool_name": DHCP_Pool_Name,
        "pool_read_only": 0,
        "pool_class_parameters" : PoolClassParameters,
	}    

    try:    
        rest_answer = requests.post(EIP_URL,params=parameters,headers=headers,verify=False,auth=AUTH)
        myjson = {} # ----------------------------------------------------------- initialize dictionary
        myjson = rest_answer.json() # -------------------------------------------------- dump output to json dictionary
    except:
        StandardErrorPopup("Could not create Pools","I could not create the DHCP Pools")
        sys.exit()


    return rest_answer

#===============================================================================================================    

def GetDHCPScopeID(EIP_URL, AUTH, headers, Subnet_IP,Subnet_Mask):
    URLADDON = "dhcp_scope_list"
    EIP_URL = EIP_URL + URLADDON
    QUERYADDON = "?WHERE=dhcpscope_net_mask='{}'".format(Subnet_Mask)+"&WHERE=dhcpscope_net_addr='{}'".format(Subnet_IP)
    EIP_URL = EIP_URL + QUERYADDON
    parameters = {
        "WHERE": "dhcpscope_net_addr='{}'".format(Subnet_IP)+"& dhcpscope_net_mask='{}'".format(Subnet_Mask),
    #    "limit": "1"
    }
    try:
#       rest_answer = requests.get(EIP_URL,params=parameters,headers=headers,verify=False,auth=AUTH)
        rest_answer = requests.get(EIP_URL,headers=headers,verify=False,auth=AUTH)
        myjson = {} # ----------------------------------------------------------- initialize dictionary
        myjson = rest_answer.json() # -------------------------------------------------- dump output to json dictionary
        dhcpscope_ID = myjson[0]["dhcpscope_id"]
    except:
        StandardErrorPopup("DHCP Scope ID","I could not find the DHCP Scope ID")
        sys.exit()

    return dhcpscope_ID
#===============================================================================================================    

def UpdateDNS(EIP_URL, AUTH, headers, DHCPScope_ID, DNS_1, DNS_2):
    URLADDON = "dhcp_option_add"
    EIP_URL = EIP_URL + URLADDON
    DNS_Servers = DNS_1 + "," + DNS_2  # ------------------ %2c represents a ,
    parameters = {
        "dhcpscope_id": DHCPScope_ID,
        "dhcpoption_type": "scope",
        "dhcpoption_name": "option domain-name-servers", #------------ %20 represents a space
        "dhcpoption_value": DNS_Servers
    }

    try:
        rest_answer = requests.post(EIP_URL,params=urllib.parse.urlencode(parameters,safe=","),headers=headers,verify=False,auth=AUTH)
        myjson = {} # ----------------------------------------------------------- initialize dictionary
        myjson = rest_answer.json() # -------------------------------------------------- dump output to json dictionary
    except:
        StandardErrorPopup("Error updating DNS Server","I could not change the default DNS servers.")
        sys.exit()
    
    return myjson

def GetRegionDNS(Region):
    try:
        if Region == "West":
            DNS_1 = '10.242.4.108'
            DNS_2 = '10.245.4.108'
        elif Region == "Central":
            DNS_1 = '10.245.4.108'
            DNS_2 = '10.242.4.108'
        else:
            DNS_1 = '10.245.4.108'
            DNS_2 = '10.242.4.108'
    except:
        StandardErrorPopup("DNS Region error","Could not retrieve DNS servers for region.")
        sys.exit()

    return DNS_1,DNS_2
