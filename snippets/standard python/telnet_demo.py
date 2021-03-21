# Telnet Security Check Demo
from telnetlib import Telnet


def telnetCheck(host, port=23):
    try:
        with Telnet(host, port) as tn:
            #tn.read_until(b'Username: ', timeout=2)
            tn.read_some()
            tn.close()
        return f'Telnet Enabled on {host}'
    except:
        return f'Telnet Error on {host}'


print(telnetCheck('192.168.56.102'))