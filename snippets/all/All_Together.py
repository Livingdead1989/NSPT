# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PyQt5_Sample.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets
from netmiko import ConnectHandler
from datetime import datetime
from time import time
import os.path


class Ui_MainWindow(object):

    # ======== Run Report Function ========
    def runReport(self):
        # Connection to Device
        cisco = {
            'device_type': 'cisco_ios',
            'host':   self.host_device_input.text(),
            'username': self.username_input.text(),
            'password': self.password_input.text()
        }
        connect = ConnectHandler(**cisco)
        
        
        # ======== Check Telnet Status Function ========
        def checkTelnet():
            command = connect.send_command('show running-config | include transport input')    
            if command.find(' telnet') != -1:
                print('Telnet   |   Telnet has been configured!\n')
                return 'Fail'
            elif command.find(' all') != -1:
                print('Telnet   |   The All transport method is in use, this includes Telnet!\n')
                return 'Fail'
            else:
                print('Telnet   |   Telnet is not in use.\n')
                return 'Pass'
                

        # ======== Check Privileged Exec Function ========
        def checkExec():
            command = connect.send_command('show running-config | include enable secret')
            if command.find('enable secret') != -1:
                print('Exec     |   Pass')
                return 'Pass'
            else:
                print('Exec     |   Fail... Enable password incorrectly configured.')
                return 'Fail'


        # ======== Check SNMP Function ========
        def checkSNMP():
            command = connect.send_command('show running-config | include snmp-server')
            command_entries = command.split('\n')
            failed_count = 0

            for entry in command_entries:
                if entry.find(' public ') != -1:
                    print('SNMP     |   has been configured with a community string of public')
                    if entry.find('version 2c') != -1:
                        print('SNMP     |   version 2c in use.')
                    elif entry.find('version 3') != -1:
                        print('SNMP     |   version 3 in use.')
                    else:
                        print('SNMP     |   version 1 in use.')
                        failed_count += 1
                else:
                    print('SNMP     |   Community string of public is not in use.')

            if failed_count >= 1:
                print(f'SNMP    |   Fail... {failed_count} failures detected')
                return 'Fail'
            elif failed_count == 0:
                print('SNMP     |   Pass')
                return 'Pass'


        # ======== Produce & Export Report ========
        def exportReport():
            now = datetime.now()
            timestamp_format = "%Y-%m-%d %H-%M"
            timestamp = now.strftime(timestamp_format)

            hostname = self.host_device_input.text()
            filename = f'Report - {timestamp} - Device - {hostname}'
            reportPath = os.path.join(self.save_report_location_input.text(), filename+'.txt')
            report = open(reportPath,'w')

            report.write(f'Device:\t\t{self.host_device_input.text()}\n\n')
            report.write(f'Timestamp:\t\t{timestamp}\n\n')
            if self.security_test_telnet_check.isChecked():
                report.write(f'Security Test: Is Telnet enabled?\tResult: {checkTelnet()}\n\n')
            if self.security_test_password_check.isChecked():
                report.write(f'Security Test: Is enable protected by a password?\tResult: {checkExec()}\n\n')
            if self.security_test_snmp_check.isChecked():  
                report.write(f'Security Test: Is SNMPv1 running with a public community string?\tResult: {checkSNMP()}\n\n')
            report.close()
            print(f'Report Exported to {self.save_report_location_input.text()}')
            sys.exit(app.exec_())
        
        exportReport()



    # ======== Setup of UI ========
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(632, 465)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 611, 351))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.inputs_layout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.inputs_layout.setContentsMargins(0, 0, 0, 0)
        self.inputs_layout.setObjectName("inputs_layout")
        self.security_test_layout = QtWidgets.QVBoxLayout()
        self.security_test_layout.setObjectName("security_test_layout")
        self.security_test_telnet_check = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.security_test_telnet_check.setObjectName("security_test_telnet_check")
        self.security_test_layout.addWidget(self.security_test_telnet_check)
        self.security_test_password_check = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.security_test_password_check.setObjectName("security_test_password_check")
        self.security_test_layout.addWidget(self.security_test_password_check)
        self.security_test_snmp_check = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.security_test_snmp_check.setObjectName("security_test_snmp_check")
        self.security_test_layout.addWidget(self.security_test_snmp_check)
        self.inputs_layout.addLayout(self.security_test_layout, 0, 3, 1, 1)
        self.host_device_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.host_device_label.setObjectName("host_device_label")
        self.inputs_layout.addWidget(self.host_device_label, 3, 0, 1, 1)
        self.device_type_combo = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.device_type_combo.setObjectName("device_type_combo")
        self.device_type_combo.addItem("")
        self.device_type_combo.addItem("")
        self.inputs_layout.addWidget(self.device_type_combo, 2, 3, 1, 1)
        self.username_input = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.username_input.setObjectName("username_input")
        self.inputs_layout.addWidget(self.username_input, 5, 3, 1, 1)
        self.password_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.password_label.setObjectName("password_label")
        self.inputs_layout.addWidget(self.password_label, 6, 0, 1, 1)
        self.ssh_port_input = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.ssh_port_input.setObjectName("ssh_port_input")
        self.inputs_layout.addWidget(self.ssh_port_input, 4, 3, 1, 1)
        self.security_test_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.security_test_label.setObjectName("security_test_label")
        self.inputs_layout.addWidget(self.security_test_label, 0, 0, 1, 1)
        self.password_input = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.password_input.setObjectName("password_input")
        self.inputs_layout.addWidget(self.password_input, 6, 3, 1, 1)
        self.host_device_input = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.host_device_input.setObjectName("host_device_input")
        self.inputs_layout.addWidget(self.host_device_input, 3, 3, 1, 1)
        self.ssh_port_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.ssh_port_label.setObjectName("ssh_port_label")
        self.inputs_layout.addWidget(self.ssh_port_label, 4, 0, 1, 1)
        self.device_type_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.device_type_label.setObjectName("device_type_label")
        self.inputs_layout.addWidget(self.device_type_label, 2, 0, 1, 1)
        self.username_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.username_label.setObjectName("username_label")
        self.inputs_layout.addWidget(self.username_label, 5, 0, 1, 1)
        self.save_report_location_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.save_report_location_label.setObjectName("save_report_location_label")
        self.inputs_layout.addWidget(self.save_report_location_label, 7, 0, 1, 1)
        self.save_report_location_input = QtWidgets.QLineEdit(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.save_report_location_input.sizePolicy().hasHeightForWidth())
        self.save_report_location_input.setSizePolicy(sizePolicy)
        self.save_report_location_input.setObjectName("save_report_location_input")
        self.inputs_layout.addWidget(self.save_report_location_input, 7, 3, 1, 1)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 370, 611, 61))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.buttons_layout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.buttons_layout.setContentsMargins(0, 0, 0, 0)
        self.buttons_layout.setObjectName("buttons_layout")
        self.run_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.run_button.setObjectName("run_button")
        self.buttons_layout.addWidget(self.run_button)
        self.reset_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.reset_button.setObjectName("reset_button")
        self.buttons_layout.addWidget(self.reset_button)
        self.exit_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.exit_button.setObjectName("exit_button")
        self.buttons_layout.addWidget(self.exit_button)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionExit = QtWidgets.QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionExport_as_JSON = QtWidgets.QAction(MainWindow)
        self.actionExport_as_JSON.setObjectName("actionExport_as_JSON")
        self.actionExport_as_CSV = QtWidgets.QAction(MainWindow)
        self.actionExport_as_CSV.setObjectName("actionExport_as_CSV")

        self.retranslateUi(MainWindow)
        # ======== Reset Form Functionality ========
        self.reset_button.clicked.connect(self.host_device_input.clear)
        self.reset_button.clicked.connect(self.ssh_port_input.clear)
        self.reset_button.clicked.connect(self.username_input.clear)
        self.reset_button.clicked.connect(self.password_input.clear)
        self.reset_button.clicked.connect(self.save_report_location_input.clear)

        # ======== Get Results Functionality ========
        self.run_button.clicked.connect(self.runReport)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.security_test_telnet_check, self.security_test_password_check)
        MainWindow.setTabOrder(self.security_test_password_check, self.security_test_snmp_check)
        MainWindow.setTabOrder(self.security_test_snmp_check, self.device_type_combo)
        MainWindow.setTabOrder(self.device_type_combo, self.host_device_input)
        MainWindow.setTabOrder(self.host_device_input, self.ssh_port_input)
        MainWindow.setTabOrder(self.ssh_port_input, self.username_input)
        MainWindow.setTabOrder(self.username_input, self.password_input)
        MainWindow.setTabOrder(self.password_input, self.save_report_location_input)
        MainWindow.setTabOrder(self.save_report_location_input, self.run_button)


    # ======= Rebuild of UI ========
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.security_test_telnet_check.setText(_translate("MainWindow", "Is Telnet Disabled?"))
        self.security_test_password_check.setText(_translate("MainWindow", "Is a privileged exec password set?"))
        self.security_test_snmp_check.setText(_translate("MainWindow", "Is SNMPv1 \"public\" in use?"))
        self.host_device_label.setText(_translate("MainWindow", "Host Device (IPv4 or Hostname)"))
        self.device_type_combo.setItemText(0, _translate("MainWindow", "Juniper JUNOS"))
        self.device_type_combo.setItemText(1, _translate("MainWindow", "Cisco IOS"))
        self.password_label.setText(_translate("MainWindow", "Password"))
        self.security_test_label.setText(_translate("MainWindow", "Security Tests"))
        self.ssh_port_label.setText(_translate("MainWindow", "SSH Port"))
        self.device_type_label.setText(_translate("MainWindow", "Device Type"))
        self.username_label.setText(_translate("MainWindow", "Username"))
        self.save_report_location_label.setText(_translate("MainWindow", "Save Report Location"))
        self.run_button.setText(_translate("MainWindow", "Run Security Tests"))
        self.reset_button.setText(_translate("MainWindow", "Reset"))
        self.exit_button.setText(_translate("MainWindow", "Exit"))
        self.actionExit.setText(_translate("MainWindow", "Exit"))
        self.actionExport_as_JSON.setText(_translate("MainWindow", "Export as JSON"))
        self.actionExport_as_CSV.setText(_translate("MainWindow", "Export as CSV"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
