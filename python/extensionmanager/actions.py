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

# Functions for installing and deleting extensions

import sys, zipfile
from PythonExtension import PluginInstance as instance
from send2trash import send2trash

def install(path):
    try:
        extZip = zipfile.ZipFile(path, "r")
        # Verify all files are in the same directory
        # NOTE: This is vulnerable to things like ../
        if len(extZip.namelist()) < 1:
            extZip.close()
            return "The .zip file is empty."
        extName = extZip.namelist()[0].split("/")[0]
        for path in extZip.namelist():
            if extName != path.split("/")[0] or len(extName) < 1:
                extZip.close()
                return "The .zip file is malformed."
        # Make sure the extension manager does not overwrite
        # extensions that are already installed
        for ext in instance.extensionList():
            if extName == ext:
                return "The extension \"{}\" is already installed. Uninstall it before trying again.".format(ext)
        extZip.extractall(instance.extensionDir().absolutePath())
        extZip.close()
    except Exception as e:
        return str(e)
    return True

def uninstall(ext):
    send2trash(instance.extensionDir().absolutePath() + "/" + ext)
