#!/usr/bin/python3

import argparse
from telnetlib import Telnet
from netmiko import ConnectHandler
from pysnmp.hlapi import getCmd, SnmpEngine, CommunityData, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity


parser = argparse.ArgumentParser(description='ArgParse')
parser.add_argument('device_type', metavar='device_type', type=str, help='Enter your device type')
parser.add_argument('host', metavar='host', type=str, help='Enter your host device address')
parser.add_argument('username', metavar='username', type=str, help='Enter your SSH username')
parser.add_argument('password', metavar='password', type=str, help='Enter your SSH password')
args = parser.parse_args()

device_type = args.device_type
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

##############################################################
##############################################################

def privilegedCheck(host, username, password):

    testing_device = {
    'device_type': device_type,
    'host':   host,
    'username': username,
    'password': password
    }

    connect = ConnectHandler(**testing_device)  
    command = connect.send_command('show running-config | include enable secret')

    if 'enable secret' in command.lower(): ## check for keyword in command output
        return f'PASSED: Privilege Exec has a password enabled on {host}.'
    elif 'error' in command.lower() or 'invalid' in command.lower(): ## check for error keywords in command output
        return f'ERROR: There has been an error on {host}.'
    else:
        return f'FAILED: Privilege Exec does not have a password enabled on {host}.'

##############################################################
##############################################################

def snmpCheck(host):
    iterator = getCmd(
        SnmpEngine(),
        CommunityData('public', mpModel=0), #mpModel=0 (SNMPv1), mpModel=1 (SNMPv2c)
        UdpTransportTarget((host, 161)),
        ContextData(),
        ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0))
    )

    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
    if errorIndication:
        # print(errorIndication)
        return f'PASSED: No SNMP response received before timeout on {host}.'
    elif errorStatus:
        # print('%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        return f'ERROR: There has been an error on {host}.'
    else:
        for varBind in varBinds:
            # print(' = '.join([x.prettyPrint() for x in varBind]))
            return f'FAILED: SNMP response received on {host}.'

##############################################################
##############################################################

print('Python Security Tester\n\n')

print(telnetCheck(host))
print(privilegedCheck(host, username, password))
print(snmpCheck(host))