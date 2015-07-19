from distutils.core import setup
from distutils.extension import Extension
from Cython.Build import cythonize
from Cython.Distutils import build_ext
import numpy

extension = Extension(
           "sub",
           sources=["sub.pyx", "sub_bg.cpp"],
           include_dirs=[numpy.get_include()],
           language="c++",
)

setup(
        cmdclass = {'build_ext': build_ext},
        ext_modules = cythonize(extension),
)
