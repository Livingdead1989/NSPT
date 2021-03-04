from netmiko import ConnectHandler

cisco = {
    'device_type': 'cisco_ios',
    'host':   '192.168.56.105',
    'username': 'cisco',
    'password': 'cisco123!'
}

connect = ConnectHandler(**cisco)

command = connect.send_command('show running-config | begin Current configuration')

print(f"\n {command} \n")

