# Python Extension Examples

This directory contains examples of what Python extensions might look like. Each extension is in its
own directory, where you can inspect its source code.


## How to install
If you want to install some of these extensions to play around with them, you can use the
`package.py` utility. Run `$ python package.py` in your terminal, to generate extension packages
(.zip files) of all the extensions in this directory. The generated extension packages can then be
installed into your QtCreator using the extension manager that comes with the plugin. (Find the
extension manager in the help menu of your QtCreator.)

To clean this directory from generated packages, simply run `$ python package.py clean` in your
terminal. Note that for your own Python extensions, it is sufficient to distribute .zip
files, which you can easily generate manually. **Remember to include a top-level directory** when
making your own extension packages.
