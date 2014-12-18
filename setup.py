import os

from setuptools import setup, find_packages

setup(
    name='sxri_pipeline',
    version='0.1',
    author = "Lenneke Jong",
    author_email= 'lenneke.jong@synchrotron.org.au',
    description = "sxri_pipeline",
    packages=find_packages(),
    license='LICENSE',
    install_requires=[
	    "numpy",
        "h5py",
        #"pyNADIA"
    ],
)