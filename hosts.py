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
        self.hostnames_file = self.load_hostnames_file(default_hostnames)
        self.add_all_hostnames_to_list()

        # Signal Handling
        QtCore.QObject.connect(self.ui.button_add,
                               QtCore.SIGNAL("clicked()"),
                               self.add_hostname)
        QtCore.QObject.connect(self.ui.button_remove,
                               QtCore.SIGNAL("clicked()"),
                               self.remove_selected)
        QtCore.QObject.connect(self.ui.button_load,
                               QtCore.SIGNAL("clicked()"),
                               self.load_from_file)

    def load_hostnames_file(self, file):
        '''Load a csv file containing the hostnames'''
        data = []
        header = []
        with open(file, "rb") as csv_file:
            reader = csv.reader(csv_file)
            header = reader.next()
            for i, column_name in enumerate(header):
                if column_name == "Hostname":
                    self.hostname_csv_column = i
                    break
            data.append(header)
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
        '''Load all the hostnames into the UI list'''
        for row in self.hostnames_file[1:]:  # [1:] skips the header row
            self.ui.list_hosts.addItem(row[self.hostname_csv_column])

    def load_from_file(self):
        '''Load the hostnames from another csv file'''
        filename = QtGui.QFileDialog.getOpenFileName(
                                                     self, "Open CSV file", "",
                                                     "CSV files (*.csv)")
        if os.path.isfile(filename):
            message = QtGui.QMessageBox(self)
            message.setText("Would you like to replace all the previous " +
                            "hostnames with the file contents (Replace) or " +
                            "merge the existing hostnames with the ones from" +
                            " file while also avoiding repeated hostnames" +
                            " (Merge)")
            message.setIcon(QtGui.QMessageBox.Question)
            message.setWindowTitle("Replace or Merge File Contents")
            message.addButton("Replace", QtGui.QMessageBox.AcceptRole)
            message.addButton("Merge", QtGui.QMessageBox.DestructiveRole)
            cancel = message.addButton("Cancel", QtGui.QMessageBox.RejectRole)
            message.setDefaultButton(cancel)
            message.exec_()
            response = message.clickedButton().text()
            if response == "Merge":
                self.merge_new_hostnames(filename)
            elif response == "Replace":
                self.replace_new_hostnames(filename)

    def merge_new_hostnames(self, file):
        '''Merge the new hostnames with the existing ones'''
        loaded_hosts = self.load_hostnames_file(file)
        hosts_to_add = []
        for loaded_host in loaded_hosts:
            merge = 1
            for old_host in self.hostnames_file:
                if loaded_host[self.hostname_csv_column] in old_host:
                    merge = 0
                    break
            if merge == 1:
                hosts_to_add.append(loaded_host)

        for new_host in hosts_to_add:
            # Add the new hostnames to the existing ones
            self.hostnames_file.append(new_host)
            # Add the on the UI
            self.add_hostname(new_host[self.hostname_csv_column])
        self.save_hostnames_to_file()

    def replace_new_hostnames(self, file):
        '''Replace the existing hostnames with the ones loaded from file'''
        self.hostnames_file = self.load_hostnames_file(file)
        self.ui.list_hosts.clear()
        self.add_all_hostnames_to_list()
        self.save_hostnames_to_file()

    def remove_selected(self):
        '''Remove the selected hostname/s from the list'''
        selected_hosts_items = self.ui.list_hosts.selectedItems()
        for item in selected_hosts_items:
            # Remove from UI
            index = self.ui.list_hosts.row(item)
            self.ui.list_hosts.takeItem(index)
            # Remove from file
            del self.hostnames_file[index + 1]
        # Save file
        self.save_hostnames_to_file()

    def add_hostname(self, hostname=""):
        '''Add a single hostname to the list'''
        if not hostname:
            host_to_add = str(self.ui.text_host.text())
        else:
            host_to_add = hostname

        if not host_to_add.strip():
            return
        # Append to file
        self.hostnames_file.append(['0.0.0.0', '0 ms', host_to_add, '[n/s]'])
        # Add to UI
        self.ui.list_hosts.addItem(host_to_add)
        # Save file
        self.save_hostnames_to_file()
        # Clear text field
        self.ui.text_host.clear()


if __name__ == "__main__":
    # Create the GUI
    app = QtGui.QApplication(sys.argv)
    gui = StartUI()

    # Show the GUI
    gui.show()
    sys.exit(app.exec_())
