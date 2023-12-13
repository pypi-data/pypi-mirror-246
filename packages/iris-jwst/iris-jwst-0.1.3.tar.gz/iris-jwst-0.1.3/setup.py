import os, sys
from setuptools import setup, find_packages
from setuptools.command.install import install as _install


def _post_install(dir):
    from subprocess import call
    call(['python', './iris-jwst/HITRAN/Create_ir_model_files.py'])


class install(_install):
    def run(self):
        _install.run(self)
        self.execute(_post_install, (self.install_lib,),
                     msg="Downloading HITRAN data...")
        
setup(
    name='iris-jwst',
    version='0.1.3',
    author='Carlos E. Muñoz-Romero',
    author_email='carlos.munoz_romero@cfa.harvard.edu',
    description='iris-jwst is a GPU-accelerated package to generate high-resolution \
                 opacity-weighted molecular line intensities to model JWST MIRI MRS spectra.',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.8',
    cmdclass={'install': install}
)



