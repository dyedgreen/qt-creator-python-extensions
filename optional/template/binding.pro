# NOTE: This is not yet properly tested on general systems
#       and will (if at all) probably only work on a linux environment

PYTHON = python
DEFINES += PYTHONEXTENSIONS_LIBRARY

# PythonExtensions files

SOURCES += \
        binding.cpp

HEADERS += \
        binding.h


# Qt Creator linking

## Either set the IDE_SOURCE_TREE when running qmake,
## or set the QTC_SOURCE environment variable, to override the default setting
isEmpty(IDE_SOURCE_TREE): IDE_SOURCE_TREE = $$(QTC_SOURCE)
isEmpty(IDE_SOURCE_TREE): IDE_SOURCE_TREE = "/home/tiroder/Documents/code/qt-creator"

## Either set the IDE_BUILD_TREE when running qmake,
## or set the QTC_BUILD environment variable, to override the default setting
isEmpty(IDE_BUILD_TREE): IDE_BUILD_TREE = $$(QTC_BUILD)
isEmpty(IDE_BUILD_TREE): IDE_BUILD_TREE = "/home/tiroder/Documents/code/qt-creator"

## uncomment to build plugin into user config directory
## <localappdata>/plugins/<ideversion>
##    where <localappdata> is e.g.
##    "%LOCALAPPDATA%\QtProject\qtcreator" on Windows Vista and later
##    "$XDG_DATA_HOME/data/QtProject/qtcreator" or "~/.local/share/data/QtProject/qtcreator" on Linux
##    "~/Library/Application Support/QtProject/Qt Creator" on macOS
USE_USER_DESTDIR = yes

## Include Qt and QtCreator paths
QT_INCLUDEPATHS = -I"$$[QT_INSTALL_HEADERS]" -I"$$[QT_INSTALL_HEADERS]/QtCore" \
    -I"$$[QT_INSTALL_HEADERS]/QtGui" -I"$$[QT_INSTALL_HEADERS]/QtWidgets" \
    -I"$$IDE_SOURCE_TREE/src/plugins" \
    -I"$$IDE_SOURCE_TREE/src/libs"

# Custom Buildsystem setup per binding
include(binding_custom.pri)

include($$IDE_SOURCE_TREE/src/qtcreatorplugin.pri)

# Shiboken stuff

# This setup is currently only tested on Linux

include(../../pyside2.pri)

SHIBOKEN_OPTIONS = --generator-set=shiboken --enable-parent-ctor-heuristic \
    --enable-pyside-extensions --enable-return-value-heuristic --use-isnull-as-nb_nonzero \
    $$QT_INCLUDEPATHS -I$$PWD -T$$PWD -T$$PYSIDE2/typesystems --output-directory=$$OUT_PWD

## Prepare the shiboken tool
QT_TOOL.shiboken.binary = $$system_path($$PYSIDE2/shiboken2)
qtPrepareTool(SHIBOKEN, shiboken)

## Shiboken run that adds the module wrapper to GENERATED_SOURCES
shiboken.output = $$WRAPPER_DIR/$${TYPESYSTEM_NAME}_module_wrapper.cpp
shiboken.commands = $$SHIBOKEN $$SHIBOKEN_OPTIONS $$PWD/$$WRAPPED_HEADER ${QMAKE_FILE_IN}
shiboken.input = TYPESYSTEM_FILE
shiboken.dependency_type = TYPE_C
shiboken.variable_out = GENERATED_SOURCES

module_wrapper_dummy_command.output = $$WRAPPER_DIR/${QMAKE_FILE_BASE}_wrapper.cpp
module_wrapper_dummy_command.commands = echo ${QMAKE_FILE_IN}
module_wrapper_dummy_command.depends = $$WRAPPER_DIR/$${TYPESYSTEM_NAME}_module_wrapper.cpp
module_wrapper_dummy_command.input = WRAPPED_CLASSES
module_wrapper_dummy_command.dependency_type = TYPE_C
module_wrapper_dummy_command.variable_out = GENERATED_SOURCES

## Get the path component to the active config build folder
defineReplace(getOutDir) {
  out_dir = $$OUT_PWD
  CONFIG(release, debug|release): out_dir = $$out_dir/release
  else:out_dir = $$out_dir/debug
  return($$out_dir)
}

QMAKE_EXTRA_COMPILERS += shiboken module_wrapper_dummy_command

# TODO: Fix some more of these hardcoded include paths
INCLUDEPATH += $$WRAPPER_DIR

for(i, PYSIDE2_INCLUDE) {
    INCLUDEPATH += $$i/QtWidgets $$i/QtGui $$i/QtCore
}
