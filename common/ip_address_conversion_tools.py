


def ConvertCIDRtoMask(cidr):
    match cidr:
        case "/32":
            mask = "255.255.255.255"
        case "/31":
            mask = "255.255.255.254"
        case "/30":
            mask = "255.255.255.252"
        case "/29":
            mask = "255.255.255.248"
        case "/28":
            mask = "255.255.255.240"
        case "/27":
            mask = "255.255.255.224"
        case "/26":
            mask = "255.255.255.192"
        case "/25":
            mask = "255.255.255.128"
        case "/24":
            mask = "255.255.255.0"
        case "/23":
            mask = "255.255.254.0"
        case "/22":
            mask = "255.255.252.0"
        case "/21":
            mask = "255.255.248.0"
        case "/20":
            mask = "255.255.240.0"
        case "/19":
            mask = "255.255.224.0"
        case "/18":
            mask = "255.255.192.0"
        case "/17":
            mask = "255.255.128.0"
        case "/16":
            mask = "255.255.0.0"
        case "/15":
            mask = "255.254.0.0"
        case "/14":
            mask = "255.252.0.0"
        case "/13":
            mask = "255.248.0.0"
        case "/12":
            mask = "255.240.0.0"
        case "/11":
            mask = "255.224.0.0"
        case "/10":
            mask = "255.192.0.0"
        case "/9":
            mask = "255.128.0.0"
        case "/8":
            mask = "255.128.0.0"
        case _:
            mask = "255.0.0.0"    

    return mask