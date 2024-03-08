"""
build-ctypes

For a ctypes binding it is compiled on a specific platform
but does not need to be recompiled for every version of Python.

`cibuildwheel` isn't set up for this necessarily so we will
do some level of manual wangling here.

# Steps
- build the wheel with `pip wheel`
- build the library for the current platform using subprocess
- inject the library into the wheel
- fix the wheel tags to be `py3-none-{platform}`
"""
import os
import zipfile
import tempfile
import platform
import subprocess

cwd = os.path.abspath(os.path.dirname(__file__))
ctm_lib = os.path.join(cwd, 'upstream', 'OpenCTM', 'lib')

def build_manylinux(image: str):
    """
    Build OpenCTM on a manylinux image.
    """

    # remove any prior built artifacts from the library
    subprocess.check_call(['git', 'clean', '-xdf'],
                          cwd=ctm_lib)

    # compose a docker command to run 
    command = ['docker', 'run',
                '-v', f'{ctm_lib}:/ctmlib',
               '-w', '/ctmlib',
               image,
               'make -f Makefile.linux']
    print(' '.join(command))

    # build in the manylinux image
    # not sure why this doesn't work as a non-shell command
    subprocess.check_call(' '.join(command), shell=True)

    libname = 'libopenctm.so' 
    with open(os.path.join(ctm_lib, libname), 'rb') as f:
        return {libname: f.read()}
    
    
    

def to_wheel(libs: dict):
    
    with tempfile.TemporaryDirectory() as tmp:
        subprocess.check_call(['pip', 'wheel', '.', f'--wheel-dir={tmp}'])

        # there should only be one file in this temp directory
        wheel_name = os.listdir(tmp)[-1]
        file_name = os.path.join(tmp, wheel_name)
        assert file_name.endswith('.whl')

        # append the requested libraries to the zip archive
        with zipfile.ZipFile(file_name, 'a') as zipped:
            for lib, raw in libs.items():
                zipped.writestr(f'openctm/{lib}', raw)
            
        with open(file_name, 'rb') as f:
            return {wheel_name: f.read()}

def main():
    
    wheelhouse = os.path.join(cwd, 'wheelhouse')
    os.makedirs(wheelhouse, exist_ok=True)
    
    if platform.system() == 'Linux':
        # build on specific manylinux tag images
        manylinux = ['quay.io/pypa/manylinux2014_x86_64',
                     'quay.io/pypa/manylinux2014_i686']
        for image in manylinux:
            tag_platform = image.rsplit('/', 1)[-1]
            wheel = to_wheel(build_manylinux(image))
            tag_none = next(iter(wheel.keys()))
            # keep the `none` ABI
            # replace the `any` platform with manylinux
            tag_new = tag_none.replace('any', tag_platform)
            
            with open(os.path.join(wheelhouse, tag_new), 'wb') as f:
                f.write(wheel[tag_none])
                
    elif platform.system() == 'Windows':
        build_windows()
        

if __name__ == '__main__':

    main()
 
