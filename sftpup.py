from json.decoder import JSONDecodeError
import os
import argparse
import json
import datetime
import syslog

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

def write_log(basic_content, content,logfile_name):
    '''
    Write log to file and system syslog
    '''
    with open (logfile_name,'a') as logfileobj:
        logfileobj.write(content)
    
    syslog.openlog(ident='sftpup.py',facility=syslog.LOG_LOCAL0)
    try:
        syslog.syslog(syslog.LOG_NOTICE,basic_content)
    except TypeError:
        raise Exception(basic_content)

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
        file_size = round(os.path.getsize(sftp_file)/1024/1024,2) # in MBytes
    else:
        os._exit('file does not exits')

    try:
        with open(loaded_file,'r') as config_file:
            config_dict = json.load(config_file)
    except IOError:
        print('Config file not exists')
    except JSONDecodeError:
        print('Config file JSON decode error, check your format')

    starttime = datetime.datetime.now()
    sftp_connect(config_dict['hostname'],config_dict['username'],config_dict['password'],config_dict['home_dir'],sftp_action,sftp_file)
    endtime = datetime.datetime.now()
    duration = endtime - starttime
    #print(f'The {sftp_action} takes: {duration}')

    # Calc avgerage throughput
    avg_speed = round(file_size*8/duration.total_seconds(),2)

    log_time = datetime.datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    machine_timezone = datetime.datetime.now(datetime.timezone.utc).astimezone().tzname()
    #print(f'Local time is {local_time}')

    # basic_log_str for syslog, log_str for log file
    basic_log_str = f"{config_dict['hostname']}{config_dict['home_dir']} {sftp_action} {sftp_file} size:{file_size}MBytes takes: {duration} average throughput is {avg_speed}mbps\n"
    log_str = f"{log_time} {machine_timezone} sftpup.py: " + basic_log_str
    write_log(basic_log_str,log_str,'sftp.log',)

    
if __name__ == '__main__':
    Main()