#############################################################################
##
## Copyright (C) 2018 The Qt Company Ltd.
## Contact: http://www.qt.io/licensing/
##
## This file is part of the Python Extensions Plugin for QtCreator.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of The Qt Company Ltd nor the names of its
##     contributors may be used to endorse or promote products derived
##     from this software without specific prior written permission.
##
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
##
## $QT_END_LICENSE$
##
#############################################################################

# Ui for extension list view

from PySide2 import QtCore, QtWidgets, QtGui
from PythonExtension import PluginInstance as instance
import actions

class ExtensionList(QtWidgets.QListWidget):
    def __init__(self):
        super(ExtensionList, self).__init__()

        self.itemClicked.connect(self.showInfo)

    def showInfo(self, item):
        return

    def loadExtensionList(self):
        i = 0
        for ext in instance.extensionList():
            item = QtWidgets.QListWidgetItem(self)
            if not ext in instance.extensionList(True):
                item.setText(ext + " [did not load]")
                item.setIcon(QtGui.QIcon.fromTheme("dialog-error"))
            else:
                item.setText(ext)
                item.setIcon(QtGui.QIcon.fromTheme("applications-development"))
            if i % 2 == 1:
                item.setBackground(QtGui.QBrush(QtGui.QColor.fromRgb(240, 240, 240)))
            i += 1


# View that lists all extensions
class ListView(QtWidgets.QDialog):
    def __init__(self, parent):
        super(ListView, self).__init__(parent, QtCore.Qt.WindowSystemMenuHint | QtCore.Qt.WindowTitleHint)

        self.setWindowTitle("Installed Python Extensions")

        self.layout = QtWidgets.QVBoxLayout(self)

        self.label = QtWidgets.QLabel()
        self.label.setText("Manage Python extensions installed to \"{0}\".".format(instance.extensionDir().absolutePath()))
        self.label.setWordWrap(True)
        self.layout.addWidget(self.label)

        self.list = ExtensionList()
        self.layout.addWidget(self.list)

        self.buttonDone = QtWidgets.QPushButton("Close")
        self.buttonDone.setDefault(True)
        self.buttonDone.clicked.connect(self.close)

        self.buttonDelete = QtWidgets.QPushButton("Uninstall")
        self.buttonDelete.setAutoDefault(False)
        self.buttonDelete.clicked.connect(self.actionDelete)

        self.buttonAdd = QtWidgets.QPushButton("Install")
        self.buttonAdd.setAutoDefault(False)
        self.buttonAdd.clicked.connect(self.actionAdd)

        self.buttonBox = QtWidgets.QDialogButtonBox(QtCore.Qt.Horizontal)
        self.buttonBox.addButton(self.buttonDone, QtWidgets.QDialogButtonBox.AcceptRole)
        self.buttonBox.addButton(self.buttonDelete, QtWidgets.QDialogButtonBox.ActionRole)
        self.buttonBox.addButton(self.buttonAdd, QtWidgets.QDialogButtonBox.ActionRole)
        self.layout.addWidget(self.buttonBox)

        self.reloadExtensionList()

        self.resize(400, 350)

    def reloadExtensionList(self):
        self.list.clear()
        self.list.loadExtensionList()

    def actionDelete(self):
        selected = self.list.selectedIndexes()
        if len(selected) >= 1:
            selected = selected[0].row()
            ext = instance.extensionList()[selected]
            if ext == "extensionmanager":
                QtWidgets.QMessageBox.warning(self, "Can not Uninstall", "The Extension Manager can not uninstall itself.")
            else:
                ret = QtWidgets.QMessageBox.warning(
                    self,
                    "Uninstall \"" + ext + "\"?",
                    "You are about to uninstall \"" + ext + "\". This action can not be undone. Do you want to proceed?",
                    QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Yes,
                    QtWidgets.QMessageBox.Cancel
                )
                if ret == QtWidgets.QMessageBox.Yes:
                    actions.uninstall(ext)
                    self.reloadExtensionList()
                    QtWidgets.QMessageBox.information(
                        self,
                        "Removed \"" + ext + "\"",
                        "The extension was uninstalled. Please restart QtCreator to apply this change."
                    )
        else:
            QtWidgets.QMessageBox.warning(self, "Select an Extension", "Please select an extension to uninstall.")

    def actionAdd(self):
        fileName = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Select Extension",
            "/",
            "QtCreator Python Extensions (*.zip)"
        )
        oldExtensions = list(instance.extensionList())
        result = actions.install(fileName[0])
        if result == True:
            QtWidgets.QMessageBox.information(
                self,
                "Extension Installed",
                "The extension from \"" + fileName[0] + "\" was installed successfully. Please restart QtCreator to apply this change."
                        )
            self.reloadExtensionList()
        else:
            box = QtWidgets.QMessageBox(self)
            box.setWindowTitle("Could not Install Extension")
            box.setText("There was a problem installing your extension.")
            box.setDetailedText(str(result))
            box.setIcon(QtWidgets.QMessageBox.Warning)
            box.exec_()
