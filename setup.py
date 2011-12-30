"""Build & packaging script for Ring.
"""

from setuptools import setup, find_packages

VERSION = '0.1.0'

def params():
    name = 'Ring'
    version = VERSION
    description = "Ring - a better planet"
    long_description = open("README.md").read()
    # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
    classifiers = [
            "Framework :: Flask",
            "Operating System :: OS Independent",
            "Programming Language :: Python",
            "Topic :: Internet :: WWW/HTTP",
            "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
            "Topic :: Internet :: WWW/HTTP :: WSGI",
            "Topic :: Software Development :: Libraries :: Application Frameworks",
            "Topic :: Software Development :: Libraries :: Python Modules",
    ]
    keywords = 'Ring Planet Feed RSS Atom aggregator'
    author = 'Stefane Fermigier'
    author_email = 'sf@fermigier.com'
    url = 'http://fermigier.com/'
    license = 'LGPL'

    packages = find_packages(exclude=['ez_setup'])
    print packages
   
    #namespace_packages = ['ring']
    include_package_data = True
    zip_safe = False
    install_requires = open("dependencies.txt").read().split('\n')
    entry_points = {
        'console_scripts': ['ring = ring:main'],
    }
    return locals()


setup(**params())
