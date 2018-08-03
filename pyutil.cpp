/****************************************************************************
**
** Copyright (C) 2018 The Qt Company Ltd.
** Contact: https://www.qt.io/licensing/
**
** This file is part of the Python Extensions Plugin for QtCreator.
**
** Commercial License Usage
** Licensees holding valid commercial Qt licenses may use this file in
** accordance with the commercial license agreement provided with the
** Software or, alternatively, in accordance with the terms contained in
** a written agreement between you and The Qt Company. For licensing terms
** and conditions see https://www.qt.io/terms-conditions. For further
** information use the contact form at https://www.qt.io/contact-us.
**
** GNU General Public License Usage
** Alternatively, this file may be used under the terms of the GNU
** General Public License version 3 as published by the Free Software
** Foundation with exceptions as appearing in the file LICENSE.GPL3-EXCEPT
** included in the packaging of this file. Please review the following
** information to ensure the GNU General Public License requirements will
** be met: https://www.gnu.org/licenses/gpl-3.0.html.
**
****************************************************************************/

#include "pyutil.h"

#include <dlfcn.h> // dlopen

#include <QtCore/QByteArray>
#include <QtCore/QCoreApplication>
#include <QtCore/QDebug>
#include <QtCore/QStringList>
#include <QtCore/QTemporaryFile>
#include <QtCore/QDir>

// These are used in python and cause compile-time errors
// if still defined.
#undef signals
#undef slots

#include <sbkpython.h>
#include <sbkconverter.h>
#include <sbkmodule.h>

// Setup and utility functions for QtCreatorPython bindings
// from typesystem.xml

#if PY_MAJOR_VERSION >= 3
extern "C" PyObject *PyInit_QtCreatorPython();
#else
extern "C" void initQtCreatorPython();
#endif

// These variables store all Python types exported by QtCreatorPython,
// as well as the types exported for QtWidgets.
extern PyTypeObject **SbkQtCreatorPythonTypes;
extern PyTypeObject **SbkPySide2_QtWidgetsTypes;

// This variable stores all type converters exported by QtCreatorPython.
extern SbkConverter **SbkScriptTestTypeConverters;

// This variable stores the Python module generated by Shiboken
extern PyObject *SbkQtCreatorPythonModuleObject;

