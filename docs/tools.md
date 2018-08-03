# Documentation regarding included tools / utilities

This project includes a few Python scripts, included as utilities for convenience. All of these are
relatively small and self-contained. They should also all include usage instructions in comments at
the beginning of the scripts. Some of them are scattered around the project. These include:

 * [The optional bindings build script](../optional/setup.py)
   - This script is intended to help building the optional bindings, by bundling files needed by
     all optional binding libraries in a `template` directory.
   - **Available options are:**
     - --qmake=/path/to/your/qmake *required*
     - --only=binding_dir *optional, only build binding_dir*
     - clean *optional, ignores all options and removes the build directories*

 * [The example packaging script](../examples/package.py)
   - This script creates .zip files for use with the included extension manager form the example
     extension sources.
   - **Available options are:**
     - *run with no arguments in `examples` directory to create extension .zip files*
     - clean *remove generated .zip files*
   - **Note:** There is a symbolic link to this script in the `tests` directory

The other scripts are in the [tools folder](../tools/), they are:

 * [The license script](../tools/license.py)
   - This script adds the Qt license to all relevant source files.
   - Takes no options and should be run in root directory with `$ python ./tools/license.py`.

 * [PySide build helper script](../tools/pyside2_config.py)
   - This is taken verbatim from the pyside-setup project and is used to discover the pyside
     installation / setup during builds. Should not be used manually.

 * [Sanity helper script](../tools/sanity.py)
   - This script automatically corrects some annoying nags for the Qt Gerrit sanity check.
   - Takes no options and should be run in root directory with `$ python ./tools/sanity.py`.

 * [Build helper script](../tools/build.py)
   - This script executes all the build scripts in this project in the correct order
   - Mainly for lazy people and only usable if everything is setup correctly
   - **Available options are:**
     - --qmake=/path/to/your/qmake *required*
     - --skip *optional, only build main c++ plugin*
     - --user *optional, build to user directory*