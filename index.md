**COM617 Project Files - Network device Security Policy Tester application**

The aim of this project is to create a software solution to perform  the automated testing of network equipment to meet the company’s  security policies and to produce a report of the testing.

## Requirements

1. The application must perform automated network security tests.
   1. The tests must check the network device configuration for:
      - Telnet must be disabled
      - The enable password must be configured
      - The SNMP v1 community string should not be “Public”
   2. The user must be able to initiate the test manually
   3. The user must be able to dictate which devices are tested
2. The automated testing must produce a report of the test results showing whether each test passed or failed on each device
3. The platform must use open source software

## Used Python Packages

- os
- argparse
- datetime
- telnetlib
- netmiko
- pysnmp
- PyQt5
