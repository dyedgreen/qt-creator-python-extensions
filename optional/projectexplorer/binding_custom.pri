# Additional sources

SOURCES += \
        # optional

HEADERS += \
        # optional


# Declare dependencies and name

# This has to be PythonBinding{PluginName}
QTC_PLUGIN_NAME = PythonBindingProjectExplorer
QTC_LIB_DEPENDS += \
    extensionsystem \
    utils

QTC_PLUGIN_DEPENDS += \
    coreplugin \
    projectexplorer \
    pythonextensions

QTC_PLUGIN_RECOMMENDS += \
    # optional plugin dependencies. nothing here at this time


# Shiboken binding generation setup

WRAPPED_HEADER = wrappedclasses.h
WRAPPER_DIR = $$OUT_PWD/QtCreatorBindingProjectExplorer
TYPESYSTEM_FILE = typesystem_projectexplorer.xml

TYPESYSTEM_NAME = qtcreatorbindingprojectexplorer

## Include additional QtCreator paths
QT_INCLUDEPATHS += \
    -I"$$IDE_SOURCE_TREE/src/plugins/projectexplorer"

INCLUDEPATH += \
    $$IDE_SOURCE_TREE/src/plugins/projectexplorer

## These headers are needed so the generated wrappers are added to the
## build. Right now they are empty files, however there might be a more elegant
## option.
WRAPPED_CLASSES = \
  bindingheaders/projectexplorer.h \
  bindingheaders/projectexplorer_buildconfiguration.h \
  bindingheaders/projectexplorer_projectconfiguration.h \
  # bindingheaders/projectexplorer_ibuildconfigurationfactory.h
# Sentinel line
