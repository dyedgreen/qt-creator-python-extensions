TEMPLATE = subdirs

SUBDIRS += \
    plugins/haskell

# Note: This does not yet include the
#       optional bindings. They have to
#       be built using their own setup.py,
#       or using the tools/build.py
