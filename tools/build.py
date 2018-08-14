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