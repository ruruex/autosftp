import os
import argparse
import json

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

def Main():
    '''
    Main function for argument build up and config file loading
    '''
    parser=argparse.ArgumentParser()
    parser.add_argument('-f','--filename',help='the upload/download file name')
    parser.add_argument('-l','--load',help='load the ip, credentails from the input')
    parser.add_argument('-a','--action',help='sftp actions, current support put, get')
     
    args = parser.parse_args()

    sftp_file = args.filename
    loaded_file = args.load
    sftp_action = args.action

    with open(loaded_file,'r') as config_file:
        config_dict = json.load(config_file)


    sftp_connect(config_dict['hostname'],config_dict['username'],config_dict['password'],config_dict['home_dir'],sftp_action,sftp_file)

    
if __name__ == '__main__':
    Main()