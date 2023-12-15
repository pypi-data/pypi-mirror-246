#!/usr/bin/python3 
# -*- coding: utf-8 -*- 

from setuptools import setup, Extension
from setuptools.command.install import install
from distutils.sysconfig import get_python_lib
from Cython.Build import cythonize, build_ext
import os

setup_dir = os.path.dirname(os.path.abspath(__file__))

package_name = "numa"
package_dir = 'src/numa'
source_files = [
    os.path.join(package_dir, "numa.pyx"),
]

extensions = [
    Extension(
        package_name,
        source_files,
        include_dirs= [
            package_dir,
        ],
        libraries=["numa"],
        library_dirs = [
            package_dir,
        ],
        define_macros=[('NUMA_VERSION1_COMPATIBILITY', 1)],
    ),
]

setup(
    ext_modules = cythonize(
        extensions,
        include_path = [
            package_dir,
        ]),
    cmdclass = {
        'build_ext': build_ext
    },
    package_data = {
        "numa": ["*.pxd"],
    },

)