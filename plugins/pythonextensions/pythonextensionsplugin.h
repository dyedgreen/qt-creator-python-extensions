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

#pragma once

#include "pythonextensions_global.h"

#include <extensionsystem/iplugin.h>

#include <QDir>
#include <QStringList>

namespace PythonExtensions {
namespace Internal {

class PythonExtensionsPlugin : public ExtensionSystem::IPlugin
{
    Q_OBJECT
    Q_PLUGIN_METADATA(IID "org.qt-project.Qt.QtCreatorPlugin" FILE "PythonExtensions.json")

public:
    PythonExtensionsPlugin();
    ~PythonExtensionsPlugin();

    bool initialize(const QStringList &arguments, QString *errorString) final;
    void extensionsInitialized() final;
    bool delayedInitialize() final;
    ShutdownFlag aboutToShutdown() final;

    QDir extensionDir();
    QStringList extensionList(const bool loadedOnly = false);
    void flagAsLoaded(const QString &extension);
    QString pythonPackagePath();
private:
    QStringList m_loadedExtensions;
    void initializePythonBindings();
    void initializeOptionalBindings();
    void installRequirements();
    void setupPythonExtensions();
    void initializePythonExtensions();
};

// Util functions
// TODO: Are any needed? Until now there were no problems with object ownership

} // namespace Internal
} // namespace PythonExtensions


// Fix for binding build, caused by multiple QtCreator headers
// having the same name, for some build configurations.
#include "bindingheaders/core_fileutils.h"
