#!/usr/bin/python3
import argparse
from datetime import datetime
from telnetlib import Telnet
from netmiko import ConnectHandler
from pysnmp.hlapi import getCmd, SnmpEngine, CommunityData, UdpTransportTarget, ContextData, ObjectType, ObjectIdentity

parser = argparse.ArgumentParser(description='ArgParse')
parser.add_argument('host', metavar='Host Address', type=str, help='Enter your host device address')
parser.add_argument('-d', metavar='Device Type', type=str, help='Enter your device type such as cisco_ios')
parser.add_argument('-u', metavar='Username', type=str, help='Enter your SSH username')
parser.add_argument('-p', metavar='Password', type=str, help='Enter your SSH password')
group = parser.add_mutually_exclusive_group()
group.add_argument('-r', '--report', action='store_true', help='Produce a text file report')
group.add_argument('-v', '--verbose', action='store_true', help='Do not print to standard output')
args = parser.parse_args() # -h for help

host = args.host
device_type = args.d
username = args.u
password = args.p

hpe_devices = ('aruba_os','aruba_osswitch','aruba_procurve','hp_comware','hp_procurve')

##############################################################
## TELNET TEST ###############################################

def telnetCheck(host, port=23):
    try:
        Telnet.open(host,port,timeout=3) ## Timeout to prevent large hang times
    except:
        return f'PASSED: Telnet Disabled on {host}'
    else:
        Telnet.close()
        return f'FAILED: Telnet Enabled on {host}'

##############################################################
## PRIVILEGE EXEC PASSWORD TEST ##############################

def privilegedCheck(host, username, password):

    try:
        testing_device = {
        'device_type': device_type.lower(),
        'host':   host,
        'username': username,
        'password': password
        }

        connect = ConnectHandler(**testing_device)
        if device_type.lower() in hpe_devices: ## Check for HPE devices which use a different syntax
            command = connect.send_command('show running-config | include password manager')
        else:
            command = connect.send_command('show running-config | include enable secret')
    except:
        return f'ERROR: connecting to device {host} using SSH.'
    else:
        if 'enable secret' or 'password manager' in command.lower(): ## check for keyword in command output
            return f'PASSED: Privilege Exec mode is protected by a password on {host}.'
        elif 'error' in command.lower() or 'invalid' in command.lower(): ## check for error keywords in command output
            return f'ERROR: There has been an error on {host}.'
        else:
            return f'FAILED: Privilege Exec does not have a password enabled on {host}.'

##############################################################
## SNMP TEST #################################################

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
## MAIN ######################################################

def main():
    telnet_result = telnetCheck(host)
    privileged_result = privilegedCheck(host, username, password)
    snmp_result = snmpCheck(host)
    
    if args.verbose:
        print('\nPython Security Tester\n')
        print(telnet_result)
        print(privileged_result)
        print(snmp_result)

    if args.report:
        report(telnet_result, privileged_result, snmp_result)

##############################################################
## REPORT ####################################################

def report(telnet_result, privileged_result, snmp_result):
    now = datetime.now()
    timestamp_format = "%Y-%m-%d %H-%M"
    timestamp = now.strftime(timestamp_format)

    report = open(f'Report - {timestamp} - Device - {host}.txt','w')
    report.write(f'Device:\t\t{host}\n')
    report.write(f'Timestamp:\t\t{timestamp}\n\n')
    report.write(f'Security Test: Is Telnet enabled?\nResult: {telnet_result}\n\n')
    report.write(f'Security Test: Is enable protected by a password?\nResult: {privileged_result}\n\n')
    report.write(f'Security Test: Is SNMPv1 running with a public community string?\nResult: {snmp_result}\n\n')
    report.close()


if __name__ == '__main__':
    main()