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

# Assemble the binding projects and build them

# You need to specify the correct qmake when running:
# $ python setup.py --qmake=/path/to/qmake
# (defaults to "qmake")

import os, shutil, subprocess, sys

def qmake():
    for arg in sys.argv:
        if arg.split("=")[0] == "--qmake":
            return arg.split("=")[-1]
    return "qmake"

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

def generateBuildDir(binding_name):
    build_dir = "build_{}".format(binding_name)
    if os.path.exists(build_dir):
        shutil.rmtree(build_dir)
    os.makedirs(build_dir)
    copytree("template", build_dir)
    copytree(binding_name, build_dir)

def runBuild(binding_name):
    build_dir = "build_{}".format(binding_name)
    if os.path.exists(build_dir):
        try:
            subprocess.check_call(qmake(), cwd=build_dir)
            subprocess.check_call("make", cwd=build_dir)
        except Exception as e:
            print("Got exception when building {}:".format(binding_name), e)
            return False
        return True
    return False

def cleanBuildDirs():
    for build_dir in os.scandir():
        if build_dir.is_dir() and build_dir.name.split("_")[0] == "build":
            shutil.rmtree(build_dir.name)
            print("Removing {}".format(build_dir.name))

def main():
    for binding in os.scandir():
        if binding.is_dir() and binding.name != "template" and binding.name.split("_")[0] != "build":
            generateBuildDir(binding.name)
            if runBuild(binding.name):
                print("Built {}".format(binding.name))
            else:
                print("Error building {}".format(binding.name))


if __name__ == "__main__":
    if "clean" in sys.argv:
        cleanBuildDirs()
    else:
        main()
