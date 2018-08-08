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

#ifndef PYUTIL_H
#define PYUTIL_H

#include "pythonextensions_global.h"
#include <string>

class QObject;
class QString;

namespace PyUtil {

// Note: If modifying the bindings, check these types still align
enum QtCreatorTypes
{
    PythonExtensionsPluginType = 31, // SBK_PYTHONEXTENSIONS_INTERNAL_PYTHONEXTENSIONSPLUGIN_IDX
};

enum State
{
    PythonUninitialized,
    PythonInitialized,
    QtCreatorModuleLoaded,
};

State init();

PYTHONEXTENSIONSSHARED_EXPORT bool createModule(const std::string &moduleName);

bool bindObject(const QString &moduleName, const QString &name, int index, void *o);

bool bindShibokenModuleObject(const QString &moduleName, const QString &name);

PYTHONEXTENSIONSSHARED_EXPORT bool bindPyObject(const QString &moduleName, const QString &name, void *obj);

PYTHONEXTENSIONSSHARED_EXPORT bool bindSubPyObject(const QString &moduleName, const QString &name, void *obj);

PYTHONEXTENSIONSSHARED_EXPORT bool runScript(const std::string &script);

PYTHONEXTENSIONSSHARED_EXPORT bool runScriptWithPath(const std::string &script, const std::string &path);

PYTHONEXTENSIONSSHARED_EXPORT bool addToSysPath(const std::string &path);

PYTHONEXTENSIONSSHARED_EXPORT bool pipInstallRequirements(const std::string &requirements, const std::string &target);

} // namespace PyUtil

#endif
