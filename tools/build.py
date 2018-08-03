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

# This is intended as a convenience for building the main C++
# plugin, as well as the optional bindings using one command.
# This exists mainly because I am lazy and should probably not
# really be a part of the build-system going forward.

# Usage:
# $ python build.py --qmake=/path/to/qmake

# Options:
# --user
# (optional, sets USE_USER_DESTDIR)
# --skip
# (optional, skip optional builds)

import subprocess, sys


def user():
    return "--user" in sys.argv

def skip():
    return "--skip" in sys.argv

def qmake():
    for arg in sys.argv:
        if arg.split("=")[0] == "--qmake":
            return arg.split("=")[-1]
    return "qmake"

def read_pri():
    f = open("plugins/pythonextensions/qtcreator.pri", "r")
    body = f.read(-1)
    f.close()
    return body

def write_pri(body):
    f = open("plugins/pythonextensions/qtcreator.pri", "w")
    f.write(body)
    f.close()

def build_plugin():
    subprocess.check_call(qmake(), cwd="plugins/pythonextensions")
    subprocess.check_call("make", cwd="plugins/pythonextensions")

def build_optional():
    subprocess.check_call(["python", "setup.py", "--qmake={}".format(qmake())], cwd="optional")


if __name__ == "__main__":
    if user():
        write_pri(read_pri().replace("# USE_USER_DESTDIR = yes", "USE_USER_DESTDIR = yes"))
    build_plugin()
    if not skip():
        build_optional()
    if user():
        write_pri(read_pri().replace("USE_USER_DESTDIR = yes", "# USE_USER_DESTDIR = yes"))
