import os.path
import distutils.core


summary = ("flatkit is a library of utilities for projects that are based on "
           "Flask, Flatland and Htables.")


distutils.core.setup(
    name='flatkit',
    url='http://github.com/eaudeweb/flatkit/',
    description=summary,
    version='0.1',
    author='Eau de Web',
    author_email='office@eaudeweb.ro',
    packages=['flatkit'],
)
