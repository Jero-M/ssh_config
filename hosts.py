#!/usr/bin/python
import csv
import os
import sys


from PyQt4 import QtCore, QtGui
from hosts_ui import Ui_HostsWindow


class StartUI(QtGui.QMainWindow):
    '''Build an instance of the GUI'''

    def __init__(self, parent=None):
        '''Initialize the interface with the correct settings'''
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_HostsWindow()
        self.ui.setupUi(self)

        self.hostnames = self.load_default_hostnames()
        self.add_all_hostnames_to_list()

    def load_default_hostnames(self):
        '''Load the default hostnames file'''
        local_path = os.path.dirname(os.path.realpath(__file__))
        default_hostnames = local_path + "/hostnames.csv"
        hostname_column = -1
        with open(default_hostnames, "rb") as csv_file:
            reader = csv.reader(csv_file)
            for i, column_name in enumerate(reader.next()):
                if column_name == "Hostname":
                    hostname_column = i
                    break
            return [hostname[hostname_column] for hostname in reader]

    def save_hostnames_to_file(self):
        '''Save the hostames to the default hostnames file'''

    def add_all_hostnames_to_list(self):
        '''Load all the hostnames into the list'''
        for hostname in self.hostnames:
            self.ui.list_hosts.addItem(hostname)


if __name__ == "__main__":
    # Create the GUI
    app = QtGui.QApplication(sys.argv)
    gui = StartUI()

    # Show the GUI
    gui.show()
    sys.exit(app.exec_())
