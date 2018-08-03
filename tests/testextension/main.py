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

# Unit tests for the Python Extensions Plugins
# behavior from the view of an extension.
# To use simply install as an extension and run
# QtCreator. (Outputs to terminal)

import unittest
import os, sys, io

# NOTE: Done here, because the unit-test stuff imports math
math_imported = "math" in sys.modules

# Test Cases

class TestRequirements(unittest.TestCase):

    def test_installed(self):
        """
        Test if numpy was installed as expected
        """
        try:
            import numpy
        except ImportError:
            self.assertTrue(False, msg="Install failed.")

    def test_marked(self):
        """
        Test whether the extensions requirements were
        marked as installed
        """
        self.assertTrue(os.path.exists("{}/requirements.txt.installed".format(sys.path[0])), msg="Install was not marked.")

class TestPath(unittest.TestCase):

    def test_clean(self):
        """
        The sys.path should be sanitized after every script
        is run. This also applies to setup.py
        """
        self.assertFalse("test/path" in sys.path, msg="Sys path not sanitized.")

class TestModules(unittest.TestCase):

    def test_clean(self):
        """
        The imported modules should be cleaned after every
        script. This also applies to setup.py
        """
        self.assertFalse(math_imported, msg="Modules not sanitized.")

    def test_exists_builtin(self):
        """
        Test if the bindings for Core, Utils, ExtensionSystem, and PluginInstance
        exist. These are the bindings that currently ship with the main C++ plugin
        and are non-optional.
        """
        try:
            from PythonExtension import QtCreator
        except ImportError:
            self.assertTrue(False, msg="QtCreator binding module missing.")
        self.assertTrue("Core" in dir(QtCreator), msg="Core module missing.")
        self.assertTrue("Utils" in dir(QtCreator), msg="Utils module missing.")
        self.assertTrue("ExtensionSystem" in dir(QtCreator), msg="ExtensionSystem module missing.")

    def text_exists_optional(self):
        """
        These tests may fail, even if everything is setup correctly, depending on
        which QtCreator plugins are enabled.
        """
        try:
            from PythonExtension.QtCreator import PluginInstance
            from PythonExtension.QtCreator import ProjectExplorer
            from PythonExtension.QtCreator import TextEditor
        except ImportError:
            self.assertTrue(False, msg="Optional binding modules missing.")


# Run Unit Tests

def add_tests(test_case, suite):
    for case in dir(test_case):
        if case[:5] == "test_":
            suite.addTest(test_case(case))

def suite():
    suite = unittest.TestSuite()
    add_tests(TestRequirements, suite)
    add_tests(TestPath, suite)
    add_tests(TestModules, suite)
    return suite

out = io.StringIO()
runner = unittest.TextTestRunner(out)
runner.run(suite())

print(out.getvalue())

# Make test output available from ui

from PySide2.QtWidgets import QMessageBox
from PythonExtension import QtCreator

menu = QtCreator.Core.ActionManager.actionContainer("QtCreator.Menu.Help")
menu.menu().addAction("Unit Test Results...", lambda: QMessageBox.information(QtCreator.Core.ICore.dialogParent(), "Python Extensions Unit Test Results", out.getvalue()))
