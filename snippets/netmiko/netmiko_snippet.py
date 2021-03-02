from netmiko import ConnectHandler

# Create a dictionary representing the device.
cisco_881 = {
    'device_type': 'cisco_ios',
    'host':   '10.10.10.10',
    'username': 'test',
    'password': 'password',
    'port' : 8022,          # optional, defaults to 22
    'secret': 'secret',     # optional, defaults to ''
}

# Establish an SSH connection to the device by passing in the device dictionary.
net_connect = ConnectHandler(**cisco_881)


# Execute show commands.
output = net_connect.send_command('show ip int brief')
print(output)

# Interface                  IP-Address      OK? Method Status                Protocol
# FastEthernet0              unassigned      YES unset  down                  down
# FastEthernet1              unassigned      YES unset  down                  down
# FastEthernet2              unassigned      YES unset  down                  down
# FastEthernet3              unassigned      YES unset  down                  down
# FastEthernet4              10.10.10.10     YES manual up                    up
# Vlan1                      unassigned      YES unset  down                  down


# Execute configuration change commands (will automatically enter into config mode)
config_commands = [ 'logging buffered 20000',
                    'logging buffered 20010',
                    'no logging console' ]
output = net_connect.send_config_set(config_commands)
print(output)

# pynet-rtr1#config term
# Enter configuration commands, one per line.  End with CNTL/Z.
# pynet-rtr1(config)#logging buffered 20000
# pynet-rtr1(config)#logging buffered 20010
# pynet-rtr1(config)#no logging console
# pynet-rtr1(config)#end

