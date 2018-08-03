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

# This example demonstrates how to use the macro expander
# API to register a macro that can evaluate Python expressions

from PySide2.QtWidgets import QInputDialog, QMessageBox
from PythonExtension import QtCreator

# Register our macro (it can be used as %{Python:exp})
QtCreator.Utils.MacroExpander().registerPrefix(b"Python", "Evaluate Python expressions.", lambda x: eval(x))

# Add a small menu item, that let's us test the macro
def act():
    text = QInputDialog.getMultiLineText(QtCreator.Core.ICore.dialogParent(),
        "Input Text", "Input your text, including some macros",
        "3 + 3 = %{Python:3+3}"
    )
    text = QtCreator.Utils.MacroExpander().expand(text[0])
    QMessageBox.information(QtCreator.Core.ICore.dialogParent(), "Result", text)

# Add this to the "Tools" menu
menu = QtCreator.Core.ActionManager.actionContainer("QtCreator.Menu.Tools")
menu.menu().addAction("Test MacroExpander...", act)
