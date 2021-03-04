## Multiple SNMP returned, need to split the lines and find content.

from netmiko import ConnectHandler

cisco = {
    'device_type': 'cisco_ios',
    'host':   '192.168.56.105',
    'username': 'cisco',
    'password': 'cisco123!'
}

connect = ConnectHandler(**cisco)

command = connect.send_command('show running-config | section snmp-server host')

# print(f'\n {command} \n====================\n')

command_entries = command.split('\n')

for entry in command_entries:
    print(f'I found: {entry}\nResults:')
    if entry.find(' public ') != -1:
        print('SNMP has been configured with a community string of "public"')
    else:
        print('Community string of "public" is not in use.')


    if entry.find('version 2c') != -1:
        print('SNMP version 2c in use.')
    elif entry.find('version 3') != -1:
        print('SNMP version 3 in use.')
    else:
        print('SNMP version 1 in use.')
    
    print("==========================\n")