# Python Extensions for QtCreator

This extension for QtCreator makes it possible to extend the QtCreator by writing Python extensions.
These extensions consist of a directory containing a `main.py` and any other Python code necessary.
They can be shared as zip archives, installed and managed through the included extension manager
(which is a Python extension itself) and thus allow the QtCreator to be easily extended with
custom functionality.

**WARNING:** This is a first draft / proof of concept and only offers very limited functionality.
There will still be many bugs and so far the project has only been tested on Linux.


## What's included
This repository contains the following:

 * The code of the C++ plugin that executes the Python extensions
 * An extension manager written in Python that is installed alongside the C++ plugin and allows to
   install new Python extensions, as well as manage existing ones.
 * A few example plugins in the `examples` folder. These can be installed manually, see the
   separate `examples/README.md` for more information.
 * An incomplete documentation of the C++ plugin, as well as an incomplete documentation for Python
   extension authors.

## Installation instructions
Note that this process has so far only be tested on Linux. The plugin itself has only been tested
with Python 3.5 and 2.7 and QtCreator 4.7.82.

### Install dependencies
Before you can compile and install the PythonExtensions plugin, you need to install [PySide2](https://pyside.org)
for the version of Python you plan to use. This is necessary, as the plugin uses the system installed
Python (or the Python installed in your virtual env, if you have one set up) and it's packages. You
will also need to build your own version of QtCreator and require a Qt installation. (This
project has so far only been tested with Qt5.11.0.)

To obtain the required Qt version, you can either build Qt yourself, or use the
[installer provided on the Qt website](https://www.qt.io/download).

To install PySide2 please refer to their [installation instructions](http://wiki.qt.io/Qt_for_Python/GettingStarted).
When installing PySide2, make sure [Shiboken](https://doc.qt.io/qtforpython/shiboken2/contents.html)
is installed alongside, as it will be necessary for compiling the plugin. (Shiboken is the binding
generator used by and originally developed for PySide2.)

**WARNING:** This project depends on two recent patches to Shiboken, one of which has not yet passed
code review. These patches are:

 * [Change-Id: Ib72b14cc704c04ae3b4197fd2af718276e3fe788](https://codereview.qt-project.org/#/c/234966/4)
   (merged)
 * [Change-Id: Iaaa38b66b5d3aabc0fb8f995f964cd7aef2a11da](https://codereview.qt-project.org/#/c/235072/)
   (review in progress)

Make sure your version of Shiboken has both of these patches. Otherwise, you will encounter errors
when parsing / compiling this project.

To build QtCreator, which is necessary for building the plugin, please refer to their
[build instructions](https://doc-snapshots.qt.io/qtcreator-extending/getting-and-building.html).

### Build the C++ plugin
Once all dependencies are installed, you can go ahead and build the plugin itself. To do this (in
the best case) all you will have to do is run the following commands in this projects root directory:
```
$ path/to/your/qmake
$ make
```
After this, the plugin should be installed into the QtCreator version you built in the previous
steps. If this worked, you can now go ahead and check out the `examples` folder and play with the
provided example Python extensions.

Notice that depending on your configuration, you may need to add clang to your library paths for
Shiboken to run. Achieve this by running the following before building the plugin:
```
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/path/to/clang/lib
```

**NOTICE:** This plugin generates a few debug messages and potential warnings. Any Python extension
that is installed might also write output to stdout. To see these messages, you can execute
QtCreator from your terminal by running the executable there.

### What to do if it didn't work?
There are several things you might want to try:

 * Read through the build output and make sure all dependencies are set up correctly
   - A problem I encountered here is Shiboken not finding clang. If this happens, try running:
     ```
     $ export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/path/to/your/libclang/lib
     ```
   - Another problem that can occur if you have multiple Qt versions installed, is PySide not finding
     the correct version. In this case try adding the line
     ```
     set(CMAKE_PREFIX_PATH "/path/to/your/qt5/5.11.0/gcc_64")
     ```
     in the file `sources/pyside2/CMakeLists.txt` in the PySide project.
 * Have a look at `pythonextensions.pro` and change the hard-coded fall-back paths you find there to
   match the paths of your setup.

If none of the above suggestions fix your problem, I am afraid you will have to find a solution for
yourself. If that happens and you find a fix, please share it with me, so that it can be included in
this list (or in the build system).

## How it works
In a nutshell, this project generates Python bindings for the QtCreator using Shiboken and then
executes python scripts it finds in a bespoke directory.

The following process allows the plugin to work:

 1. At compile time, Shiboken generates a huge amount of C++ code that allows a few classes from the
    Core plugin and utils library to be accessed from Python.
 2. When QtCreator is executed, the C++ plugin searches the standard QtCreator plugin directories
    for a directory named `python`, the first directory found is the Python extension directory.
    - Now, each subdirectory represents it's own Python extension. For each subdirectory the
      C++ plugin checks whether it contains a `setup.py`. If it does, this setup script is
      executed.
    - After all the setup scripts have been executed, each subdirectory is checked for a file named
      `main.py`. This file is the extensions entry point and is executed by the C++ plugin.
 3. Now all Python extensions have registered their actions / menus / etc., which can be triggered
    from the QtCreator interface.

When executed, the Python extensions can import any modules / packages installed for the system
Python or found in their own directory. While the C++ plugin takes some precautions to isolate the
Python extensions when executed, they are still all run in the same Python instance, which means that
they are not completely isolated. However, so far this did not turn out to be a problem.

For a more detailed description, please refer to the documentation in `docs`.
