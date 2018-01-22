#!/usr/bin/python
import csv
import os
import sys


from PyQt4 import QtCore, QtGui
from hosts_ui import Ui_HostsWindow


local_path = os.path.dirname(os.path.realpath(__file__))
default_hostnames = local_path + "/hostnames.csv"


class StartUI(QtGui.QMainWindow):
    '''Build an instance of the GUI'''

    def __init__(self, parent=None):
        '''Initialize the interface with the correct settings'''
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_HostsWindow()
        self.ui.setupUi(self)

        self.hostname_csv_column = -1
        self.hostnames_file = self.load_default_hostnames_file()
        self.add_all_hostnames_to_list()

        # Signal Handling
        QtCore.QObject.connect(self.ui.button_add,
                               QtCore.SIGNAL("clicked()"),
                               self.add_selected)

    def load_default_hostnames_file(self):
        '''Load the default hostnames file'''
        data = []
        with open(default_hostnames, "rb") as csv_file:
            reader = csv.reader(csv_file)
            for i, column_name in enumerate(reader.next()):
                if column_name == "Hostname":
                    self.hostname_csv_column = i
                    break
            for row in reader:
                data.append(row)
            return data

    def save_hostnames_to_file(self):
        '''Save the hostames to the default hostnames file'''
        with open(default_hostnames, "wb") as csv_file:
            writer = csv.writer(csv_file)
            for row in self.hostnames_file:
                writer.writerow(row)

    def add_all_hostnames_to_list(self):
        '''Load all the hostnames into the list'''
        for row in self.hostnames_file:
            self.ui.list_hosts.addItem(row[self.hostname_csv_column])

    def remove_selected(self):
        '''Remove the selected hostname/s from the list'''

    def add_selected(self):
        '''Add the selected hostname to the list'''
        host_to_add = str(self.ui.text_host.text())
        self.hostnames_file.append(['0.0.0.0', '0 ms', host_to_add, '[n/s]'])
        self.ui.list_hosts.addItem(host_to_add)
        self.save_hostnames_to_file()


if __name__ == "__main__":
    # Create the GUI
    app = QtGui.QApplication(sys.argv)
    gui = StartUI()

    # Show the GUI
    gui.show()
    sys.exit(app.exec_())
