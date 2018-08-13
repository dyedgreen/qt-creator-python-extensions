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

# This one fixes things for the sanity bot
# Usage: Run with no options from project root

import os


files_nl = ["cpp", "h", "py", "xml", "md", "pro", "pri", "txt", "gitignore"]

def fix_nl(file):
    f = open(file, "r")
    body = f.read(-1)
    f.close()
    if len(body) > 0 and body[-1] != "\n":
        body += "\n"
        f = open(file, "w")
        f.write(body)
        f.close()
        print("Fixed {}".format(file))
    else:
        print("Skipped {}".format(file))

files_width = ["cpp", "h"]
max_line_widths = {"cpp": 100, "h": 100}

def notice_line_width(file):
    f = open(file, "r")
    lines = f.read(-1).split("\n")
    f.close()
    for i in range(len(lines)):
        if len(lines[i]) > max_line_widths[file_type(file)]:
            print("Notice: Max line width exceeded in file '{0}', line {1}".format(file, i))

def file_type(file):
    return file.split(".")[-1]

for path in os.walk("."):
    for filename in path[2]:
        if file_type(filename) in files_nl:
            fix_nl(path[0] + "/" + filename)
        if file_type(filename) in files_width:
            notice_line_width(path[0] + "/" + filename)