namespace PyUtil {

static State state = PythonUninitialized;

static void cleanup()
{
    if (state > PythonUninitialized) {
        Py_Finalize();
        state = PythonUninitialized;
    }
}

State init()
{
    if (state > PythonUninitialized)
        return state;

    // If there is an active python virtual environment, use that environment's packages location.
    QByteArray virtualEnvPath = qgetenv("VIRTUAL_ENV");
    if (!virtualEnvPath.isEmpty())
        qputenv("PYTHONHOME", virtualEnvPath);

    // Python's shared libraries don't work properly if included from other
    // shared libraries. See https://mail.python.org/pipermail/new-bugs-announce/2008-November/003322.html
    #if PY_MAJOR_VERSION >= 3
    std::string version = "libpython"+std::to_string(PY_MAJOR_VERSION)+"."+std::to_string(PY_MINOR_VERSION)+"m.so";
    #else
    std::string version = "libpython"+std::to_string(PY_MAJOR_VERSION)+"."+std::to_string(PY_MINOR_VERSION)+".so";
    #endif
    dlopen(version.c_str(), RTLD_LAZY | RTLD_GLOBAL);

    Py_Initialize();
    qAddPostRoutine(cleanup);
    state = PythonInitialized;
    #if PY_MAJOR_VERSION >= 3
    const bool pythonInitialized = PyInit_QtCreatorPython() != nullptr;
    #else
    const bool pythonInitialized = true;
    initQtCreatorPython();
    #endif
    const bool pyErrorOccurred = PyErr_Occurred() != nullptr;
    if (pythonInitialized && !pyErrorOccurred) {
        state = QtCreatorModuleLoaded;
    } else {
        if (pyErrorOccurred)
            PyErr_Print();
        qWarning("Failed to initialize the QtCreator module.");
    }

    return state;
}

bool createModule(const std::string &moduleName)
{
    if (init() != QtCreatorModuleLoaded)
        return false;

    PyObject *module = PyImport_AddModule(moduleName.c_str());
    if (!module) {
        if (PyErr_Occurred())
            PyErr_Print();
        qWarning() << __FUNCTION__ << "Failed to create module";
        return false;
    }

    return true;
}

bool bindObject(const QString &moduleName, const QString &name, int index, void *o)
{
    if (init() != QtCreatorModuleLoaded)
        return false;

    // Generate the type
    PyTypeObject *typeObject = SbkQtCreatorPythonTypes[index];

    PyObject *po = Shiboken::Conversions::pointerToPython(reinterpret_cast<SbkObjectType *>(typeObject), o);
    if (!po) {
        qWarning() << __FUNCTION__ << "Failed to create wrapper for" << o;
        return false;
    }
    Py_INCREF(po);

    PyObject *module = PyImport_AddModule(moduleName.toLocal8Bit().constData());
    if (!module) {
        Py_DECREF(po);
        if (PyErr_Occurred())
            PyErr_Print();
        qWarning() << __FUNCTION__ << "Failed to locate module" << moduleName;
        return false;
    }

    if (PyModule_AddObject(module, name.toLocal8Bit().constData(), po) < 0) {
        if (PyErr_Occurred())
            PyErr_Print();
        qWarning() << __FUNCTION__ << "Failed to add object" << name << "to" << moduleName;
        return false;
    }

    return true;
}

bool bindShibokenModuleObject(const QString &moduleName, const QString &name)
{
    if (init() != QtCreatorModuleLoaded)
        return false;

    PyObject *module = PyImport_AddModule(moduleName.toLocal8Bit().constData());
    if (!module) {
        if (PyErr_Occurred())
            PyErr_Print();
        qWarning() << __FUNCTION__ << "Failed to locate module" << moduleName;
        return false;
    }

    if (PyModule_AddObject(module, name.toLocal8Bit().constData(), SbkQtCreatorPythonModuleObject) < 0) {
        if (PyErr_Occurred())
            PyErr_Print();
        qWarning() << __FUNCTION__ << "Failed to add object" << name << "to" << moduleName;
        return false;
    }

    return true;
}

bool runScript(const std::string &script)
{
    if (init() == PythonUninitialized)
        return false;

    if (PyRun_SimpleString(script.c_str()) == -1) {
        if (PyErr_Occurred())
            PyErr_Print();
        return false;
    }

    return true;
}

std::string privateName(const std::string &name)
{
    // Python has no concept of private variables and there
    // is no way to declare a namespace or scope that will be
    // inaccessible from the user script.
    // To avoid naming collisions with the setup and tear down
    // scripts that attempt to separate different extensions on
    // the level of user code (or at least make them appear separated),
    // this function mangles the names of variables used.
    return "qt_creator_" + name + "_symbol_mchawrioklpilnjajqkfl";
}

bool runScriptWithPath(const std::string &script, const std::string &path)
{
    // I couldn't find a direct c api, but this should cause no variable name
    // collisions. It also cleans the imported modules after the script finishes
    const std::string s =
"import sys as " + privateName("sys") + "\n"
"" + privateName("path") + " = list(" + privateName("sys") + ".path)\n"
"" + privateName("sys") + ".path.insert(0, \"" + path + "\")\n"
"" + privateName("loaded_modules") + " = list(" + privateName("sys") + ".modules.keys())\n"
"" + script + "\n"
"" + privateName("sys") + ".path = " + privateName("path") + "\n"
"for m in list(" + privateName("sys") + ".modules):\n"
"    if m not in " + privateName("loaded_modules") + ":\n"
"        del(" + privateName("sys") + ".modules[m])\n";
    return runScript(s);
}

bool addToSysPath(const std::string &path)
{
    // Add a path to Pythons sys.path
    // Used for installing dependencies into custom
    // directory
    const std::string s =
"import sys as " + privateName("sys") + "\n"
"" + privateName("sys") + ".path.append(\"" + path + "\")";
    return runScript(s);
}

bool pipInstallRequirements(const std::string &requirements, const std::string &target)
{
    // Run a requirements.txt file with pip
    const std::string s =
"import subprocess, sys\n"
"subprocess.call(\"{} -m pip install -t " + target + " -r " + requirements + "\".format(sys.executable).split())\n"
"open(\"" + requirements + "\".replace(\"requirements.txt\",\"requirements.txt.installed\"),\"a\").close()\n";
    return runScriptWithPath(s, "");
}

} // namespace PyUtil
