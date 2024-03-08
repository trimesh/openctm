# openctm
[![Build And Release Wheels](https://github.com/trimesh/openctm/actions/workflows/wheels.yml/badge.svg)](https://github.com/trimesh/openctm/actions/workflows/wheels.yml) [![PyPI version](https://badge.fury.io/py/openctm.svg)](https://badge.fury.io/py/openctm)

A wheel-packaged binding for [OpenCTM](https://openctm.sourceforge.net/) Python bindings. 

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

The build steps are:
1. build the library for the current platform using subprocess
2. build the wheel with `pip wheel` which only contains Python
3. Inject the built library into the wheel
4. Fix the wheel tags to be `py3-none-{platform}`
  - this indicates it runs on any Python 3
  - it does not require a specific ABI
  - it will only run on the platform specified (windows/mac/linux)

This is done automatically in `build.py`