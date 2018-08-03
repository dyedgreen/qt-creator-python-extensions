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

#include "pythonextensionsplugin.h"

#include "pyutil.h"

#include <coreplugin/icore.h>
#include <coreplugin/icontext.h>
#include <coreplugin/actionmanager/actionmanager.h>
#include <coreplugin/actionmanager/command.h>
#include <coreplugin/actionmanager/actioncontainer.h>
#include <coreplugin/coreconstants.h>
#include <coreplugin/editormanager/editormanager.h>
#include <coreplugin/messagemanager.h>

#include <extensionsystem/pluginmanager.h>
#include <extensionsystem/pluginspec.h>

#include <QDir>
#include <QIODevice>
#include <QFile>
#include <QDir>
#include <QTextStream>
#include <QString>
#include <QStringList>
#include <QLibrary>


namespace PythonExtensions {
namespace Constants {

const char EXTENSIONS_DIR[] = "/python";
const char PY_PACKAGES_DIR[] = "/site-packages";

const char PY_BINDING_LIB[] = "/libPythonBinding";

const char MESSAGE_MANAGER_PREFIX[] = "Python Extensions: ";

} // namespace Constants
namespace Internal {

PythonExtensionsPlugin::PythonExtensionsPlugin()
{
    // Empty
}

PythonExtensionsPlugin::~PythonExtensionsPlugin()
{
    // Unregister objects from the plugin manager's object pool
    // Delete members
}

bool PythonExtensionsPlugin::initialize(const QStringList &arguments, QString *errorString)
{
    // Register objects in the plugin manager's object pool
    // Load settings
    // Add actions to menus
    // Connect to other plugins' signals
    // In the initialize function, a plugin can be sure that the plugins it
    // depends on have initialized their members.

    Q_UNUSED(arguments)
    Q_UNUSED(errorString)

    initializePythonBindings();

    // Python extensions are loaded after C++ plugins for now (plan: later flag can be set)

    return true;
}

void PythonExtensionsPlugin::extensionsInitialized()
{
    // Retrieve objects from the plugin manager's object pool
    // In the extensionsInitialized function, a plugin can be sure that all
    // plugins that depend on it are completely initialized.
}

bool PythonExtensionsPlugin::delayedInitialize()
{
    // Initialize optional bindings
    initializeOptionalBindings();
    // Pip install any requirements known for the script
    installRequirements();
    // Run the setup for each extension that requires it
    setupPythonExtensions();
    // Python plugins are initialized here, to avoid blocking on startup
    initializePythonExtensions();
    return true;
}

ExtensionSystem::IPlugin::ShutdownFlag PythonExtensionsPlugin::aboutToShutdown()
{
    // Save settings
    // Disconnect from signals that are not needed during shutdown
    // Hide UI (if you add UI that is not in the main window directly)
    return SynchronousShutdown;
}

QDir PythonExtensionsPlugin::extensionDir()
{
    // Search python directory in plugin paths
    QDir extension_dir;
    for (const QString &path : ExtensionSystem::PluginManager::pluginPaths()) {
        extension_dir = QDir(path + Constants::EXTENSIONS_DIR);
        if (extension_dir.exists())
            break;
    }
    // Can be checked for validity with .exists()
    return extension_dir;
}

QStringList PythonExtensionsPlugin::extensionList(const bool loadedOnly)
{
    if (loadedOnly)
        return m_loadedExtensions;

    QDir extension_dir = extensionDir();
    if (!extension_dir.exists())
        return QStringList();

    QStringList extension_list = extension_dir.entryList(QDir::AllDirs | QDir::NoDotAndDotDot);
    extension_list.removeOne("site-packages");
    return extension_list;
}

void PythonExtensionsPlugin::flagAsLoaded(const QString &extension)
{
    m_loadedExtensions << extension;
}

QString PythonExtensionsPlugin::pythonPackagePath()
{
    if (extensionDir().exists()) {
        return extensionDir().absolutePath() + Constants::PY_PACKAGES_DIR;
    } else {
        return QString();
    }
}

void PythonExtensionsPlugin::initializePythonBindings()
{
    // Add our custom module directory
    if (extensionDir().exists())
        PyUtil::addToSysPath(pythonPackagePath().toStdString());
    // Initialize the Python context and register global QtCreator variable
    if (!PyUtil::bindShibokenModuleObject("PythonExtension", "QtCreator")) {
        qWarning() << "Python bindings could not be initialized";
        Core::MessageManager::write(Constants::MESSAGE_MANAGER_PREFIX + tr("Python bindings could not be initialized"));
        return;
    }
    // Bind the plugin instance
    PyUtil::bindObject("PythonExtension", "PluginInstance", PyUtil::PythonExtensionsPluginType, this);
}

void PythonExtensionsPlugin::initializeOptionalBindings()
{
    // Try to load optional bindings for all loaded plugins
    // If a plugin has optional bindings, they occur in the form of
    // a shared object which has the name libPythonBinding{PluginName}
    // and exposes a symbol called `bind' which is a void function taking
    // no arguments. This function is responsible for binding the
    // object using the exposed PyUtil api and for reporting any errors
    // etc. to the stderr / stdout.
    // Examples of projects for such libraries exist within this repository.
    for (int i = 0; i < ExtensionSystem::PluginManager::loadQueue().size(); i++) {
        // Check each plugin directory for the library (first found is used)
        QString name = ExtensionSystem::PluginManager::loadQueue()[i]->name();
        for (const QString &path : ExtensionSystem::PluginManager::pluginPaths()) {
            QLibrary bindingLib(path + Constants::PY_BINDING_LIB + name);
            QFunctionPointer bind = bindingLib.resolve("bind");
            if (bind) {
                qDebug() << "Initializing optional bindings for plugin" << name;
                bind();
                break;
            }
        }
    }
}

void PythonExtensionsPlugin::installRequirements()
{
    // Pip install any requirements.txt file found
    QDir extension_dir = extensionDir();
    if (!extension_dir.exists())
        return;

    QStringList extension_list = extensionList();
    for (const QString &extension : extension_list) {
        QString extension_requirements(extension_dir.absolutePath() + "/" + extension + "/requirements.txt");
        if (QFileInfo::exists(extension_requirements) && !QFileInfo::exists(extension_requirements + ".installed")) {
            if (!PyUtil::pipInstallRequirements(
                extension_requirements.toStdString(),
                pythonPackagePath().toStdString()
            )) {
                qWarning() << "Failed to install requirements for extension" << extension;
                Core::MessageManager::write(Constants::MESSAGE_MANAGER_PREFIX + tr("Failed to install requirements for extension ") + extension);
            }
        }
    }
}

void PythonExtensionsPlugin::setupPythonExtensions()
{
    // Run the setup.py file for all extensions that provide it.
    // later, there might be a way to determine if the setup needs
    // to run.
    QDir extension_dir = extensionDir();
    if (!extension_dir.exists())
        return;

    QStringList extension_list = extensionList();
    for (const QString &extension : extension_list) {
        QFile extension_setup(extension_dir.absolutePath() + "/" + extension + "/setup.py");
        if (extension_setup.open(QIODevice::ReadOnly)) {
            QTextStream in(&extension_setup);
            QString setup_code = in.readAll();
            if (!PyUtil::runScriptWithPath(
                setup_code.toStdString(),
                QString(extension_dir.absolutePath() + "/" + extension).toStdString()
            )) {
                qWarning() << "Failed to setup extension" << extension;
                Core::MessageManager::write(Constants::MESSAGE_MANAGER_PREFIX + tr("Failed to setup extension ") + extension);
            }
        }
    }
}

void PythonExtensionsPlugin::initializePythonExtensions()
{
    // Search python directory in plugin paths
    QDir extension_dir = extensionDir();
    if (!extension_dir.exists()) {
        qWarning() << "Python extension directory not found";
        Core::MessageManager::write(Constants::MESSAGE_MANAGER_PREFIX + tr("Python extension directory not found"));
        return;
    }

    qDebug() << "Found Python extension directory at location" << extension_dir.absolutePath();

    QStringList extension_list = extensionList();

    qDebug() << "Number of Python extensions found:" << extension_list.size();

    // Run the extension initialization code
    for (const QString &extension : extension_list) {
        qDebug() << "Trying to initialize extension" << extension;

        QFile extension_main(extension_dir.absolutePath() + "/" + extension + "/main.py");
        if (extension_main.open(QIODevice::ReadOnly)) {
            QTextStream in(&extension_main);
            QString extension_code = in.readAll();
            if (!PyUtil::runScriptWithPath(
                extension_code.toStdString(),
                QString(extension_dir.absolutePath() + "/" + extension).toStdString()
            )) {
                qWarning() << "Failed to initialize extension" << extension;
                Core::MessageManager::write(Constants::MESSAGE_MANAGER_PREFIX + tr("Failed to initialize extension ") + extension);
            } else {
                m_loadedExtensions << extension;
            }
        } else {
            qWarning() << "Failed to load main.py for extension" << extension;
            Core::MessageManager::write(Constants::MESSAGE_MANAGER_PREFIX + tr("Failed to load main.py for extension ") + extension);
        }
    }

    qDebug() << "Number of Python extensions loaded:" << m_loadedExtensions.size();
}

} // namespace Internal
} // namespace PythonExtensions
