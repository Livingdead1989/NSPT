#!/usr/bin/python3

## Telnet Security Check Demo
import argparse
from telnetlib import Telnet

parser = argparse.ArgumentParser(description='ArgParse')
parser.add_argument('host', metavar='host', type=str, help='Enter your host device address')
args = parser.parse_args()

host = args.host

def telnetCheck(host, port=23):
    try:
        with Telnet(host, port) as tn:
            #tn.read_until(b'Username: ', timeout=2)
            tn.read_some()
            tn.close()
        return f'Telnet Enabled on {host}'
    except:
        return f'Telnet Disabled on {host}'

print(telnetCheck(host))