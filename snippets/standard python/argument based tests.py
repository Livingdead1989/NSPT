#!/usr/bin/python3

import argparse
from telnetlib import Telnet
from netmiko import ConnectHandler

parser = argparse.ArgumentParser(description='ArgParse')
parser.add_argument('host', metavar='host', type=str, help='Enter your host device address')
parser.add_argument('username', metavar='username', type=str, help='Enter your SSH username')
parser.add_argument('password', metavar='password', type=str, help='Enter your SSH password')
args = parser.parse_args()

host = args.host
username = args.username
password = args.password

##############################################################
##############################################################

def telnetCheck(host, port=23):
    try:
        with Telnet(host, port) as tn:
            tn.read_some()
            tn.close()
        return f'FAILED: Telnet Enabled on {host}'
    except:
        return f'PASSED: Telnet Disabled on {host}'

print(telnetCheck(host))

##############################################################
##############################################################

def privilegedCheck(host, username, password):

    testing_device = {
    'device_type': 'cisco_ios',
    'host':   host,
    'username': username,
    'password': password
    }

    connect = ConnectHandler(**testing_device)



        print(Fore.YELLOW + 'Running Security Test: Is enable protected by a password?' + Style.RESET_ALL)
        
        command = connect.send_command('show running-config | include enable secret')
    
        print('I found:\n' + Fore.CYAN + command + Style.RESET_ALL + '\n\nResults:')


        if 'enable secret' in command.lower(): ## check for keyword in command output
            print(Fore.GREEN + 'Enable password has been configured correctly\n' + Style.RESET_ALL)
            return 'Pass'
        elif 'error' in command.lower() or 'invalid' in command.lower(): ## check for error keywords in command output
            print(Fore.RED + 'There has been an error\n' + Style.RESET_ALL)
            return 'Error'
        else:
            print(Fore.RED + 'Enable password has not been configured\n' + Style.RESET_ALL)
            return 'Fail'
