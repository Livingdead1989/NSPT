# Using Netmiko, connect to our Cisco router and extract if Telnet is enabled.
from netmiko import ConnectHandler

cisco = {
    'device_type': 'cisco_ios',
    'host':   '192.168.56.105',
    'username': 'cisco',
    'password': 'cisco123!'
}

connect = ConnectHandler(**cisco)

command = connect.send_command('show running-config | section line vty')

print(f"\n {command} \n")

if command.find(' telnet') != -1:
    print('Telnet Found!')
elif command.find(' all') != -1:
    print('All Found!')
else:
    print('Something else found!')
