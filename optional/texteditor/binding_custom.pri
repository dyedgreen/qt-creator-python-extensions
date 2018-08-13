# Additional sources

SOURCES += \
        # optional

HEADERS += \
        # optional


# Declare dependencies and name

# This has to be PythonBinding{PluginName}
QTC_PLUGIN_NAME = PythonBindingTextEditor
QTC_LIB_DEPENDS += \
    extensionsystem \
    utils

QTC_PLUGIN_DEPENDS += \
    coreplugin \
    texteditor \
    pythonextensions

QTC_PLUGIN_RECOMMENDS += \
    # optional plugin dependencies. nothing here at this time


# Shiboken binding generation setup

WRAPPED_HEADER = wrappedclasses.h
WRAPPER_DIR = $$OUT_PWD/QtCreatorBindingTextEditor
TYPESYSTEM_FILE = typesystem_texteditor.xml

TYPESYSTEM_NAME = qtcreatorbindingtexteditor

## Include additional QtCreator paths
QT_INCLUDEPATHS += \
    -I"$$IDE_SOURCE_TREE/src/plugins/texteditor"

INCLUDEPATH += \
    $$IDE_SOURCE_TREE/src/plugins/coreplugin \
    $$IDE_SOURCE_TREE/src/plugins/coreplugin/editormanager \
    $$IDE_SOURCE_TREE/src/plugins/coreplugin/find \
    $$IDE_SOURCE_TREE/src/plugins/texteditor \
    "$$IDE_SOURCE_TREE/src/libs/utils"

## These headers are needed so the generated wrappers are added to the
## build. Right now they are empty files, however there might be a more elegant
## option.
WRAPPED_CLASSES = \
  bindingheaders/texteditor.h \
# Sentinel line
