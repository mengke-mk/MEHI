from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

import  numpy

setup(
        cmdclass = {'build_ext': build_ext},
        ext_modules = [Extension("trans",
                       sources=["trans.pyx", "c_trans.c"],
                       include_dirs=[numpy.get_include()])],
)
