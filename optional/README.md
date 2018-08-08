# Optional Bindings

This directory contains all optional bindings for QtCreator
Modules that are bundled with this plugin.

Optional bindings come in the form of dynamically loaded libraries,
each binding has its own folder. The template directory contains files
that are shared for each binding.

## Documentation

### Building
If your environment is setup correctly (i.e. you can build the Python Extensions plugin), all that
you should need to do is run:

```
python setup.py --qmake=/path/to/your/qmake
```

and the optional bindings should build and be installed. To clean the build files after a build,
just run:

```
python setup.py clean
```

For problems and possible solutions, please refer to the main `README.md`.

### Writing optional binding libraries
**NOTICE:** Please refer to the `pyutil.h` header file for anything that is not explained
here.

Each library project here must include a `binding.cpp` file which must implement
a function with the signature `void bind();`.
