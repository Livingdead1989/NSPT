import getpass
from netmiko import ConnectHandler

host = input("Host: ")
username = input("Username: ")
password = getpass.getpass(prompt="Enter password: ")

linux = {
    'device_type': 'linux',
    'host':   host,
    'username': username,
    'password': password,
}

net_connect = ConnectHandler(**linux)

hostname = net_connect.send_command('hostname')
print(f"\nHostname: {hostname}")

osrelease = net_connect.send_command('lsb_release -a')
print(f"\n {osrelease}")
