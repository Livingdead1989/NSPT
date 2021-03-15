from time import time
from datetime import datetime
from netmiko import ConnectHandler
import getpass
import colorama
from colorama import Fore, Back, Style
colorama.init()

print(Fore.YELLOW + 'Python security tester\n' + Style.RESET_ALL)

## User Input prompts
device_type = input(((
    'Supported devices:\n'
    'Vendor\t| Value\n'
    'Cisco\t| cisco_ios\n'
    'Enter device type: '
)))
device_host = input('Enter host IPv4 address (192.168.56.105): ')
device_username = input('Enter Username (cisco): ')
device_password = getpass.getpass(prompt='Enter password (cisco123!): ', stream=None)

## Hardcoded Inputs
# device_type = 'cisco_ios'
# device_host = '192.168.56.101'
# device_username = 'cisco'
# device_password = 'cisco123!'

testing_device = {
    'device_type': device_type,
    'host':   device_host,
    'username': device_username,
    'password': device_password
}

## Security Test: Is enable protected by a password?
def enable_secret():
    try:
        print(Fore.YELLOW + 'Running Security Test: Is enable protected by a password?' + Style.RESET_ALL)
        command = connect.send_command('show running-config | include enable secret')
        print('I found:\n' + Fore.CYAN + command + Style.RESET_ALL + '\n\nResults:')

        if command.find('enable secret') != -1:
            print(Fore.GREEN + 'Enable password has been configured correctly' + Style.RESET_ALL)
            return 'Pass'
        else:
            print(Fore.RED + 'Enable password has not been configured' + Style.RESET_ALL)
            return 'Fail'
    except:
        print(Fore.RED + 'There has been an error' + Style.RESET_ALL)


## Security Test: Is SNMPv1 running with a public community string?
def snmpv1_public():
    try:
        print(Fore.YELLOW + 'Running Security Test: Is SNMPv1 running with a public community string?' + Style.RESET_ALL)
        command = connect.send_command('show running-config | include snmp-server')
        command_entries = command.split('\n') # Splits the output by new line and adds to a list

        failed_count = 0

        for entry in command_entries:
            print('I found:\n' + Fore.CYAN + entry + Style.RESET_ALL + '\n\nResults:')
            
            if entry.find(' public ') != -1: # match was found, -1 is returned if no match was found using find, we reverse this using not equal !=
                print(Fore.RED + 'SNMP has been configured with a community string of public' + Style.RESET_ALL)
                if entry.find('version 2c') != -1:
                    print(Fore.GREEN + 'SNMP version 2c in use.\n' + Style.RESET_ALL)
                elif entry.find('version 3') != -1:
                    print(Fore.GREEN + 'SNMP version 3 in use.\n' + Style.RESET_ALL)
                else:
                    print(Fore.RED + 'SNMP version 1 in use.\n' + Style.RESET_ALL)
                    failed_count += 1 # if a failed result is found add 1 to the variable
            else:
                print(Fore.GREEN + 'Community string of public is not in use.\n' + Style.RESET_ALL)
            
            print(f'Number of failures: {failed_count}')

        # Fail marking, each line of config is evaluated seperately with an incrementing fail counter
        if failed_count >= 1:
            return 'Fail'
        elif failed_count == 0:
            return 'Pass'
        else:
            return 'Error'
            
    except:
        print(Fore.RED + 'There has been an error' + Style.RESET_ALL)


## Security Test: Is Telnet enabled?

def telnet_check():
    try:
        print(Fore.YELLOW + 'Running Security Test: Is Telnet enabled?' + Style.RESET_ALL)
        command = connect.send_command('show running-config | include transport input')

        print('I found:\n' + Fore.CYAN + command + Style.RESET_ALL + '\n\nResults:')

        if command.find(' telnet') != -1:
            print(Fore.RED + 'Telnet has been configured!' + Style.RESET_ALL)
            return 'Fail'
        elif command.find(' all') != -1:
            print(Fore.RED + 'The All transport method is in use, this includes Telnet!' + Style.RESET_ALL)
            return 'Fail'
        else:
            print(Fore.GREEN + 'Telnet is not in use.' + Style.RESET_ALL)
            return 'Pass'
    except:
        print(Fore.RED + 'There has been an error' + Style.RESET_ALL)




# Main
try:
    connect = ConnectHandler(**testing_device)
    print(Fore.GREEN + f'\nConnection to {device_host} established.\n' + Style.RESET_ALL)
except:
    print(Fore.RED + f'\nERROR: Unable to establish connection to device {device_host}. Please check your credentials.\n' + Style.RESET_ALL)
else:
    
    perform_test = 0
    
    # Time stamping
    now = datetime.now()
    timestamp_format = "%Y-%m-%d %H:%M"
    timestamp = now.strftime(timestamp_format)

    while perform_test != range(1,4):
        perform_test = input(((
            '\nWhat test would you like perform?\n\n'
            '1 - Check if privileged exec password has been configured?\n'
            '2 - Check if SNMP is running with a community string of public and what version\n'
            '3 - Check if telnet is enabled\n'
            '4 - Export Full Report\n'
            '5 - Exit\n\n'
        )))


        if perform_test == '1':
            enable_secret()
        elif perform_test == '2':
            snmpv1_public()
        elif perform_test == '3':
            telnet_check()
        elif perform_test == '4':
            report = open(f'Report - {timestamp} - Device - {device_host}.txt','w')
            report.write(f'Device:\t\t{device_host}\n')
            report.write(f'Timestamp:\t\t{timestamp}\n\n')
            report.write(f'Security Test: Is enable protected by a password?\n\tResult: {enable_secret()}\n\n')
            report.write(f'Security Test: Is SNMPv1 running with a public community string?\n\tResult: {snmpv1_public()}\n\n')
            report.write(f'Security Test: Is Telnet enabled?\n\tResult: {telnet_check()}\n\n')
            report.close()
            print(Fore.YELLOW + 'Report Created.' + Style.RESET_ALL)
        elif perform_test == '5':
            print(Fore.YELLOW + 'Exiting...' + Style.RESET_ALL)
            break
        else:
            print(Fore.RED + 'Please enter a selection from the menu.' + Style.RESET_ALL)