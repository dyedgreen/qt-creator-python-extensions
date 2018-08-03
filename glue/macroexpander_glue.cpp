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

void registerPythonVariable(const QByteArray &variable, const QString &description, PyObject *func) {
    if (!PyCallable_Check(func)) {
        PyErr_BadArgument();
        return;
    }
    Py_XINCREF(func);

    globalMacroExpander()->registerVariable(variable, description,
        [=]() -> QString {
            PyObject *ret = PyObject_Repr(PyObject_CallFunction(func, NULL));
            #if PY_MAJOR_VERSION >= 3
            QString value = QString::fromUtf8(PyUnicode_AsUTF8(ret));
            #else
            QString value = QString::fromUtf8(PyString_AsString(ret));
            #endif
            return value;
        }
    );
}

void registerPythonPrefixVariable(const QByteArray &variable, const QString &description, PyObject *func) {
    if (!PyCallable_Check(func)) {
        PyErr_BadArgument();
        return;
    }
    Py_XINCREF(func);

    globalMacroExpander()->registerPrefix(variable, description,
        [=](QString passed_string) -> QString {
            PyObject *ret = PyObject_Repr(PyObject_CallFunction(func, "s", passed_string.toStdString().c_str()));
            #if PY_MAJOR_VERSION >= 3
            QString value = QString::fromUtf8(PyUnicode_AsUTF8(ret));
            #else
            QString value = QString::fromUtf8(PyString_AsString(ret));
            #endif
            return value;
        }
    );
}
