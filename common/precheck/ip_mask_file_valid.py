import os.path
import sys
from common.logging.LogModule import LogEntry
from common.ip_address_conversion_tools import ConvertCIDRtoMask

#Checking IP address file and content validity
def ip_mask_file_valid(ip_file,logging,log_file):

    global ip_list
    
    #Changing exception message
    if os.path.isfile(ip_file) == False:
        if logging == True:
            LogEntry('error',"IP file is missing!!!",log_file)
        print("\n* IP File {} does not exist :( Please check and try again.\n".format(ip_file))
        sys.exit()

    #Open user selected file for reading (IP addresses file)
    selected_ip_file = open(ip_file, 'r')
    
    #Starting from the beginning of the file
    selected_ip_file.seek(0)
    
    #Reading each line (IP address) in the file
    ips = selected_ip_file.readlines()
    
    ip_list=[]
    for ip in ips:
        ipaddr=ip[:ip.index("/")]
        cidr = ip[ip.index("/"):].rstrip("\n")
        mask = ConvertCIDRtoMask(cidr)
        
        ip_list.append({'IP':ipaddr,'MASK':mask})
    
    #Closing the file
    selected_ip_file.close()
        
    return ip_list