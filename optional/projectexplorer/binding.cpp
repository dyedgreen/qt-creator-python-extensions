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

#include "binding.h"

#include <QtCore/QDebug>
#include <QtCore/QString>

#undef signals
#undef slots

#include <sbkpython.h>
#include <sbkconverter.h>
#include <sbkmodule.h>

#if PY_MAJOR_VERSION >= 3
extern "C" PyObject *PyInit_QtCreatorBindingProjectExplorer();
#else
extern "C" void initQtCreatorBindingProjectExplorer();
#endif

extern PyObject *SbkQtCreatorBindingProjectExplorerModuleObject;

namespace PyUtil {
    extern bool bindPyObject(const QString &moduleName, const QString &name, void *obj);
}

void bind()
{
    // Init module
    #if PY_MAJOR_VERSION >= 3
    const bool pythonInitialized = PyInit_QtCreatorBindingProjectExplorer() != nullptr;
    #else
    const bool pythonInitialized = true;
    initQtCreatorBindingProjectExplorer();
    #endif
    // Bind module into interpreter
    bool pythonError = PyErr_Occurred() != nullptr;
    if (pythonInitialized && !pythonError) {
        PyUtil::bindPyObject("__main__", "test", (void *)SbkQtCreatorBindingProjectExplorerModuleObject);
    } else {
        if (pythonError)
            PyErr_Print();
        qDebug() << "There was a problem initializing the ProjectExplorer bindings.";

    }
}
