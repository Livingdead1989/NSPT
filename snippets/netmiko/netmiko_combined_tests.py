import getpass
import colorama
from colorama import Fore, Back, Style
from netmiko import ConnectHandler

colorama.init()

device_type = input(((
    'Supported devices:\n'
    'Vendor\t| Value\n'
    'Cisco\t| cisco_ios\n'
    'Enter device type: '
)))
device_host = input('Enter host IPv4 address (192.168.56.105): ')
device_username = input('Enter Username (cisco): ')
device_password = getpass.getpass(prompt='Enter password (cisco123!): ', stream=None)

testing_device = {
    'device_type': device_type,
    'host':   device_host,
    'username': device_username,
    'password': device_password
}

## Security Test: Is enable protected by a password?
def enable_secret():
    try:
        print('Running Security Test: Is enable protected by a password?')
        command = connect.send_command('show running-config | section enable secret')

        print(f'I found:\n{command}\n\nResults:')

        if command.find('enable secret') != -1:
            print(Fore.RED + 'Enable password has been configured correctly' + Style.RESET_ALL)
        else:
            print(Fore.GREEN + 'Enable password has not been configured' + Style.RESET_ALL)
    except:
        print(Fore.RED + 'There has been an error' + Style.RESET_ALL)


## Security Test: Is SNMPv1 running with a public community string?
def snmpv1_public():
    try:
        print('Running Security Test: Is SNMPv1 running with a public community string?')
        command = connect.send_command('show running-config | section snmp-server host')

        command_entries = command.split('\n')

        for entry in command_entries:
            print(f'I found: {entry}\nResults:')
            if entry.find(' public ') != -1:
                print(Fore.RED + 'SNMP has been configured with a community string of public' + Style.RESET_ALL)
                if entry.find('version 2c') != -1:
                    print('SNMP version 2c in use.\n')
                elif entry.find('version 3') != -1:
                    print('SNMP version 3 in use.\n')
                else:
                    print('SNMP version 1 in use.\n')
            else:
                print(Fore.GREEN + 'Community string of public is not in use.\n' + Style.RESET_ALL)
    except:
        print(Fore.RED + 'There has been an error' + Style.RESET_ALL)


## Security Test: Is Telnet enabled?
def telnet_check():
    try:
        print('Running Security Test: Is Telnet enabled?')
        command = connect.send_command('show running-config | section line vty')

        print(f'I found:\n{command}\n\nResults:')

        if command.find(' telnet') != -1:
            print(Fore.RED + 'Telnet has been configured!' + Style.RESET_ALL)
        elif command.find(' all') != -1:
            print(Fore.RED + 'The All transport method is in use, this includes Telnet!' + Style.RESET_ALL)
        else:
            print(Fore.GREEN + 'Telnet is not in use.' + Style.RESET_ALL)
    except:
        print(Fore.RED + 'There has been an error' + Style.RESET_ALL)




# Main
try:
    connect = ConnectHandler(**testing_device)
    print(Fore.GREEN + f'\nConnection to {device_host} established.\n' + Style.RESET_ALL)
except:
    print(Fore.RED + f'\nERROR: Unable to establish connection to device {device_host}.\n' + Style.RESET_ALL)
else:
    print(Fore.YELLOW + 'Python security tester\n' + Style.RESET_ALL)
    perform_test = 0
    while perform_test != range(1,3):
        perform_test = int(input(((
            '\nWhat test would you like perform?\n\n'
            '1 - Check if privileged exec password has been configured?\n'
            '2 - Check if SNMP is running with a community string of public and what version\n'
            '3 - Check if telnet is enabled\n'
            '4 - Exit\n'
        ))))


        if perform_test == 1:
            enable_secret()
        elif perform_test == 2:
            snmpv1_public()
        elif perform_test == 3:
            telnet_check()
        else:
            print(Fore.YELLOW + 'EXITING...' + Style.RESET_ALL)
            break