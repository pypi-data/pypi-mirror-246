import os, sys
from setuptools import setup, find_packages

os.system('python ./iris-jwst/HITRAN/Create_ir_model_files.py')


setup(
    name='iris-jwst',
    version='0.1.4',
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
    python_requires='>=3.8'
)



