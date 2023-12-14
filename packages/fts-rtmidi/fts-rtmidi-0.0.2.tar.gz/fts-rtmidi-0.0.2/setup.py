"""Created using tutorial: https://www.youtube.com/watch?v=tEFkHEKypLI&ab_channel=NeuralNine"""

from setuptools import setup, find_packages
import codecs
import os

root = os.path.abspath(os.path.dirname(__file__))

setup(
    name         = 'fts-rtmidi',
    author       = 'Ferdinand Oliver M Tonby-Strandborg',
    author_email = 'ferdinand.tonby.strandborg@gmail.com',
    description  = 'Simple class for MIDI control',
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
    install_requires = [
        'python-rtmidi>=1.5.8',
    ],
    packages = find_packages(include=['src/*']),
)
