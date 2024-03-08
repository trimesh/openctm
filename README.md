# openctm

A wheel-packaged binding for OpenCTM.

## Install

There should be wheels for Mac, Windows, and Linux on PyPi:

```
pip install openctm
```

## Building

This is a ctypes binding it is compiled on a specific platform
but does not need to be recompiled for every version of Python.

`cibuildwheel` isn't set up for this necessarily so we will
do some level of manual wangling here.

# Steps
1. build the library for the current platform using subprocess
2. build the wheel with `pip wheel` which only contains Python
3. Inject the built library into the wheel
4. Fix the wheel tags to be `py3-none-{platform}`