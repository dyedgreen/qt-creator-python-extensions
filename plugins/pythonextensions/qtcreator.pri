# QtCreator specific build settings
# (shared by plugin and optional bindings)

## Either set the IDE_SOURCE_TREE when running qmake,
## or set the QTC_SOURCE environment variable, to override the default setting
isEmpty(IDE_SOURCE_TREE): IDE_SOURCE_TREE = $$(QTC_SOURCE)

## Either set the IDE_BUILD_TREE when running qmake,
## or set the QTC_BUILD environment variable, to override the default setting
isEmpty(IDE_BUILD_TREE): IDE_BUILD_TREE = $$(QTC_BUILD)

# KEEP this line and DON'T edit it!
# (if you NEED to change it, have a look at tools/build.py)
# USE_USER_DESTDIR = yes
# END KEEP