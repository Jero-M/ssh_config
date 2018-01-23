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
        QtCore.QObject.connect(self.ui.button_remove,
                               QtCore.SIGNAL("clicked()"),
                               self.remove_selected)
        QtCore.QObject.connect(self.ui.button_load,
                               QtCore.SIGNAL("clicked()"),
                               self.load_from_file)

    def load_default_hostnames_file(self):
        '''Load the default hostnames file'''
        data = []
        header = []
        with open(default_hostnames, "rb") as csv_file:
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
        '''Load all the hostnames into the list'''
        for row in self.hostnames_file[1:]:  # [1:] skips the header row
            self.ui.list_hosts.addItem(row[self.hostname_csv_column])

    def load_from_file(self):
        '''Load the hostnames from another file'''
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
                print "Merge", filename
            elif response == "Replace":
                print "Replace", filename

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

    def add_selected(self):
        '''Add the selected hostname to the list'''
        host_to_add = str(self.ui.text_host.text())
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

    def load_replace(self):
        print "replace"

    def replace_or_merge_dialog(self):
        '''Creates the Dialog window to replace or merge new hostnames'''
        dialog = QtGui.QDialog()
        dialog.resize(646, 140)
        dialog.setMinimumSize(QtCore.QSize(646, 140))
        dialog.setMaximumSize(QtCore.QSize(646, 140))
        dialog.setWindowTitle("Replace or Merge Contents")
        self.dialog_label = QtGui.QLabel(dialog)
        self.dialog_label.setGeometry(QtCore.QRect(31, 12, 581, 56))
        self.dialog_label.setAlignment(QtCore.Qt.AlignLeading |
                                       QtCore.Qt.AlignLeft |
                                       QtCore.Qt.AlignTop)
        self.dialog_label.setWordWrap(True)
        self.dialog_label.setText("Would you like to replace all the" +
                                  "previous hostnames with the file contents" +
                                  "(Replace) or merge the existing hostnames" +
                                  "with the ones from file while also" +
                                  "avoiding repeated hostnames (Merge)")
        self.button_replace = QtGui.QPushButton("Relace", dialog)
        self.button_replace.setGeometry(QtCore.QRect(130, 90, 99, 27))
        self.button_merge = QtGui.QPushButton("Merge", dialog)
        self.button_merge.setGeometry(QtCore.QRect(270, 90, 99, 27))
        self.button_cancel = QtGui.QPushButton("Cancel", dialog)
        self.button_cancel.setGeometry(QtCore.QRect(410, 90, 99, 27))
        dialog.exec_()

        QtCore.QObject.connect(self.button_replace,
                               QtCore.SIGNAL("clicked()"),
                               self.load_replace)

if __name__ == "__main__":
    # Create the GUI
    app = QtGui.QApplication(sys.argv)
    gui = StartUI()

    # Show the GUI
    gui.show()
    sys.exit(app.exec_())
