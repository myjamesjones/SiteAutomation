


def CreateStandardSubnets(startingSubnet,strSiteCode):
    int_Number_of_Subnets_in_Pods = 6
    totalNumberOfSubnets = 7
    names=[]
    names.append({"Name":strSiteCode+"-ADMIN","Prefix":24})  # ----------------------- Infrastructure Sunbnet
    names.append({"Name":strSiteCode+"-SERVERS","Prefix":24})
    names.append({"Name":strSiteCode+"-DATA","Prefix":23})
    names.append({"Name":strSiteCode+"-WIRELESS","Prefix":22})
    names.append({"Name":strSiteCode+"-GUEST","Prefix":22})
    names.append({"Name":strSiteCode+"-SECURITY","Prefix":24})
    names.append({"Name":strSiteCode+"-MERAKI","Prefix":24})
        

    # ----------------------------------------------------------------------------- Break Apart Master Subnet into Octets
    calculateOctet1 = startingSubnet.find(".")
    calculateOctet2 = startingSubnet.find(".",calculateOctet1+1)
    calculateOctet3 = startingSubnet.find(".",calculateOctet2+1)

    FirstOctet = startingSubnet[:calculateOctet1]
    SecondOctet = startingSubnet[calculateOctet1+1:calculateOctet2]
    ThirdOctet  = startingSubnet[calculateOctet2+1:calculateOctet3]
    FourthOctet = startingSubnet[calculateOctet3+1:]
    
    StartThirdOctet = int(ThirdOctet)

    newSubnets = []
    
    
    x = range(totalNumberOfSubnets)
 
    thirdOctet = StartThirdOctet
    FourthOctet =  "0"
    fourthOctetGW = "1"
    
    print('{0:30}{1:15}{2:<15}{3:15}{4:40}{5:15}{6:15}'.format("Subnet_Name","Subnet_IP","Subnet_Prefix","Subnet_Gateway","DHCP_Pool_Name","DHCP_Start","DHCP_End"))    
    for n in range(totalNumberOfSubnets):
        
        Subnet_Name = names[n]["Name"]
        Subnet_Prefix = names[n]["Prefix"]
        if Subnet_Prefix == 24:
            dhcp_end_third_octet = thirdOctet
            Subnet_Mask = "255.255.255.0"
        elif Subnet_Prefix == 23:
            dhcp_end_third_octet = thirdOctet + 1
            Subnet_Mask = "255.255.254.0"    
        else:
            dhcp_end_third_octet = thirdOctet + 3
            Subnet_Mask = "255.255.252.0"
            
        Subnet_IP = FirstOctet + "." + SecondOctet + "." +str(thirdOctet) + "." + FourthOctet
        Subnet_Gateway = FirstOctet + "." + SecondOctet + "." +str(thirdOctet) + "." + str(fourthOctetGW)
        DHCP_Pool_Name = names[n]["Name"]+"_Pool"
        DHCP_Start = FirstOctet + "." + SecondOctet + "." +str(thirdOctet) + ".10"
        DHCP_End = FirstOctet + "." + SecondOctet + "." +str(dhcp_end_third_octet) + ".200"
                
        newSubnets.append({"Name":Subnet_Name,"Subnet_IP":Subnet_IP,"Prefix":Subnet_Prefix,"Mask":Subnet_Mask,"Subnet_Gateway":Subnet_Gateway,"DHCP_Pool_Name":DHCP_Pool_Name, "DHCP_Start_Addr":DHCP_Start,"DHCP_End_Addr":DHCP_End})
        
        thirdOctet = dhcp_end_third_octet + 1
    
        print('{0:30}{1:15}{2:<15}{3:15}{4:40}{5:15}{6:15}'.format(Subnet_Name,Subnet_IP,Subnet_Prefix,Subnet_Gateway,DHCP_Pool_Name,DHCP_Start,DHCP_End))
    

    return newSubnets

