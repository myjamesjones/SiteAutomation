import sys
import subprocess
import PySimpleGUI as sg
import logging 
from common.logging.LogModule import LogEntry
import concurrent.futures

#Checking IP reachability
def ip_reach(list,logging,log_file,threads):

    LineCount = sum(1 for line in list)
    status = 0
 
    with concurrent.futures.ThreadPoolExecutor(max_workers=threads) as executor:   
        ping_check = {executor.submit(subprocess.call,'ping %s -n 2' % (ip,), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL): ip for ip in list}

 
        for future in concurrent.futures.as_completed(ping_check):
            ip = ping_check[future]
            reachable=future.result()  
            
        if reachable == 0:
            status+=1
            #continue
            
        else:
            print('\n* {} not reachable :( Check connectivity and try again.'.format(ip))
            if logging == True:
                LogEntry('error',"{} not reachable :( Check connectivity and try again.'.format(ip)",log_file)
            sys.exit()

        sg.one_line_progress_meter_cancel(key='ReachibilityCheck')
        if logging == True:
            LogEntry('info',"All IP's reachable with ping",log_file)