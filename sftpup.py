from json.decoder import JSONDecodeError
import os
import argparse
import json
import time

import pysftp

def sftp_connect(hostname,sftp_username,sftp_password,home_dir,sftp_action,sftp_file):
    '''
    SFTP module connect to remote and put/get file
    '''
    with pysftp.Connection(hostname, username=sftp_username, password=sftp_password) as sftp:
        with sftp.cd(home_dir):
            if sftp_action == 'get':        
                sftp.get(sftp_file)
            elif sftp_action == 'put':
                sftp.put(sftp_file)
            else:
                return 'wrong sftp_action'

def write_log(content,logfile_name):
    '''
    Write log to file
    '''
    with open (logfile_name,'a') as logfileobj:
        logfileobj.write(content)

def Main():
    '''
    Main function for argument build up and config file loading
    '''
    parser=argparse.ArgumentParser()
    parser.add_argument('-f','--filename',help='the upload/download file name')
    parser.add_argument('-l','--load',help='load the ip, credentails from the input')
    parser.add_argument('-a','--action',help='sftp actions, current support put, get')
     
    args = parser.parse_args()

    loaded_file = args.load
    sftp_action = args.action

    if os.path.isfile(args.filename):
        sftp_file = args.filename
    else:
        os._exit('file does not exits')

    try:
        with open(loaded_file,'r') as config_file:
            config_dict = json.load(config_file)
    except IOError:
        print('Config file not exists')
    except JSONDecodeError:
        print('Config file JSON decode error, check your format')

    starttime = time.time()
    sftp_connect(config_dict['hostname'],config_dict['username'],config_dict['password'],config_dict['home_dir'],sftp_action,sftp_file)
    endtime = time.time() # type - float
    duration = round((endtime - starttime),2)
    print(f'The {sftp_action} takes: {duration}')
    local_time = time.strptime(time.time(),)
    #print(f'Local time is {local_time}')

    log_str = f"{local_time} sftpup.py: {sftp_action} to {config_dict['hostname']} {config_dict['home_dir']} takes: {duration} seconds \n"
    write_log(log_str,'sftp.log')

    
if __name__ == '__main__':
    Main()