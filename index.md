# Brief Description

**Network device Security Policy Tester application**

COM617 project task, the aim of this project was to create a software solution to perform the automated testing of network equipment to meet the company’s security policies and to produce a report of the testing.

# Project Requirements

This project had a few requirements set by the problem giver, these were extracted from the provided document.

1. The application must perform network security tests automatically with minimal user input.
1. The tests must check the network device configuration for the following:
    * Telnet must be disabled.
    * The privilege exec must have a password configured.
    * SNMPv1 with a community string of 'public' must not be in use.
1.  The user must be able to initiate the test manually
1.  The user must be able to select which devices are tested
1.  The application must produce a report of the test results showing whether each test passed or failed on each device
1.  The platform must use open source software

# Windows Setup Guide

1. Install [Git](https://git-scm.com/download/win)
2. Install [Python](https://www.python.org/downloads/)
3. Install required modules using these commands
   1. `pip install netmiko`
   2. `pip install pysnmp`
4. Clone the GitHub repository `git clone https://github.com/livingdead1989/NSPT`
5. Move into the cloned repository using the command `cd NSPT/nspt`
6. Run the script help `python "cli argument based tests.py" -h`

**Demo**

![nspt-running-on-windows](nspt-running-on-windows.gif)

# Testing

We have tested this application on the following devices:

* Cisco CSR1000v
* Aruba JL256A 2930F
* HP J9729A 2920
* HP J8698A 5412 zl 

# Demonstration

A short demonstration of the CLI version in use, this showcases the help menu, a minimal test just using the device IP address, both verbose and report mode with custom report path. Included in the demonstration are good examples where all tests pass as well as showing error and case handling and failed devices.

<video controls src="demo_cli_arguments.m4v" style="width:100%;"></video>

Thank you for taking the time to view our project.
