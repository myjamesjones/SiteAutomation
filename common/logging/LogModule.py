import logging 
import os
from datetime import datetime

#from PySimpleGUI.PySimpleGUI import MESSAGE_BOX_LINE_WIDTH


def LogEntry(Level,Message,LogFile):

    """
    :param Level:   info or error
    :type Level:    (str)
    :param Message: text of message to log
    :type Message:  (str)
    """
    
    today = datetime.now()
    logstamp = today.strftime("%d-%b-%y")
    #systemRoot=os.environ.get('TEMP')
    #script_dir=systemRoot
#    script_dir=os.path.dirname(os.path.realpath(__file__))    

    # logging.basicConfig(filename=f'{script_dir}\\Logs\\NetworkApp-{logstamp}.log', level=logging.INFO,
                        # format='%(asctime)s %(levelname)s %(name)s : %(message)s')

    logging.basicConfig(filename=f'{LogFile}\\NetworkApp-{logstamp}.log', level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(name)s : %(message)s')

    if Level == "info":
        logging.info(Message)
    elif Level == "error":
        logging.error(Message)
