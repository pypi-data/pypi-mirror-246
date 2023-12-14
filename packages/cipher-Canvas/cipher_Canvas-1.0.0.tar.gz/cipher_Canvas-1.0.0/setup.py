# setup.py
from setuptools import setup, find_packages

setup(
    name='cipher_Canvas',
    version='1.0.0',
    author='Mani',
    description='A package for embedding and extracting text within images using markers.',
    license='MIT',
    packages=find_packages(),
    install_requires=['Pillow'],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
