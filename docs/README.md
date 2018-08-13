# Documentation for Python Extensions

This is the documentation for the QtCreator Python Extensions plugin.

## Contents
 1. [Writing Python Extensions](./extensions.md)
 2. [The C++ PythonExtensionsPlugin](./plugin.md)
 3. [Build and Development Tools](./tools.md)

## General overview

Please refer to the section \`How it works' in the main [README.md](../README.md) file.

## A Note regarding Python versions
In principle, the C++ plugin supports both Python 2 and 3 (at least for the versions tested, i.e.
2.7 and 3.5). However, the extensions themselves might only support one version of Python. This is
currently the case for the extension manager.
