from netmiko import ConnectHandler


testing_device = {
    'device_type': 'cisco_ios',
    'host':   '192.168.56.102',
    'username': 'cisco',
    'password': 'cisco123!'
}


## Security Test: Is enable protected by a password?
def enable_secret():
    print("Running Security Test: Is enable protected by a password?")
    connect = ConnectHandler(**testing_device)
    command = connect.send_command('show running-config | section enable secret')

    print(f"I found:\n{command}\n\nResults:")

    if command.find("enable secret") != -1:
        print("Enable password has been configured")
    else:
        print("Enable password has not been configured")


## Security Test: Is SNMPv1 running with a public community string?
def snmpv1_public():
    print("Running Security Test: Is SNMPv1 running with a public community string?")
    connect = ConnectHandler(**testing_device)
    command = connect.send_command('show running-config | section snmp-server host')

    command_entries = command.split('\n')

    for entry in command_entries:
        print(f'I found: {entry}\nResults:')
        if entry.find(' public ') != -1:
            print('SNMP has been configured with a community string of "public"')
            if entry.find('version 2c') != -1:
                print('SNMP version 2c in use.')
            elif entry.find('version 3') != -1:
                print('SNMP version 3 in use.')
            else:
                print('SNMP version 1 in use.')
        else:
            print('Community string of public is not in use.')


## Security Test: Is Telnet enabled?
def telnet_check():
    print("Running Security Test: Is Telnet enabled?")
    connect = ConnectHandler(**testing_device)
    command = connect.send_command('show running-config | section line vty')

    print(f"I found:\n{command}\n\nResults:")

    if command.find(' telnet') != -1:
        print('Telnet has been configured!')
    elif command.find(' all') != -1:
        print('The All transport method is in use, this includes Telnet!')
    else:
        print('Telnet is not in use.')




# Main
#enable_secret()
#snmpv1_public()
#telnet_check()

print('Stevens crappy Python security tester\n')
perform_test = 0
while perform_test != range(1,3):
    perform_test = int(input(((
        '\nWhat test would you like perform?\n\n'
        '1 - Check if privileged exec password has been configured?\n'
        '2 - Check if SNMP is running with a community string of public and what version\n'
        '3 - Check if telnet is enabled\n'
    ))))
    if perform_test == 1:
        enable_secret()
    elif perform_test == 2:
        snmpv1_public()
    elif perform_test == 3:
        telnet_check()
    else:
        print("EXITING...")
        break