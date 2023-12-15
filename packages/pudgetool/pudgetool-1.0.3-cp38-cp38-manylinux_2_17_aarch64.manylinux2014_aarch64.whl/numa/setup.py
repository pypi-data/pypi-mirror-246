#!/usr/bin/python3 
# -*- coding: utf-8 -*- 

from setuptools import setup, find_packages, Extension
from setuptools.command.install import install
from Cython.Build import cythonize
from distutils.sysconfig import get_python_lib
import os

class PostInstallCommand(install):
    """Post-installation for installation mode."""
    def run(self):
        # PUT YOUR POST-INSTALL SCRIPT HERE or CALL A FUNCTION
        install.run(self)
 
        pkg_path = get_python_lib()
        pg_path = os.path.join(pkg_path, 'pudge')

with open('requirements.txt') as f:
    required = f.read().splitlines()

package_dir = 'src'
try:
    from Cython.Distutils import build_ext

    source_file = os.path.join(package_dir, "numa/numa.pyx")
    cython_available = True
except ImportError:
    source_file = "numa.c"
    cython_available = False

extensions = [Extension("numa", ["src/numa/*.pyx"])]

options = {
    'ext_modules': cythonize(extensions)
}

# options = {'ext_modules': [
#         Extension("numa",
#             [source_file],
#             libraries=["numa"],
#             define_macros=[('NUMA_VERSION1_COMPATIBILITY', 1)],
#         ),
#     ]
# }

if cython_available:
    options['cmdclass'] = {"build_ext": build_ext}

setup(
    name = "pudgetool", 
    version = "1.0.4", 
    keywords = ("pudge tools", "CLI tools"),
    description = "pudge tools is automatic coding tools",  
    long_description = "convenient python cli tools, like s3, jumpserver url switches...",  
    license = "MIT Licence",  
    url = "https://github.com/ThierryZhou/pudgetool.git",
    author = "thierry.zhou",  
    author_email = "zhouhui295@163.com",
    platforms = "any",  
    install_requires = required,
    packages=['numa', 'pudgetool'],
    package_dir={
        '': 'src',
    },
    include_package_data = True,
    scripts = [],  
    entry_points = {  
        'console_scripts': [  
            'pg = pudgetool.entry_point:entry_point' 
        ]
    },
    **options
)