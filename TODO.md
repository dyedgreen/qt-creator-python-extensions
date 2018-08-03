# To do list for the project

## Bindings
- [ ] Complete Core bindings (most of the necessary xml is there, but commented)
- [ ] Complete Utils bindings
- [ ] Maybe add more bindings from QtCreators libs (?)

## Optional Bindings
- [ ] Find a way to include the non-optional bindings (see `optional/texteditor/typesystem_texteditor.xml` for description of problem)
- [ ] Complete ProjectExplorer bindings
- [ ] Complete TextEditor bindings

## Build System
- [ ] Fix having to `export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/path/to/clang/lib`
- [ ] Automatically build optional bindings alongside main plugin (?)
- [ ] Fix optional bindings build system

## Examples
- [ ] Make a text editor example (once the text editor binding does anything)

## Documentation
- [ ] Write more docs for the optional binding (`optional/README.md`)

## Unit Tests
- [ ] Add unit tests for PyUtils (C++)
- [ ] Add unit tests for Bindings themselves (in Python unit test extension)

## Other
- [ ] Fix excessive line widths (run `tools/sanity.py` to find them)
- [ ] Maybe make tools executable (?) (adding `#!/usr/bin/env python`)
