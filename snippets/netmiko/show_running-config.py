from netmiko import ConnectHandler

cisco = {
    'device_type': 'aruba_os',
    'host':   '10.10.200.10',
    'username': 'manager',
    'password': 'Je55ica1'
}

connect = ConnectHandler(**cisco)

command = connect.send_command('show system')

print(f"\n {command} \n")

