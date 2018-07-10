import os

from setuptools import setup


here = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(here, 'c302', '__version__.py')) as version_file:
    exec (version_file.read(), about)
version = about['__version__']


long_description = """
c302 is a framework for generating network models in NeuroML 2 based on C elegans connectivity data. Part of the OpenWorm project
"""

setup(
    name = 'c302',
    version=version,
    author='Padraig Gleeson and OpenWorm contributors',
    author_email='p.gleeson@gmail.com',
    packages = ['c302'],
    install_requires=[
        'numpy',
        'xlrd',
        'xlwt',
        'libNeuroML>=0.2.39',
        'pyNeuroML>=0.3.11',
        'pyopenworm==0.7.1'
    ],
    entry_points={
        'console_scripts': ['c302 = c302.__init__:main']},
    package_data={
        'c302': [
            '*.xml',
            'data/*',
            'NeuroML2/*']},
    description = 'c302 is a framework for generating models of the worm C. elegans',
    long_description = long_description,
    license = 'MIT',
    url='http://github.com/openworm/c302',
    download_url = 'https://github.com/openworm/c302/archive/master.zip',
    classifiers = [
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering'
    ]
)
