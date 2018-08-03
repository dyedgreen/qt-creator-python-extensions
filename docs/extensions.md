# Documentation for Python Extension Authors

This document is intended to provide an introduction to writing Python extensions
for the QtCreator.

## Importing QtCreator specific modules
Currently, the bindings are available from Python under the following names:
```Python
from PythonExtension import QtCreator # Imports the generated module for the typesystem
from PythonExtension import PluginInstance # Imports the plugin instance
```

## `PythonExtension.PluginInstance`
This is the Python binding for the extension manager that works on the C++ side. It provides the
following functions, that can (and should) be used from Python:

```Python
from PythonExtension import PluginInstance as inst

# Returns a PySide QDir which points to the extension directory
inst.extensionDir()

# Returns a list with the names of all Python extensions
# If loaded only is supplied as True, only extensions that
# where loaded successfully are returned
inst.extensionList(loadedOnly = False)

# Mark an extension as loaded
# This should normally not be used and exists mainly
# for use by the extension manager
inst.flagAsLoaded("name_of_extension")

# Returns the path of the custom location to
# where missing dependencies should be pip installed
inst.pythonPackagePath()
```


# QtCreator bindings
Generally, the parts of QtCreator that are exposed have an interface that is nearly
identical to the C++ interface.

## Working with Menus
You can add new items to the menus of QtCreator. You can either add an action directly, or
add a new action container, that holds a sub-menu.

### Adding a sub menu
The following code snippet illustrates how to add a new menu.

```Python
from PythonExtension import QtCreator

def hello():
    print("Hello World.")

# By convention, the menuId starts with "Python"
menuId = "Python.SmallMenu.Menu"

menu = QtCreator.Core.ActionManager.createMenu(menuId)
menu.menu().setTitle("My menu")
menu.menu().addAction("My action", hello)
# Add our new menu to the "Tools" menu in QtCreator
QtCreator.Core.ActionManager.actionContainer("QtCreator.Menu.Tools").addMenu(menu)
```

### Adding a new action directly
The following code snippet illustrates how to add a new action to an existing action container.

```Python
from PythonExtension import QtCreator

def hello():
    print("Hello World.")

# Add a new action to the "Tools" menu
menu = QtCreator.Core.ActionManager.actionContainer("QtCreator.Menu.Tools")
menu.menu().addAction("My action", hello)
```

### Menu Id list
Currently, the following menu ids are available in QtCreator.

```Python
"QtCreator.Menu.File"
"QtCreator.Menu.File.RecentFiles"
"QtCreator.Menu.Edit"
"QtCreator.Menu.Edit.Advanced"
"QtCreator.Menu.Tools"
"QtCreator.Menu.Tools.External"
"QtCreator.Menu.Window"
"QtCreator.Menu.Window.Panes"
"QtCreator.Menu.Window.ModeStyles"
"QtCreator.Menu.Window.Views"
"QtCreator.Menu.Help"
```


# The embedded Python interpreter

## Python modules and `sys.path`
When importing modules, the following important locations will be checked (in this order):

 1. The folder of the extension itself (files and folders in your extension)
 2. The system Python path entries (anything you `pip install`ed globally)
 3. The QtCreator specific Python module directory
    - Note: This is where you should install any dependencies missing
      if you want to use non-standard Python packages / modules
    - This last path is accessible with `PluginInstance.pythonPackagePath()`

Any changes you make to sys.path and any modules you import, will be cleared after your script
finished executing.

## Reserved variable names
Names that look like
```Python
qt_creator_{SOME_NAME}_symbol_mchawrioklpilnjajqkfl
```
are reserved for the ExtensionManager. Unless you know exactly what you are doing, you should never
touch any of these variables.

## Installing dependencies
There are two ways you can install dependencies. If you need very fine-grained control over how
extension looks like before it can be run, you can supply a `setup.py` script, which is run
separately before your extension is started. An example of such a script can be found in the example
extension `examples/numpysetup`.

If you only want to install dependencies, you can also include a standard Python `requirements.txt`
file in your extension folder. **Note that this file is pip installed _once_.** After the initial
pip install, a new file called `requirements.txt.installed` is created in the extensions folder. To
run the install again, this file simply has to be deleted. **Be careful to remove this file, when
distributing your extension in a .zip file.**
